import json
from zipfile import ZipFile
from tools.export_students import export_students


def test_export_excludes_private_material_and_notebook_outputs(tmp_path):
    output = export_students(tmp_path / "students.zip")
    with ZipFile(output) as archive:
        names = archive.namelist()
        assert any(name.endswith("uv.lock") for name in names)
        assert not any("instructor" in name or "solutions" in name for name in names)
        assert not any(".venv" in name or "__pycache__" in name for name in names)
        for name in names:
            if name.endswith(".ipynb"):
                notebook = json.loads(archive.read(name))
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        assert cell["outputs"] == []
                        assert cell["execution_count"] is None
