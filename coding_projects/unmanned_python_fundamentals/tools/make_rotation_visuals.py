"""Draw the coordinate diagrams embedded in the Monday notebook."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np

OUT = Path(__file__).resolve().parents[1] / 'lecture_01' / 'assets'
BLUE, ORANGE, GREEN = '#1769aa', '#bf5700', '#147d50'
plt.rcParams.update({'font.size': 11, 'axes.titlesize': 13, 'figure.facecolor': 'white'})


def axes(ax, xlim, ylim):
    ax.set(xlim=xlim, ylim=ylim, xlabel='World X', ylabel='World Y')
    ax.set_aspect('equal')
    ax.axhline(0, color='#889099', linewidth=1)
    ax.axvline(0, color='#889099', linewidth=1)
    ax.grid(alpha=0.15)
    ax.spines[['top', 'right']].set_visible(False)


def arrow(ax, end, color, start=(0, 0), **kwargs):
    start, end = np.array(start), np.array(end)
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=2.5, mutation_scale=15, **kwargs))


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=170, bbox_inches='tight')
    plt.close(fig)


def draw():
    theta = np.deg2rad(35)
    c, s = np.cos(theta), np.sin(theta)
    ex, ey = np.array([c, s]), np.array([-s, c])
    fig, axs = plt.subplots(1, 2, figsize=(11, 5), layout='constrained')
    for ax in axs:
        axes(ax, (-1.2, 1.3), (-0.4, 1.4))
        arrow(ax, ex, BLUE)
        arrow(ax, ey, ORANGE)
        ax.text(0.86, 0.66, 'Body X\nforward', color=BLUE, fontsize=10)
        ax.text(-0.88, 0.99, 'Body Y\nleft', color=ORANGE, fontsize=10)
        ax.plot(0, 0, 'ko', ms=4)
    ax = axs[0]
    ax.set_title('1. Project the forward unit vector')
    ax.plot([c, c], [0, s], '--', color=BLUE, alpha=0.7)
    ax.plot([0, c], [s, s], '--', color=BLUE, alpha=0.7)
    ax.text(c / 2, -0.15, r'$\cos\theta$', ha='center', color=BLUE)
    ax.text(-0.08, s, r'$\sin\theta$', ha='right', color=BLUE)
    ax.add_patch(Arc((0, 0), 0.7, 0.7, theta1=0, theta2=35, color=BLUE))
    ax.text(0.4, 0.1, r'$\theta$', color=BLUE)
    ax = axs[1]
    ax.set_title('2. Turn another 90° to get the left unit vector')
    ax.plot([-s, -s], [0, c], '--', color=ORANGE, alpha=0.7)
    ax.plot([-s, 0], [c, c], '--', color=ORANGE, alpha=0.7)
    ax.text(-s / 2, -0.15, r'$-\sin\theta$', ha='center', color=ORANGE)
    ax.text(0.08, c, r'$\cos\theta$', color=ORANGE)
    ax.add_patch(Arc((0, 0), 0.7, 0.7, theta1=35, theta2=125, color=ORANGE))
    ax.text(-0.04, 0.44, '90°', color=ORANGE)
    fig.suptitle('Same origin, different axes  •  yaw = 35° counterclockwise', fontsize=15)
    save(fig, 'rotation_basis.png')

    a, b = 2 * ex, ey
    p = a + b
    t = np.array([3., 1.])
    fig, axs = plt.subplots(1, 2, figsize=(11, 5), layout='constrained')
    ax = axs[0]
    axes(ax, (-0.9, 2.5), (-0.5, 2.9))
    arrow(ax, a, BLUE)
    arrow(ax, p, ORANGE, start=a)
    arrow(ax, p, GREEN)
    ax.plot([0, b[0], p[0]], [0, b[1], p[1]], '--', color='#999999')
    ax.text(1.3, 0.5, '2 × forward', color=BLUE)
    ax.text(1.63, 1.65, '1 × left', color=ORANGE)
    ax.text(0.1, 2.22, f'World: ({p[0]:.2f}, {p[1]:.2f})', color=GREEN)
    ax.set_title('3. Body point (2, 1): scale and add the columns')
    ax = axs[1]
    axes(ax, (-0.4, 5.4), (-0.4, 4.2))
    arrow(ax, t, '#666666')
    arrow(ax, t+p, GREEN, start=t)
    arrow(ax, t+1.1*ex, BLUE, start=t)
    arrow(ax, t+1.1*ey, ORANGE, start=t)
    ax.plot(*t, 'ko')
    ax.text(1.05, 0.25, 'Robot position t = (3, 1)', fontsize=10)
    ax.text(3.2, 0.65, 'Robot origin', fontsize=10)
    ax.plot(*(t+p), 'o', color=GREEN)
    ax.text(1.6, 3.55, f'World point = ({(t+p)[0]:.2f}, {(t+p)[1]:.2f})', color=GREEN)
    ax.set_title('4. For a point, also add the robot position')
    fig.suptitle('Rotation changes direction; translation changes the origin', fontsize=15)
    save(fig, 'rotation_sum_translation.png')

    fig, axs = plt.subplots(1, 2, figsize=(11, 5), layout='constrained')
    ax = axs[0]
    axes(ax, (-1.3, 1.5), (-0.4, 1.5))
    q = np.linspace(0, np.pi / 2, 100)
    ax.plot(np.cos(q), np.sin(q), color=GREEN, lw=3)
    arrow(ax, [1, 0], BLUE)
    arrow(ax, [0, 1], BLUE)
    ax.text(0.72, 0.9, r'arc length $s=\pi/2$', color=GREEN)
    ax.text(0.55, -0.2, 'radius r = 1', ha='center')
    ax.text(-1.1, 1.22, r'$\theta=s/r=\pi/2$ rad', fontsize=13)
    ax.set_title('5. Radians measure arc length ÷ radius')
    ax = axs[1]
    axes(ax, (-1.3, 1.5), (-0.4, 1.5))
    wrong = np.array([np.cos(90), np.sin(90)])
    arc = np.linspace(0, np.pi, 120)
    ax.plot(np.cos(arc), np.sin(arc), color='#dddddd')
    arrow(ax, [0, 1], GREEN)
    arrow(ax, wrong, ORANGE)
    ax.text(0.1, 1.12, '90° → π/2 rad\n(0, 1)', color=GREEN)
    ax.text(-1.2, 0.49, '90 rad\n(−0.45, 0.89)', color=ORANGE)
    ax.text(-1.15, -0.28, 'Both have length 1. Only one points north.', fontsize=10)
    ax.set_title('6. NumPy reads 90 as radians, not degrees')
    save(fig, 'rotation_units.png')


def draw_frame_chain():
    fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
    axes(ax, (-0.5, 4.5), (-0.5, 3.2))
    ax.set(xlabel='World X (m)', ylabel='World Y (m)',
           title='One point, three frames: sensor → body → world')
    robot = np.array([3., 1.])
    sensor = np.array([3., 2.])
    point = np.array([1., 2.])
    arrow(ax, robot, '#666666')
    arrow(ax, sensor, BLUE, start=robot)
    arrow(ax, point, GREEN, start=sensor)
    arrow(ax, robot + [-0.65, 0], ORANGE, start=robot)
    arrow(ax, sensor + [0, -0.55], ORANGE, start=sensor)
    for xy in [robot, sensor, point]:
        ax.plot(*xy, 'ko', ms=5)
    ax.text(1.4, 0.25, 'Body origin: (3, 1)', fontsize=11)
    ax.text(3.15, 1.15, 'Body X / forward', color=BLUE, fontsize=10)
    ax.text(1.8, 0.8, 'Body Y / left', color=ORANGE, fontsize=10)
    ax.text(3.15, 2.15, 'Sensor origin\n(3, 2)', fontsize=10)
    ax.text(1.5, 2.15, 'Sensor X: 2 m', color=GREEN, fontsize=10)
    ax.text(3.15, 1.65, 'Sensor Y', color=ORANGE, fontsize=10)
    ax.text(0.0, 2.35, 'Point in world: (1, 2)', fontsize=11)
    ax.text(0.0, 2.95, 'Body yaw: 90°   |   Sensor yaw relative to body: 90°', fontsize=10)
    save(fig, 'frame_chain.png')


if __name__ == '__main__':
    draw()
    draw_frame_chain()
    print(f'Figures saved to {OUT}')
