"""Random maze generation, reproducible from a seed."""

from .maze import Maze

# Only the public interface below is fixed, because the rest of the program
# uses it: MazeGenerator(width, height, entry, exit, perfect) and
# generate(seed) returning a Maze. Everything else is up to you: the
# algorithm, helper methods or functions, new files inside mazegen/...
#
# Hints:
#  - maze.py has optional helpers: Maze.closed() builds a maze with every
#    wall closed, and maze.open_wall() opens a wall on both sides at once,
#    so walls stay coherent. Use them only if they help.
#  - For the seed to work, use your own random.Random(seed) instance
#    instead of the functions of the random module.
#  - The cells of the "42" go in maze.pattern (left empty if it does not
#    fit); the program prints the warning, not this class.
#  - Explain in the README which algorithm you chose and why.


class MazeGenerator:
    """Generate random mazes of a given size.

    The generator keeps the shape of the maze (size, entry, exit,
    perfect). Each call to ``generate`` builds a new maze; pass a seed to
    get the same maze again.

    Example::

        generator = MazeGenerator(20, 15, entry=(0, 0), exit=(19, 14))
        maze = generator.generate(seed=42)  # always the same maze
        maze.cells[0][0]                    # walls of the top-left cell
        solve(maze)                         # e.g. "EESSE..."
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

        The maze must follow the rules of the subject:

        - walls are coherent between neighbouring cells;
        - the outer border is closed;
        - every cell can be reached, except the cells of the "42";
        - there is no open area of 3x3 cells or more;
        - if ``perfect`` is True, there is exactly one path between any
          two cells.

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
        raise NotImplementedError("generate is not implemented yet")
