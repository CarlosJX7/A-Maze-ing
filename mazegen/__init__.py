"""mazegen: random maze generation, reproducible from a seed.

Example::

    from mazegen import MazeGenerator, solve

    generator = MazeGenerator(20, 15, entry=(0, 0), exit=(19, 14))
    maze = generator.generate(seed=42)
    print(maze.cells[0][0])  # closed walls of the top-left cell
    print(solve(maze))       # shortest path, e.g. "EESSE..."
"""

from .generator import MazeGenerator
from .maze import (
    ALL_WALLS,
    DIRECTIONS,
    EAST,
    NORTH,
    OPPOSITE,
    SOUTH,
    WEST,
    Direction,
    Maze,
)
from .solver import solve

__version__ = "1.0.0"

__all__ = [
    "ALL_WALLS",
    "DIRECTIONS",
    "EAST",
    "NORTH",
    "OPPOSITE",
    "SOUTH",
    "WEST",
    "Direction",
    "Maze",
    "MazeGenerator",
    "solve",
]
