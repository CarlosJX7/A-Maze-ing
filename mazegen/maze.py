"""Maze data structure, shared by the generator, the solver and the display.

Coordinates are ``(x, y)``: ``x`` is the column (0 = left) and ``y`` is
the row (0 = top). Cells are stored row by row, so the cell at ``(x, y)``
is ``maze.cells[y][x]``.

Each cell is an ``int`` whose bits are its CLOSED walls, the same encoding
as the output file::

    bit 0 (1) North    bit 1 (2) East    bit 2 (4) South    bit 3 (8) West

so ``15`` (``F``) is a fully closed cell and ``0`` has no walls at all.
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import NamedTuple


class Direction(NamedTuple):
    """A move from a cell to one of its four neighbours.

    Attributes:
        letter: Letter used in the solution path (``N``, ``E``, ``S``, ``W``).
        wall: Bit of the wall on this side of a cell.
        dx: Column change when moving in this direction.
        dy: Row change when moving in this direction.
    """

    letter: str
    wall: int
    dx: int
    dy: int


NORTH = Direction("N", 1, 0, -1)
EAST = Direction("E", 2, 1, 0)
SOUTH = Direction("S", 4, 0, 1)
WEST = Direction("W", 8, -1, 0)

DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
OPPOSITE: dict[Direction, Direction] = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}
ALL_WALLS = NORTH.wall | EAST.wall | SOUTH.wall | WEST.wall


@dataclass
class Maze:
    """A rectangular grid of cells with walls.

    ``open_wall`` updates both cells at once, which keeps the walls
    coherent between neighbours.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell as ``(x, y)``.
        exit: Exit cell as ``(x, y)``.
        seed: Seed used to generate this maze. The same seed and the
            same generator arguments always give the same maze.
        cells: Closed walls of each cell, indexed as ``cells[y][x]``.
        pattern: Cells that draw the "42". They stay fully closed and
            cannot be reached. Empty if the maze is too small for it.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    seed: int
    cells: list[list[int]]
    pattern: set[tuple[int, int]] = field(default_factory=set)

    @classmethod
    def closed(
        cls,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int,
    ) -> "Maze":
        """Create a maze where every wall of every cell is closed.

        This is the usual starting point of a generation algorithm,
        which then opens walls to carve the corridors.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: Entry cell as ``(x, y)``.
            exit: Exit cell as ``(x, y)``.
            seed: Seed used to generate the maze.

        Returns:
            A maze with all the cells set to ``ALL_WALLS``.
        """
        cells = [[ALL_WALLS] * width for _ in range(height)]
        return cls(width, height, entry, exit, seed, cells)

    def in_bounds(self, x: int, y: int) -> bool:
        """Tell whether ``(x, y)`` is a cell of the maze.

        Args:
            x: Column.
            y: Row.

        Returns:
            True if the cell is inside the maze.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        """Tell whether a cell has a closed wall on one side.

        Args:
            x: Column of the cell.
            y: Row of the cell.
            direction: Side of the cell to check.

        Returns:
            True if the wall on that side is closed.
        """
        return bool(self.cells[y][x] & direction.wall)

    def neighbours(
        self, x: int, y: int
    ) -> Iterator[tuple[Direction, int, int]]:
        """Yield the cells next to ``(x, y)`` that are inside the maze.

        Walls are not checked: use ``has_wall`` to know if the neighbour
        can be reached.

        Args:
            x: Column of the cell.
            y: Row of the cell.

        Yields:
            ``(direction, nx, ny)``: the direction to go from ``(x, y)``
            to the neighbour, and the neighbour's coordinates.
        """
        for direction in DIRECTIONS:
            nx, ny = x + direction.dx, y + direction.dy
            if self.in_bounds(nx, ny):
                yield direction, nx, ny

    def open_wall(self, x: int, y: int, direction: Direction) -> None:
        """Remove the wall between ``(x, y)`` and its neighbour.

        Both cells are updated, so walls always stay coherent.

        Args:
            x: Column of the cell.
            y: Row of the cell.
            direction: Side of the cell where the wall is removed.

        Raises:
            ValueError: If the neighbour is outside the maze. The outer
                border always stays closed.
        """
        nx, ny = x + direction.dx, y + direction.dy
        if not self.in_bounds(nx, ny):
            raise ValueError(f"cannot open the outer wall of ({x}, {y})")
        self.cells[y][x] &= ~direction.wall
        self.cells[ny][nx] &= ~OPPOSITE[direction].wall
