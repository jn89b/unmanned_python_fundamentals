"""Export only student material. Never archive the entire working tree."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def student_files(root=ROOT):
    names = ["README.md", "python_quick_reference.md", "pyproject.toml",
             "uv.lock", ".python-version", ".gitignore",
             ".vscode/settings.json", ".vscode/launch.json",
             "lecture_01/lecture_01_python_rotations.ipynb",
             "lecture_02/WORKSHEET.md", "tools/check_notebooks.py",
             "tools/export_students.py"]
    paths = [root / name for name in names]
    # Only immediate teaching modules; no recursive traversal into solutions.
    paths.extend(sorted((root / "lecture_02").glob("*.py")))
    return paths


def export_students(output=None):
    output = Path(output) if output else ROOT / "dist/robotics_python_workshop_students.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in student_files():
            relative = path.relative_to(ROOT)
            if "instructor" in relative.parts:
                raise ValueError(f"Private path in export: {relative}")
            data = path.read_bytes()
            if path.suffix == ".ipynb":
                notebook = json.loads(data)
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        cell["outputs"] = []
                        cell["execution_count"] = None
                data = (json.dumps(notebook, indent=1) + "\n").encode()
            archive.writestr(str(Path("robotics_python_workshop") / relative), data)
    return output


if __name__ == "__main__":
    print(export_students())
