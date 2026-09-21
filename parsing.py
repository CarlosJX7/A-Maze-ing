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
THEME=Hedge
ANIMATE=False

"""

import sys
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0)]
NegativeInt = Annotated[int, Field(gt=0)]

class Config(BaseModel):
    width: int = Field(..., gt=0)
    height: PositiveInt
    entry: tuple[PositiveInt, PositiveInt] = Field(...)
    exit_p: tuple[PositiveInt, PositiveInt] = Field(...)
    output_file: str
    perfect: bool
    algorith: str
    show_path: bool
    theme: str
    animate: bool

    @staticmethod
    def open_file(path: str) -> dict[str, str]:
        new_dict = {}
        with open(path, "r", encoding="utf-8") as file:
            params = {}
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                key, sep, value = line.partition("=")
                params[key] = value
            for key, value in params.items():
                key = key.lower()
                match key:
                    case "entry":
                        values = value.split(",")
                        print(values)
                        exit()
                new_dict[key] = value
        return new_dict

    @staticmethod
    def parse_input(input: dict[str, str]):
        new = Config.model_validate(input)
        print(new)

