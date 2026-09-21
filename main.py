from parsing import Config
import sys


if __name__ == "__main__":
    path = sys.argv[1]
    params = Config.open_file(path)
    parsed = Config.parse_input(params)
    print(parsed)