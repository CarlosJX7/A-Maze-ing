from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated


PositiveInt = Annotated[int, Field(gt=0)]
NegativeInt = Annotated[int, Field(gt=0)]


class ValidParams(str, Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit_p"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"


class Config(BaseModel):
    width: int = Field(..., gt=0)
    height: PositiveInt = Field(...)
    entry: tuple[int, int] = Field(...)
    exit: tuple[int, int] = Field(...)
    output_file: str = Field(...)
    perfect: bool = Field(...)
    # Optionals
    algorithm: str | None = None
    show_path: bool | None = None
    theme: str | None = None
    animate: bool | None = None

    @model_validator(mode="after")
    def validate_args(self) -> "Config":
        entry_x, entry_y = self.entry
        if entry_x >= self.width or entry_y >= self.height:
            raise ValidationError("Entry points outside the limits")
        exit_x, exit_y = self.exit
        if exit_x >= self.width or exit_y >= self.height:
            raise ValidationError("Exit points outside the limits")
        if self.exit == self.entry:
            raise ValidationError("Exit point can't be the same as the entry")
        return self

    @staticmethod
    def open_file(path: str):
        line_counter = 0
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line_counter += 1
                line = line.strip()
                if line.startswith("#"):
                    continue
                key, sep, value = line.partition("=")
                if not sep:
                    raise ValueError(
                        f"Error in sign input. Line {line_counter}"
                        )
                if not key.strip().lower() in Config.model_fields:
                    raise ValueError(f"Error: key '{key}' not found")
            print(line)
        exit()

    @staticmethod
    def parse_input(input: dict[str, str | bool]) -> "Config":
        try:
            new = Config.model_validate(input)
        except:
            raise ValidationError()
        return new
