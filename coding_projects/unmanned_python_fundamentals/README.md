# Python fundamentals for robotics

A lecture on Python basics and 2D rotations using a simple non-holonomic model:

- **Monday:** Python basics and 2D rotations in Jupyter.

Each class ends with 25 minutes of independent coding without AI. All exercises are completed in class; no additional homework.

## Installation

You need VS Code with the **Python** and **Jupyter** extensions, internet access for setup, and basic vector/trigonometry knowledge. uv installs Python and the dependencies.

### 1. Install uv

macOS / Linux:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal and run `uv --version`. See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) if needed.

### 2. Get the files

Replace `REPOSITORY_URL` with the URL from your instructor:

```sh
git clone https://github.com/jn89b/unmanned_python_fundamentals.git
cd unmanned_python_fundamentals
```

You can also extract the repository or student ZIP. Open a terminal in the folder containing `pyproject.toml`.

### 3. Install dependencies

```sh
uv sync --locked
```

This creates `.venv` using Python **3.12.12** and the versions in `uv.lock`. No environment activation is needed. Keep `.python-version`, `pyproject.toml`, and `uv.lock` together.

### 4. Check the installation

```sh
uv run --locked python -c "import numpy, matplotlib, ipykernel; print('Workshop environment ready')"
```

You should see `Workshop environment ready`. Next, open the Monday notebook below.

## Monday: notebook

1. Open the repository folder in VS Code.
2. Run **Python: Select Interpreter** and choose `.venv`.
3. Open `lecture_01/lecture_01_python_rotations.ipynb`.
4. Choose **Select Kernel → Python Environments → .venv**.
5. Run the cells in order.

The interpreter is `.venv/bin/python` on macOS/Linux or `.venv\Scripts\python.exe` on Windows. Restart the kernel and run all cells to check for out-of-order execution errors.

For a browser notebook, run `uv run --locked jupyter lab`. Stop it with Ctrl+C.

<!-- Week 2 is hidden until release.
## Wednesday: simulator

Run these commands from the repository root:

```sh
uv run --locked python -m lecture_02.demo
uv run --locked python -m lecture_02.main
```

`demo` shows holonomic motion and works before you complete the challenge. `main` is the challenge starter; complete its TODOs using [the worksheet](lecture_02/WORKSHEET.md). Add `--output artifacts/waypoints.png` to save a plot. Use the module commands above or the included VS Code debug configurations.

The lesson focuses on tracing one pose update, composition, and loops. The controller and plotting are supplied. Inheritance and the unicycle comparison are optional; run `uv run --locked python -m lecture_02.demo --compare` to see both models.

-->

During challenges, disable AI chat and completions. Notes, the [quick reference](python_quick_reference.md), and official Python/NumPy documentation are allowed.

## Model and units

The rotation examples use a planar model with world and body coordinate frames.

| Quantity | Convention |
|---|---|
| World axes | X east/right, Y north/up |
| Body axes | X forward, Y left |
| Yaw | Counterclockwise from world X, in radians |
| Position | m |

<!-- Week 2 model notes:
The quadcopter moves at constant altitude and follows velocity commands instantly. The model omits roll, pitch, thrust, motors, and aerodynamic forces.
Velocity is measured in m/s, time in seconds, and yaw rate in rad/s.
The holonomic model allows lateral motion. The optional unicycle comparison sets lateral velocity to zero; this is an imposed constraint.
-->

## Checks and student export

From the full repository:

```sh
uv run --locked pytest tests/test_rotation.py
uv run --locked python tools/check_notebooks.py
uv run --locked python tools/export_students.py
```

The notebook check leaves source outputs unchanged. The export creates `dist/robotics_python_workshop_students.zip` without instructor files, tests, caches, plots, or notebook outputs. For a student ZIP installation, use the installation check above to check setup.

**Keep solutions private.** Git ignores every `instructor/` folder, and the student export excludes them. Do not force-add them or share a ZIP of the entire workspace. Before posting, check `git ls-files` for instructor paths; ignored files already tracked by Git would still be included. Keep instructor backups separately.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv` not found | Restart the terminal; check the installer's PATH instructions. |
| Import error in VS Code | Select `.venv` for both interpreter and kernel; run `uv sync --locked`. |
| Download failure | Check your connection or institutional proxy, then retry sync. |
| Unrelated `VIRTUAL_ENV` warning | Deactivate the other environment. uv uses the local `.venv`. |

Keep dependency versions fixed during class. To update them later, run `uv lock --upgrade`, test, and commit the lockfile. See [uv's sync documentation](https://docs.astral.sh/uv/concepts/projects/sync/).
