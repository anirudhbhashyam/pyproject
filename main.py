import sys
import argparse
from pathlib import Path

sys.path.append(str(Path("src").resolve()))

from project import Project

CWD = Path.cwd()

def process_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Create a new project."
    )
    parser.add_argument(
        "name",
        help = "Name of the project that is to be created."
    )
    parser.add_argument(
        "-p",
        "--path",
        help = "Absolute path to where project must be created. PWD by default.",
        default = CWD,
    )
    return parser.parse_args()

def main() -> None:
    args = process_args()
    p = Project(
        name = args.name,
        path = args.path
    )

    p.create_project()

if __name__ == "__main__":
    main()