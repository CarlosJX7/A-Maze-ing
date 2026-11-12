"""Shortest path between the entry and the exit of a maze."""

from .maze import Maze


def solve(maze: Maze) -> str:
    """Find the shortest path from the entry to the exit.

    The maze is only read, never modified.

    Args:
        maze: The maze to solve.

    Returns:
        The moves to follow from the entry, one letter per move,
        for example ``"EESWS"``.

    Raises:
        ValueError: If the exit cannot be reached from the entry.
    """
    # TODO: breadth-first search (BFS) from maze.entry.
    #  - Use a queue (collections.deque) of cells to visit and a
    #    dict that remembers, for each visited cell, the cell and the
    #    Direction it was reached from.
    #  - From a cell, you can move to a neighbour (maze.neighbours)
    #    only if there is no wall in between (maze.has_wall).
    #  - When maze.exit is reached, walk the dict back to the entry
    #    and join the Direction letters in the right order.
    #  BFS always finds a shortest path, even if PERFECT=False.
    raise NotImplementedError("solve is not implemented yet")
