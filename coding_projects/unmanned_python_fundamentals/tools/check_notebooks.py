"""Validate and execute fresh notebook copies without changing source outputs."""
import argparse
import os
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-instructor", action="store_true")
    args = parser.parse_args()
    os.environ.setdefault("MPLBACKEND", "Agg")
    paths = [ROOT / "lecture_01/lecture_01_python_rotations.ipynb"]
    if args.include_instructor:
        paths.append(ROOT / "lecture_01/instructor/lecture_01_solutions.ipynb")
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        NotebookClient(notebook, timeout=120, kernel_name="python3",
                       resources={"metadata": {"path": str(ROOT)}}).execute()
        print(f"Validated and executed: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
