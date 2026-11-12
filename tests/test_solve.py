"""Tests for ``solve``, using the hand-made mazes of ``fake_mazes``."""

from collections.abc import Callable

import pytest

from mazegen import Maze, solve
from tests.fake_mazes import CASES, unreachable

SOLVABLE = [(build, path) for build, path in CASES if path is not None]


@pytest.mark.parametrize(
    "build, expected", SOLVABLE, ids=[b.__name__ for b, _ in SOLVABLE]
)
def test_shortest_path(build: Callable[[], Maze], expected: str) -> None:
    """``solve`` returns the shortest path of each fake maze."""
    assert solve(build()) == expected


def test_unreachable_exit_raises() -> None:
    """``solve`` raises ValueError when the exit cannot be reached."""
    with pytest.raises(ValueError):
        solve(unreachable())


def test_solve_does_not_change_the_maze() -> None:
    """``solve`` only reads the maze, it never opens or closes walls."""
    maze = CASES[2][0]()
    before = [row[:] for row in maze.cells]
    solve(maze)
    assert maze.cells == before
