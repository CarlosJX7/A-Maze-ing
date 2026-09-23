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
    exit_p: tuple[int, int] = Field(...)
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
        exit_x, exit_y = self.exit_p
        if exit_x >= self.width or exit_y >= self.height:
            raise ValidationError("Exit points outside the limits")
        if self.exit_p == self.entry:
            raise ValidationError("Exit point can't be the same as the entry")
        return self

    @staticmethod
    def open_file(path: str) -> dict[str, str | bool]:
        new_dict: dict[str, str | bool] = {}
        line_counter = 0
        with open(path, "r", encoding="utf-8") as file:
            params = {}
            for line in file:
                line_counter += 1
                line = line.strip()
                if line.startswith("#"):
                    continue
                p_key, sep, value = line.partition("=")
                if not sep:
                    raise ValueError(
                        f"Error in sign input. Line {line_counter}"
                        )
                # validar que exista la clave
                try:
                    key = ValidParams[p_key]
                except ValueError:
                    raise ValueError(f"Error: key '{p_key}' not found")
                params[key] = value
            for key, value in params.items():
                match key:
                    case "entry" | "exit_p":
                        value_splited = value.split(",")
                        value_tuple = (value_splited[0], value_splited[1])
                match value:
                    case "False":
                        new_dict[key] = False
                        continue
                    case "True":
                        new_dict[key] = True
                        continue
                new_dict[key] = value
        return new_dict

    @staticmethod
    def parse_input(input: dict[str, str | bool]) -> "Config":
        try:
            new = Config.model_validate(input)
        except:
            raise ValidationError()
        return new
