import sys

from src.exception import ConfigFileError
from src.map_loader import MapLoader


def main():
    try:
        # print("Hello from github-fly-in!")
        # parser = Parser("maps/easy/01_linear_path.txt")
        parser = MapLoader("maps/easy/01_linear_path_testing.txt")
        # parser = Parser("maps/easy/02_simple_fork.txt")
        # parser = Parser("maps/hard/01_maze_nightmare.txt")
        parser.parse()

    except ConfigFileError as e:
        print(f"ConfigFileError: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
