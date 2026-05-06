import argparse
import sys

from PyQt6.QtWidgets import QApplication

from src.core.exception import ConfigFileError, GraphError, PathfindingError
from src.core.graph import Graph
from src.gui.main_window import MainWindow
from src.io.map_loader import MapLoader
from src.pathfinding.pathfinding import Pathfinding


def main():
    try:
        parser = argparse.ArgumentParser(description="Fly-in")
        parser.add_argument('--map', type=str,
                            default='maps/medium/03_priority_puzzle.txt')
        args = parser.parse_args()

        map_loader = MapLoader(args.map)
        map_loader.parse()
        zones = map_loader.zones
        connections = map_loader.connections
        nb_drone = map_loader.nb_drones

        graph = Graph(zones, connections)
        pathfinding = Pathfinding(graph)
        path = pathfinding.space_time_a_star()
        for _ in path:
            print(_)

        app = QApplication([])
        window = MainWindow(graph)
        window.show()
        app.exec()

    except ConfigFileError as e:
        print(f"ConfigFileError: {e}", file=sys.stderr)
        sys.exit(1)
    except GraphError as e:
        print(f"GraphError: {e}", file=sys.stderr)
        sys.exit(1)
    except PathfindingError as e:
        print(f"PathfindingError: {e}", file=sys.stderr)
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
