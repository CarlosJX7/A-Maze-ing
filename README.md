*This project has been created as part of the 42 curriculum by carlinaq, danipere.*

<!--
TO DO BEFORE SUBMITTING (these comments are not rendered on GitHub; search this file for "TODO"):
- Controls: keys of the visual display.
- How it works: chosen algorithm and WHY it was chosen (required by the subject).
- Using mazegen as a library: usage example with the real API (required by the subject).
- Project management: roles, planning and retrospective (required by the subject).
- Optional keys: keep only the keys and values that actually exist.
- Preview: add a screenshot or a GIF.
-->

# A-Maze-ing

**Generate, solve and explore random mazes.** Every maze is reproducible from a seed,
exported in a compact hexadecimal format and hides a little "42" inside. The generator
is also available as a standalone Python library.

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-informational)
![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-informational)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

<!-- TODO: add a screenshot or a GIF of the maze here, e.g. ![Preview](docs/preview.gif) -->

## Description

A-Maze-ing reads a small configuration file, builds a random maze that matches it, saves it
to a file and shows it on screen so you can explore it.

### Features

- **Random but reproducible.** The same configuration and the same seed always give the same maze.
- **Perfect or imperfect mazes.** With `PERFECT=True` there is exactly one path between any two
  cells; with `PERFECT=False` the maze can contain loops.
- **Always valid.** Walls are coherent between neighbouring cells, the outer border is closed
  except at the entry and the exit, every cell is reachable, and there are no open areas wider
  than 2 cells.
- **A hidden "42".** Every maze contains a "42" drawn with fully closed cells (skipped, with a
  warning, when the maze is too small to fit it).
- **Solved for you.** The output file includes the shortest path from the entry to the exit.
- **Interactive display.** Regenerate the maze, show or hide the solution and change the wall colours.
- **Reusable.** The generator is packaged as `mazegen`, a library you can `pip install` in your
  own projects.
- **Friendly errors.** A missing file, a typo or an impossible value never crashes the program:
  you get a clear message telling you what is wrong.

## Instructions

### Requirements

- Python **3.10** or newer
- `make`

### Quick start

```bash
git clone https://github.com/CarlosJX7/A-Maze-ing.git
cd A-Maze-ing
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

### Usage

```bash
python3 a_maze_ing.py <config_file>
```

The only argument is the path to a configuration file. `config.txt` is the default one
shipped with the repository, and `make run` uses it.

<!--
TODO: controls section, once the visual display exists. For example:

### Controls

| Key | Action |
|---|---|
| `r` | Generate a new maze |
| `p` | Show / hide the shortest path |
| `c` | Change the wall colour |
| `q` | Quit |
-->

## Configuration

A configuration file has one `KEY=VALUE` pair per line. Lines starting with `#` are comments.

```ini
# Default A-Maze-ing configuration
WIDTH=13
HEIGHT=9
ENTRY=0,0
EXIT=12,8
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Mandatory keys

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width, in cells | `WIDTH=20` |
| `HEIGHT` | Maze height, in cells | `HEIGHT=15` |
| `ENTRY` | Entry cell, as `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit cell, as `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | File where the maze is saved | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a perfect maze (a single path), `False` to allow loops | `PERFECT=True` |

Coordinates start at `0,0` in the top-left corner. The entry and the exit must be inside the
maze and must be different cells.

### Optional keys

<!-- TODO: keep only the keys that actually exist, with their accepted values. -->

| Key | Description | Example |
|---|---|---|
| `SEED` | Seed for the random generator. Reuse it to get the exact same maze again | `SEED=42` |

Unknown keys are rejected, so a typo in a key name is reported instead of being silently ignored.

## Output file format

The maze is written row by row, **one hexadecimal digit per cell**. Each bit of the digit
tells whether a wall is closed (`1`) or open (`0`):

| Bit | Wall |
|---|---|
| 0 (least significant) | North |
| 1 | East |
| 2 | South |
| 3 | West |

For example, `3` (`0011`) is a cell with its North and East walls closed, `A` (`1010`) has its
East and West walls closed, and `F` (`1111`) is a fully closed cell, like the ones that draw
the "42".

After the maze come an empty line and three more lines:

```
<one line per row of the maze>

<entry coordinates>
<exit coordinates>
<shortest path from the entry to the exit, using N, E, S and W>
```

Every line, including the last one, ends with a newline.

<!--
TODO: algorithm section (required by the subject). For example:

## How it works

### Generation algorithm

Which algorithm is used, how it works (in a few lines) and WHY it was chosen over the others.
How a non-perfect maze is obtained with PERFECT=False.

### Finding the shortest path

How the shortest path is computed (e.g. BFS).
-->

## Using `mazegen` as a library

The maze generator lives in its own package, `mazegen`, so you can use it in other projects
without the rest of A-Maze-ing. It is distributed as a single file at the root of this
repository.

### Install

```bash
pip install ./mazegen-1.0.0-py3-none-any.whl
```

### Build it from source

```bash
pip install build
python3 -m build
```

The `.whl` and `.tar.gz` files are created in `dist/`.

<!--
TODO: usage example with the real API (required by the subject): how to create the generator,
how to pass parameters (size, seed...), how to access the maze structure and get a solution.
Also check that the name and version of the .whl match the pyproject.toml.

### Example

```python
from mazegen import MazeGenerator, solve

generator = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14),
                          perfect=True)
maze = generator.generate(seed=42)  # same seed -> same maze
print(maze.cells[0][0])             # closed walls of the top-left cell
path = solve(maze)                  # shortest path, e.g. "EESSE..."
```
-->

## Development

### Makefile rules

| Rule | Description |
|---|---|
| `make install` | Install the dependencies (run it inside the virtual environment) |
| `make run` | Run the program with `config.txt` |
| `make debug` | Run the program inside the Python debugger (`pdb`) |
| `make clean` | Remove `__pycache__` and `.mypy_cache` |
| `make lint` | Check the code style with `flake8` and the types with `mypy` |

### Project structure

<!-- TODO: add mazegen/ and pyproject.toml once they exist. -->

```
.
├── a_maze_ing.py      # Entry point
├── parsing.py         # Reads and validates the configuration file
├── config.txt         # Default configuration
├── requirements.txt   # Dependencies
├── Makefile
└── README.md
```

## Project management

<!--
TODO (required by the subject):

### Team and roles
- **carlinaq**: ...
- **danipere**: ...

### Planning
- Planned: ...
- How it actually went: ...

### What worked well and what could be improved
...
-->

### Tools

| Tool | Used for |
|---|---|
| Python 3 | The whole project |
| [pydantic](https://docs.pydantic.dev/latest/) | Validating the configuration file |
| flake8 and mypy | Code style and static type checking |
| pytest | Unit tests |
| build | Packaging `mazegen` |
| Make | Everyday tasks: install, run, debug, clean, lint |
| Git and GitHub | Version control |
| VS Code and Pylance | Editing and type hints |
| Claude Code | AI assistant (see [AI usage](#ai-usage)) |

## Resources

### Maze generation and solving

- [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm), Wikipedia
- [Maze-solving algorithm](https://en.wikipedia.org/wiki/Maze-solving_algorithm), Wikipedia
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search), Wikipedia:
  the classic way to find the shortest path in a grid
- [Maze Generation: Algorithm Recap](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap),
  Jamis Buck: interactive demos of the main generation algorithms
- [Mazes for Programmers](https://pragprog.com/titles/jbmaze/mazes-for-programmers/),
  Jamis Buck (book)

### Python

- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [pydantic documentation](https://docs.pydantic.dev/latest/)
- [random module](https://docs.python.org/3/library/random.html): seeds and reproducibility
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/),
  Python Packaging User Guide

### AI usage

An AI assistant (Claude Code) was used during development to:

- Set up the project tooling: `requirements.txt`, `.gitignore`, `.flake8` and the `Makefile`.
- Review the configuration parser against the subject, look for bugs and edge cases, and
  discuss the design of a refactor.
- Explain concepts such as pydantic models, `model_fields`, flake8 and mypy.

<!-- TODO: keep this up to date as the project grows: which parts you wrote yourselves and how you checked what the AI suggested. -->

## License

Released under the [MIT License](LICENSE).
