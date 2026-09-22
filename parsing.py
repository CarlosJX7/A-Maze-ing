"""
# Default A-Maze-ing configuration
WIDTH=13
HEIGHT=9
ENTRY=0,0
EXIT=12,8
OUTPUT_FILE=maze.txt
PERFECT=True
ALGORITHM=dfs
SHOW_PATH=False
THEME=Hedge #optional
ANIMATE=False #optional

"""

from enum import Enum
from pydantic import BaseModel, model_validator, Field

class ValidParams(str, Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"

import sys
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0)]
NegativeInt = Annotated[int, Field(gt=0)]

class Config(BaseModel):
    width: int = Field(..., gt=0)
    height: PositiveInt
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
    def validate_args(self):
        entry_x, entry_y = self.entry
        if entry_x >= self.width or entry_y >= self.height:
            raise ValueError("Entry points outside the limits")
        return self

    @staticmethod
    def open_file(path: str) -> dict[str, str]:
        new_dict = {}
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
                    raise ValueError(f"Error in sign input. Line {line_counter}")
                try:
                    key = ValidParams[p_key]
                except ValueError:
                    raise ValueError(f"Error: key '{p_key}' not found")
                params[key] = value
            for key, value in params.items():
                match key:
                    case "entry" | "exit":
                        value = value.split(",")
                        value = (value[0], value[1])
                match value:
                    case "False":
                        value = False
                    case "True":
                        value = True
                new_dict[key] = value
        return new_dict

    @staticmethod
    def parse_input(input: dict[str, str]):
        try:
            new = Config.model_validate(input)
        except ValueError as e:
            print(e)
            return
        print(new)
