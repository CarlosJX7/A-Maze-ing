"""A-Maze-ing entry point.

Usage:
    python3 a_maze_ing.py <config_file>
"""

from parsing import Config, ConfigError
import sys


def main() -> int:
    """Read the config file given as argument and run the program.

    Errors are printed to stderr instead of raising.

    Returns:
        The exit status: 0 on success, 1 on error.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        return 1
    try:
        params = Config.open_file(sys.argv[1])
        config = Config.parse_input(params)
    except ConfigError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
