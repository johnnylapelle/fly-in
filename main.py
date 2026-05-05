import argparse
import sys

from PyQt6.QtWidgets import QApplication

from src.core.exception import ConfigFileError
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

        came_from, cost_so_far = pathfinding.dijkstra_search(graph.end, graph.start)
        print("came_from")
        for key, value in came_from.items():
            print(f"{key}: {value}")

        print("\ncost_so_far")
        for key, value in cost_so_far.items():
            print(f"{key}: {value}")

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
