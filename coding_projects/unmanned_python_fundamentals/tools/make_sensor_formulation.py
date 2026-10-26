"""Draw the sensor-frame problem and embed it in the Monday notebook."""
import base64
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
WORLD, BODY, SENSOR = "#475569", "#1d4ed8", "#087f5b"


def draw() -> None:
    """Save PNG/SVG diagrams with geometry and the coordinate-conversion chain."""
    fig = plt.figure(figsize=(16, 11), facecolor="white")
    fig.text(.045, .95, "Sensor reading → world position", fontsize=28, weight="bold")
    fig.text(.045, .91, "Find the world coordinates of P. The physical point stays fixed; its coordinates change.", fontsize=16)
    ax = fig.add_axes([.045, .32, .55, .54])
    ax.set(xlim=(-.5, 4.5), ylim=(-.5, 3.2), aspect="equal")
    ax.axis("off")

    def arrow(start, end, color, dashed=False):
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(
            arrowstyle="-|>", color=color, lw=2.5,
            linestyle="--" if dashed else "-", mutation_scale=19))

    # Frame axes: world east/north, body north/west, sensor west/south.
    for start, end, color in [
        ((0, 0), (4.1, 0), WORLD), ((0, 0), (0, 2.9), WORLD),
        ((3, 1), (3, 1.65), BODY), ((3, 1), (2.25, 1), BODY),
        ((3, 2), (2.3, 2), SENSOR), ((3, 2), (3, 1.65), SENSOR),
    ]:
        arrow(start, end, color)
    ax.text(4.1, -.18, "$x_W$ east", ha="right", fontsize=14, color=WORLD)
    ax.text(.1, 2.9, "$y_W$ north", fontsize=14, color=WORLD)
    ax.text(-.12, -.3, "W: (0, 0)", fontsize=13, color=WORLD)
    ax.text(3.12, 1.35, "$x_B$ forward", fontsize=14, color=BODY)
    ax.text(2.05, 1.12, "$y_B$ left", fontsize=14, color=BODY)
    ax.text(2.45, 2.13, "$x_S$", fontsize=15, color=SENSOR)
    ax.text(2.7, 1.66, "$y_S$", fontsize=15, color=SENSOR)
    ax.text(3.2, .8, "B: robot origin\nworld (3, 1)", fontsize=14, color=BODY)
    ax.text(3.2, 2.05, "S: sensor origin\nworld (3, 2)", fontsize=14, color=SENSOR)
    ax.scatter([0, 3, 3], [0, 1, 2], c=[WORLD, BODY, SENSOR], s=45, zorder=5)

    # Head-to-tail displacements terminate at the single measured point.
    arrow((0, 0), (3, 1), BODY, dashed=True)
    ax.text(1.05, .12, "$t^W_B=(3,1)$", fontsize=17, color=BODY)
    ax.plot([3, 3], [1, 2], color=BODY, alpha=.25, lw=8, zorder=0)
    ax.text(3.2, 1.75, "1 m mount", fontsize=13, color=BODY)
    arrow((3, 2), (1, 2), SENSOR, dashed=True)
    ax.text(1.3, 2.16, "2 m along sensor X", fontsize=14, color=SENSOR)
    ax.plot(1, 2, "o", color="#111827", ms=10)
    ax.text(.45, 2.6, "Point P", fontsize=18, weight="bold")
    ax.text(.4, 2.36, "world (1, 2)", fontsize=14)
    ax.plot([1, 1], [0, 2], ":", color="#cbd5e1", zorder=0)
    ax.plot([0, 1], [2, 2], ":", color="#cbd5e1", zorder=0)
    ax.text(1, -.18, "1", ha="center", fontsize=12)
    ax.text(-.16, 2, "2", va="center", fontsize=12)

    # Keep givens away from the geometry, at a readable size.
    x = .64
    for y, heading, detail, equation, color in [
        (.83, "GIVEN · Robot pose in world", "Position (3, 1); heading 90° (north).", "$t^W_B=(3,1),\\quad R^W_B=R(90^\\circ)$", BODY),
        (.67, "GIVEN · Sensor mount on robot", "1 m forward; turned 90° left of body.", "$t^B_S=(1,0),\\quad R^B_S=R(90^\\circ)$", SENSOR),
        (.51, "GIVEN · Sensor measurement", "Point is 2 m along sensor X.", "$p^S=(2,0)$", SENSOR),
    ]:
        fig.text(x, y, heading, fontsize=17, color=color, weight="bold")
        fig.text(x, y-.04, detail, fontsize=14)
        fig.text(x, y-.085, equation, fontsize=18, color=color)
    fig.text(x, .33, "FIND  $p^W$", fontsize=22, weight="bold")

    fig.text(.045, .275, "Coordinate conversion · apply the rightmost transform first", fontsize=18, weight="bold")
    cards = [(.045, "SENSOR S", "$p^S=(2,0)$", SENSOR),
             (.375, "BODY B", "$p^B=(1,2)$", BODY),
             (.705, "WORLD W", "$p^W=(1,2)$", WORLD)]
    for left, title, equation, color in cards:
        fig.add_artist(FancyBboxPatch((left, .10), .25, .125, transform=fig.transFigure,
                       boxstyle="round,pad=0.008", facecolor="#f8fafc", edgecolor=color, lw=2))
        fig.text(left+.015, .192, title, fontsize=15, color=color, weight="bold")
        fig.text(left+.015, .137, equation, fontsize=22, color=color)
    for left, label in [(.30, "$R^B_S,\\ t^B_S$"), (.63, "$R^W_B,\\ t^W_B$")]:
        fig.text(left+.027, .205, label, fontsize=15, ha="center")
        fig.text(left+.027, .147, "→", fontsize=32, ha="center")
    fig.text(.045, .045, "Each step: rotate the coordinates, then add the destination-frame offset. All distances are in meters.", fontsize=15)
    out = ROOT / "lecture_01/assets"
    out.mkdir(exist_ok=True)
    for suffix in ("png", "svg"):
        fig.savefig(out / f"sensor_problem_formulation.{suffix}", dpi=160)
    plt.close(fig)


def embed() -> None:
    """Attach the diagram so it travels with the notebook."""
    path = ROOT / "lecture_01/lecture_01_python_rotations.ipynb"
    notebook = json.loads(path.read_text())
    name = "sensor_problem_formulation.png"
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        if "### Optional: add a sensor frame" not in source:
            continue
        link = f"![Sensor, body, and world frames with the known poses, mounting offset, and measured point P.](attachment:{name})"
        if f"attachment:{name}" not in source:
            source = source.replace("### Optional: add a sensor frame\n", "### Optional: add a sensor frame\n\n" + link + "\n")
            cell["source"] = source.splitlines(keepends=True)
        cell.setdefault("attachments", {})[name] = {
            "image/png": base64.b64encode((ROOT / "lecture_01/assets" / name).read_bytes()).decode()
        }
        break
    else:
        raise ValueError("Sensor-frame section was not found")
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    draw()
    embed()
