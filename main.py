import argparse
import sys

from PyQt6.QtWidgets import QApplication

from src.core.exception import ConfigFileError
from src.core.graph import Graph
from src.gui.main_window import MainWindow
from src.io.map_loader import MapLoader


def main():
    try:
        parser = argparse.ArgumentParser(description="Fly-in")
        parser.add_argument('--map', type=str,
                            default='maps/medium/03_priority_puzzle.txt')
        args = parser.parse_args()

        map_loader = MapLoader(args.map)
        map_loader.parse()

        graph = Graph(map_loader.zones, map_loader.connections)

        app = QApplication([])
        window = MainWindow(graph)

        window.show()
        app.exec()


    except ConfigFileError as e:
        print(f"ConfigFileError: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("FileNotFoundError: "
              f"no such file or directory '{args.map}'", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"PermissionError: '{args.map}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
