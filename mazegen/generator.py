"""Random maze generation, reproducible from a seed."""

import random

from .maze import Maze


class MazeGenerator:
    """Generate random mazes of a given size.

    The generator keeps the shape of the maze (size, entry, exit,
    perfect). Each call to ``generate`` builds a new maze; pass a seed to
    get the same maze again.

    Example::

        generator = MazeGenerator(20, 15, entry=(0, 0), exit=(19, 14))
        maze = generator.generate(seed=42)  # always the same maze
        maze.cells[0][0]                    # walls of the top-left cell
        maze.solve()                        # e.g. "EESSE..."
        other = generator.generate()        # a new random maze
        other.seed                          # seed to get it back

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell as ``(x, y)``.
        exit: Exit cell as ``(x, y)``.
        perfect: If True, there is exactly one path between any two
            cells. If False, the maze also has some loops.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = True,
    ) -> None:
        """Check the arguments and store them.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: Entry cell as ``(x, y)``.
            exit: Exit cell as ``(x, y)``.
            perfect: Whether the maze must be perfect.

        Raises:
            ValueError: If the size is not positive, or if the entry or
                the exit is outside the maze, or if they are the same.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"{name} {x},{y} is outside the maze")
        if entry == exit:
            raise ValueError("entry and exit must be different")
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

    def generate(self, seed: int | None = None) -> Maze:
        """Build a new maze.

        The result always follows the rules of the subject: coherent
        walls, closed outer border, every cell reachable except the
        "42", no open area of 3x3 cells or more, and exactly one path
        between any two cells if ``perfect`` is True.

        Args:
            seed: Seed for the random generator. The same seed always
                gives the same maze. If None, a random seed is chosen
                and saved in ``maze.seed``.

        Returns:
            The generated maze. ``maze.pattern`` is empty if the maze
            was too small for the "42".

        Raises:
            ValueError: If the entry or the exit falls on a cell of the
                "42" pattern.
        """
        if seed is None:
            seed = random.randrange(2**32)
        rng = random.Random(seed)
        maze = Maze.closed(
            self.width, self.height, self.entry, self.exit, seed
        )
        self._place_pattern(maze)
        self._carve(maze, rng)
        if not self.perfect:
            self._add_loops(maze, rng)
        return maze

    def _place_pattern(self, maze: Maze) -> None:
        """Reserve the cells that draw the "42".

        Args:
            maze: Fully closed maze to draw the pattern on.

        Raises:
            ValueError: If the entry or the exit is one of the pattern
                cells.
        """
        # TODO:
        #  - Decide the shape of the "42" (e.g. a small grid of 0/1) and
        #    place it in the centre of the maze.
        #  - Add its cells to maze.pattern. They are already fully
        #    closed: _carve must never open them.
        #  - If the maze is too small, leave maze.pattern empty and
        #    return. The program (not this class) prints the error.
        #  - If self.entry or self.exit is a pattern cell, raise
        #    ValueError.
        raise NotImplementedError("pattern is not implemented yet")

    def _carve(self, maze: Maze, rng: random.Random) -> None:
        """Open walls until every cell is reachable: a perfect maze.

        Args:
            maze: Maze with the "42" already placed.
            rng: Random generator to use. Never use the functions of the
                ``random`` module directly, or the seed stops working.
        """
        # TODO: generation algorithm (e.g. recursive backtracker, Prim,
        # Kruskal, Wilson...). Explain in the README which one and WHY.
        #  - Open walls only with maze.open_wall(x, y, direction):
        #    it keeps the walls coherent and the outer border closed.
        #  - Skip the cells in maze.pattern.
        #  - Every other cell must be reachable from the entry.
        #  - Opening exactly one wall per newly visited cell builds a
        #    spanning tree: one single path between any two cells.
        #  A spanning tree never has open 2x2 areas, so the "no 3x3
        #  open area" rule only matters in _add_loops.
        raise NotImplementedError("generation is not implemented yet")

    def _add_loops(self, maze: Maze, rng: random.Random) -> None:
        """Open some extra walls so the maze has loops (PERFECT=False).

        Args:
            maze: Perfect maze returned by ``_carve``.
            rng: Random generator to use.
        """
        # TODO:
        #  - Open a few random walls that are still closed (never on
        #    pattern cells nor on the outer border).
        #  - Before opening a wall, check that it does not create an
        #    open area of 3x3 cells or more (subject rule).
        raise NotImplementedError("loops are not implemented yet")
