"""Small hand-made mazes, to work without the real generator.

Each function builds a maze by opening walls one by one, and ``CASES``
lists every maze with its expected shortest path.

Run ``python3 -m tests.fake_mazes`` to see them drawn in the terminal.
"""

from collections.abc import Callable

from mazegen import DIRECTIONS, EAST, NORTH, SOUTH, WEST, Direction, Maze

Opening = tuple[int, int, Direction]


def _build(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
    openings: list[Opening],
) -> Maze:
    """Create a closed maze and open the given walls.

    Args:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell as ``(x, y)``.
        exit: Exit cell as ``(x, y)``.
        openings: Walls to open, as ``(x, y, direction)``.

    Returns:
        The maze.
    """
    maze = Maze.closed(width, height, entry, exit, seed=0)
    for x, y, direction in openings:
        maze.open_wall(x, y, direction)
    return maze


def two_cells() -> Maze:
    """Two cells side by side. Shortest path: ``E``.

    Returns:
        The maze.
    """
    return _build(2, 1, (0, 0), (1, 0), [(0, 0, EAST)])


def two_cells_reversed() -> Maze:
    """Same maze, going from right to left. Shortest path: ``W``.

    Returns:
        The maze.
    """
    return _build(2, 1, (1, 0), (0, 0), [(0, 0, EAST)])


def perfect_4x3() -> Maze:
    """Perfect maze (a single path), with dead ends.

    Shortest path: ``ESWSEEE``.

    Returns:
        The maze.
    """
    return _build(4, 3, (0, 0), (3, 2), [
        (0, 0, EAST),
        (1, 0, SOUTH),
        (1, 1, WEST),
        (0, 1, SOUTH),
        (0, 2, EAST),
        (1, 2, EAST),
        (2, 2, EAST),
        (3, 2, NORTH),
        (3, 1, WEST),
        (2, 1, NORTH),
        (2, 0, EAST),
    ])


def two_routes_3x3() -> Maze:
    """Maze with a loop: a short route and a long one.

    Short route: ``EESS`` (4 moves). Long route: ``SSENES`` (6 moves).
    A depth-first search that tries South first finds the long one; a
    breadth-first search always finds the short one.

    Returns:
        The maze.
    """
    return _build(3, 3, (0, 0), (2, 2), [
        (0, 0, EAST),
        (1, 0, EAST),
        (2, 0, SOUTH),
        (2, 1, SOUTH),
        (0, 0, SOUTH),
        (0, 1, SOUTH),
        (0, 2, EAST),
        (1, 2, NORTH),
        (1, 1, EAST),
    ])


def around_pattern_5x3() -> Maze:
    """Maze with a closed "42"-like cell in the middle to go around.

    Shortest path: ``NEEEES``.

    Returns:
        The maze.
    """
    maze = _build(5, 3, (0, 1), (4, 1), [
        (0, 1, NORTH),
        (0, 0, EAST),
        (1, 0, EAST),
        (2, 0, EAST),
        (3, 0, EAST),
        (4, 0, SOUTH),
        (1, 0, SOUTH),
        (0, 1, SOUTH),
        (0, 2, EAST),
        (1, 2, EAST),
        (2, 2, EAST),
        (3, 2, NORTH),
        (4, 1, SOUTH),
    ])
    maze.pattern.add((2, 1))
    return maze


def unreachable() -> Maze:
    """The exit cannot be reached: ``solve`` must raise ``ValueError``.

    Returns:
        The maze.
    """
    return _build(3, 1, (0, 0), (2, 0), [(0, 0, EAST)])


CASES: list[tuple[Callable[[], Maze], str | None]] = [
    (two_cells, "E"),
    (two_cells_reversed, "W"),
    (perfect_4x3, "ESWSEEE"),
    (two_routes_3x3, "EESS"),
    (around_pattern_5x3, "NEEEES"),
    (unreachable, None),
]
"""Every fake maze with its shortest path (None: no path)."""


def path_cells(maze: Maze, path: str) -> list[tuple[int, int]]:
    """Follow a path from the entry and list the cells it goes through.

    Args:
        maze: The maze.
        path: Moves, one letter per move (``N``, ``E``, ``S``, ``W``).

    Returns:
        The cells visited, entry included.
    """
    by_letter = {direction.letter: direction for direction in DIRECTIONS}
    x, y = maze.entry
    cells = [(x, y)]
    for letter in path:
        direction = by_letter[letter]
        x, y = x + direction.dx, y + direction.dy
        cells.append((x, y))
    return cells


def draw(maze: Maze, path: str = "") -> str:
    """Draw a maze in ASCII, for debugging.

    ``E`` is the entry, ``X`` the exit, ``.`` the path and ``###`` a
    cell of the "42".

    Args:
        maze: The maze to draw.
        path: Optional path to show from the entry.

    Returns:
        The drawing, one line per text row.
    """
    on_path = set(path_cells(maze, path)) if path else set()
    lines = []
    for y in range(maze.height):
        top = "+"
        middle = ""
        for x in range(maze.width):
            top += "---+" if maze.has_wall(x, y, NORTH) else "   +"
            middle += "|" if maze.has_wall(x, y, WEST) else " "
            if (x, y) == maze.entry:
                middle += " E "
            elif (x, y) == maze.exit:
                middle += " X "
            elif (x, y) in maze.pattern:
                middle += "###"
            elif (x, y) in on_path:
                middle += " . "
            else:
                middle += "   "
        last = maze.width - 1
        middle += "|" if maze.has_wall(last, y, EAST) else " "
        lines += [top, middle]
    bottom = "+"
    for x in range(maze.width):
        has_wall = maze.has_wall(x, maze.height - 1, SOUTH)
        bottom += "---+" if has_wall else "   +"
    lines.append(bottom)
    return "\n".join(lines)


if __name__ == "__main__":
    for build, expected in CASES:
        print(f"{build.__name__}  ->  expected: {expected}")
        print(draw(build(), expected or ""))
        print()
