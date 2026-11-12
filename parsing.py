"""Read and validate the A-Maze-ing configuration file.

The file contains one ``KEY=VALUE`` pair per line. Lines starting with
``#`` are comments. ``Config.open_file`` reads the raw text values and
``Config.parse_input`` converts and validates them.
"""

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ValidationError,
    field_validator,
    NonNegativeInt,
    PositiveInt
    )


class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""


class Config(BaseModel):
    """Validated maze configuration.

    Each field matches a key of the config file in lower case
    (``OUTPUT_FILE`` -> ``output_file``).

    Attributes:
        width: Maze width, in cells.
        height: Maze height, in cells.
        entry: Entry cell as ``(x, y)``.
        exit: Exit cell as ``(x, y)``.
        output_file: Path of the file where the maze is written.
        perfect: Whether the maze must have exactly one path between
            any two cells.
        seed: Seed for the random generator, to reproduce a maze.
        algorithm: Name of the generation algorithm.
        show_path: Whether to show the solution path at start.
        theme: Colour theme of the display.
        animate: Whether to animate the generation.
    """

    width: PositiveInt
    height: PositiveInt
    entry: tuple[NonNegativeInt, NonNegativeInt]
    exit: tuple[NonNegativeInt, NonNegativeInt]
    output_file: str = Field(min_length=1)
    perfect: bool
    # Optionals
    seed: int | None = None
    algorithm: str | None = None
    show_path: bool | None = None
    theme: str | None = None
    animate: bool | None = None

    @model_validator(mode="after")
    def validate_args(self) -> "Config":
        """Check that the entry and the exit are valid for this maze.

        Runs after every field has been validated.

        Returns:
            The validated config.

        Raises:
            ValueError: If the entry or the exit is outside the maze,
                or if they are the same cell.
        """
        entry_x, entry_y = self.entry
        if entry_x >= self.width or entry_y >= self.height:
            raise ValueError("Entry points outside the limits")
        exit_x, exit_y = self.exit
        if exit_x >= self.width or exit_y >= self.height:
            raise ValueError("Exit points outside the limits")
        if self.exit == self.entry:
            raise ValueError("Exit point can't be the same as the entry")
        return self

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def split_coords(cls, value: str) -> tuple[str, str]:
        """Split ``"x,y"`` into ``("x", "y")``.

        Runs before pydantic converts each coordinate to ``int``.

        Args:
            value: Raw coordinates from the config file.

        Returns:
            The two coordinates, still as text.

        Raises:
            ValueError: If there is no comma between the coordinates.
        """
        x_axis, sep, y_axis = value.partition(",")
        if not sep:
            raise ValueError(f"Invalid coordinates format: {value}")
        return (x_axis.strip(), y_axis.strip())

    @staticmethod
    def open_file(path: str) -> dict[str, str]:
        """Read the ``KEY=VALUE`` pairs of a config file.

        Blank lines and lines starting with ``#`` are skipped. Keys are
        stored in lower case; values are kept as text.

        Args:
            path: Path of the config file.

        Returns:
            The raw values, indexed by lower-case key.

        Raises:
            ConfigError: If the file cannot be read or is not a text
                file, or if a line has no ``=``, an unknown key or a
                repeated key.
        """
        line_counter = 0
        params: dict[str, str] = {}
        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    line_counter += 1
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, sep, value = line.partition("=")
                    if not sep:
                        raise ConfigError(
                            f"Line {line_counter}: expected KEY=VALUE"
                            )
                    key = key.strip().lower()
                    if key not in Config.model_fields:
                        raise ConfigError(
                            f"Line {line_counter}: "
                            f"key '{key.upper()}' not found."
                            )
                    if key in params:
                        raise ConfigError(
                            f"Line {line_counter}: "
                            f"Duplicate '{key.upper()}'"
                            )
                    params[key] = value.strip()
        except OSError as error:
            raise ConfigError(
                f"Cannot read '{path}': {error.strerror}"
                ) from error
        except UnicodeDecodeError as error:
            raise ConfigError(f"'{path}' is not a valid text file") from error
        return params

    @staticmethod
    def parse_input(input: dict[str, str]) -> "Config":
        """Convert and validate the raw values read by ``open_file``.

        Args:
            input: Raw values, indexed by lower-case key.

        Returns:
            The validated config.

        Raises:
            ConfigError: If any value is missing or invalid. The message
                has one line per problem.
        """
        try:
            new = Config.model_validate(input)
        except ValidationError as error:
            messages = []
            for item in error.errors():
                loc = item["loc"]
                location = str(loc[0] if loc else "CONFIG")
                messages.append(f"{location.upper()}: {item['msg']}")
            raise ConfigError("\n".join(messages)) from error
        return new
