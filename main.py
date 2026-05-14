import argparse
import sys
import traceback

import PyQt6
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QTimeEdit

from src.core.exception import ConfigFileError, GraphError, PathfindingError
from src.gui.main_window import MainWindow


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Fly-in")
        parser.add_argument('--map', type=str,
                            default=None)
        parser.add_argument('--debug', action="store_true",
                            default=False)
        args = parser.parse_args()

        app = QApplication([])

        # font = QFont("Cantarell", 10)
        # app.setFont(font)

        window = MainWindow(map_path=args.map,
                            debug=args.debug)
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
    except FileNotFoundError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        print(f"Error: {e}.", file=sys.stderr)
        print(f"In {tb.name}, line {tb.lineno} in {tb.filename}.")
        sys.exit(1)


if __name__ == "__main__":
    main()
