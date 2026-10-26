# Python robotics quick reference

Permitted during the independent challenges. Units: position m, time s, body velocity m/s, yaw rad, yaw rate rad/s. World X east, world Y north, body X forward, body Y left; positive yaw is counterclockwise.

| Idea | Syntax / meaning |
|---|---|
| Assignment | `dt = 0.1`; names refer to values |
| Basic types | `3` int, `3.0` float, `"quad"` str, `True` bool, `None` no value |
| List | `headings = [0, 90, 180]`; mutable; `.append(value)` |
| Tuple | `waypoint = (2.0, 1.0)`; cannot replace an element |
| Array | `velocity = np.array([1.0, 0.5])`; numeric operations |
| Index | `velocity[0]` first, `velocity[-1]` last; `a[0:2]` excludes index 2 |
| Matrix columns | `points[:, 0]` selects all rows, first column |
| Import | `import numpy as np`; `from lecture_02.pose import Pose2D` |
| Convert angle | `np.deg2rad(degrees)`; `np.rad2deg(radians)` |
| Trigonometry | `np.sin(theta)`, `np.cos(theta)` expect radians |
| Multiply | `A @ v` matrix product; `A * B` elementwise for arrays |
| Compare | `==`, `!=`, `<`, `<=`, `>`, `>=`; combine using `and`, `or`, `not` |
| Approximate check | `np.isclose(a, b)` for scalars; `np.allclose(a, b)` for arrays |
| Length of vector | `np.linalg.norm(vector)` |
| Inverse rotation | `R.T` is transpose; for a rotation it equals its inverse |
| Frame notation | $R^{W}_{B}$ converts body to world; superscript = destination, subscript = source |
| Rotation chain | $R^{W}_{S}=R^{W}_{B}R^{B}_{S}$; apply the rightmost rotation first |
| Debug | Read last traceback line, locate your file/line, inspect values/shapes |

Parameters are names in a function definition; arguments are values passed to it. Variables inside the function are local. `return` sends a value back; `print` displays it.

```python
def elapsed_time(steps, dt):
    duration = steps * dt
    return duration

seconds = elapsed_time(10, 0.1)
```

Use conditionals to choose branches; indentation matters:

```python
if battery_fraction < 0.2:
    print("Land soon")
elif battery_fraction < 0.5:
    print("Monitor battery")
else:
    print("Continue")
```

`for` visits each item; `range(n)` gives 0 through n−1. `while` repeats while a condition is true. Update the condition variables and limit simulation steps. Interrupt a loop that will not stop.

```python
for heading in [0, 90, 180]:
    print(heading)

sample = 0
while sample < 3:
    print(sample)
    sample += 1
```

A class defines data and methods. `__init__` initializes an instance; `self` refers to it. Attributes store state. Composition means **has a**: Robot contains a pose and a motion model; Simulator contains a Robot.

```python
class Pose2D:
    def __init__(self, x, y, yaw):
        self.x = x
        self.y = y
        self.yaw = yaw

pose = Pose2D(0.0, 0.0, 0.0)
print(pose.x)
```

For plotting: `fig, ax = plt.subplots()`, `ax.plot(xs, ys, "o-")`, `ax.set_aspect("equal")`, `ax.set(xlabel="X (m)", ylabel="Y (m)")`, `plt.show()`.

Common errors: `NameError` (name/scope), `IndexError` (index outside sequence), `TypeError` (wrong kind of argument), `ValueError` (invalid value/shape), `AttributeError` (missing attribute), `IndentationError` (block structure). Also check units, signs, and expected results; incorrect code may run without errors.

Official references: [Python tutorial](https://docs.python.org/3.12/tutorial/), [NumPy beginner guide](https://numpy.org/doc/stable/user/absolute_beginners.html), [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html).

## Optional: inheritance

Not required for the Wednesday challenge. HolonomicModel **is a** MotionModel (inheritance). A subclass can override a method with its own implementation. Polymorphism lets Robot call the same `step` method on different model objects.
