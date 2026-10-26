"""Create a slide diagram for the sensor/body/world example."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / 'lecture_01/assets'
WORLD, BODY, SENSOR = '#465461', '#1769aa', '#147d50'


def draw():
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    fig.text(.055, .93, 'One point. Three coordinate frames.', fontsize=29, weight='bold')
    fig.text(.055, .88, 'Sensor → body → world   |   Top view; all distances in meters', fontsize=17, color=WORLD)
    ax = fig.add_axes([.055, .18, .51, .65])
    ax.set(xlim=(-.35, 4.2), ylim=(-.3, 3), aspect='equal')
    ax.axis('off')

    def arrow(start, end, color, lw=2.7, style='-'):
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, linestyle=style, mutation_scale=19))

    # World frame and robot translation.
    arrow((0, 0), (3.95, 0), WORLD)
    arrow((0, 0), (0, 2.7), WORLD)
    ax.text(3.8, -.2, '$X_W$ / east', fontsize=14, ha='right', color=WORLD)
    ax.text(.1, 2.65, '$Y_W$ / north', fontsize=14, color=WORLD)
    ax.text(-.05, -.2, 'World origin', fontsize=12, color=WORLD)
    arrow((0, 0), (3, 1), WORLD, lw=1.8, style='--')
    ax.text(.9, .15, '$t^{W}_{B}=(3,1)$', fontsize=15, color=WORLD)

    # Stylized quadcopter at the body origin (3, 1).
    for dx, dy in [(-.28, -.28), (.28, .28), (-.28, .28), (.28, -.28)]:
        ax.plot([3, 3+dx], [1, 1+dy], color='#aebac5', lw=7, zorder=1)
        ax.add_patch(Circle((3+dx, 1+dy), .16, facecolor='#eef3f7', edgecolor='#9caab7', lw=2))
    ax.add_patch(FancyBboxPatch((2.9, .81), .2, .38,
                              boxstyle='round,pad=0.03', facecolor='#d8e8f5', edgecolor=BODY))
    # Mounting boom, body axes, sensor package.
    ax.plot([3, 3], [1.2, 2], color='#aebac5', lw=5, zorder=1)
    arrow((3, 1), (3, 1.65), BODY)
    arrow((3, 1), (2.3, 1), BODY)
    ax.text(3.12, 1.42, '$X_B$ forward', fontsize=13, color=BODY)
    ax.text(1.85, .82, '$Y_B$ left', fontsize=13, color=BODY)
    ax.text(3.45, .8, 'Body origin\n(3, 1)', fontsize=13, color=BODY)
    ax.text(3.12, 1.8, '1 m mount', fontsize=12, color=WORLD)
    ax.add_patch(Rectangle((2.9, 1.93), .2, .14, facecolor='#d8f0e6', edgecolor=SENSOR, lw=2))
    ax.text(3.1, 2.05, 'Sensor origin\n(3, 2)', fontsize=13, color=SENSOR)
    # Measurement and sensor axes.
    arrow((3, 2), (1, 2), SENSOR)
    arrow((3, 2), (3, 1.67), SENSOR, lw=2)
    ax.text(2.4, 1.72, '$Y_S$', fontsize=14, color=SENSOR)
    ax.text(1.5, 2.16, '$X_S$: point is 2 m ahead', fontsize=14, color=SENSOR)
    ax.plot(1, 2, 'o', color='#171e25', ms=10)
    ax.text(.45, 2.36, 'Measured point P\nWorld position (1, 2)', fontsize=14, weight='bold')
    ax.plot([1, 1], [0, 2], ':', color='#b9c1c8', zorder=0)
    ax.plot([0, 1], [2, 2], ':', color='#b9c1c8', zorder=0)
    ax.text(1, -.18, '1', ha='center', fontsize=12, color=WORLD)
    ax.text(-.13, 2, '2', va='center', fontsize=12, color=WORLD)

    fig.text(.625, .825, '$R^{W}_{S}=R^{W}_{B}R^{B}_{S}$', fontsize=23, color=WORLD)
    # Calculation sequence, separate from the geometry.
    x = .625
    for y, title, subtitle, equation, color in [
        (.77, '1  SENSOR READING', 'Point is 2 m along the sensor X axis.', '$p^{S}=(2,0)$', SENSOR),
        (.57, '2  SENSOR → BODY', 'Sensor is 1 m forward and turned 90° left.', '$p^{B}=R(90^\\circ)p^{S}+(1,0)=(1,2)$', BODY),
        (.37, '3  BODY → WORLD', 'Robot is at (3, 1), facing north (90°).', '$p^{W}=R(90^\\circ)p^{B}+(3,1)=(1,2)$', WORLD),
    ]:
        fig.text(x, y, title, fontsize=16, weight='bold', color=color)
        fig.text(x, y-.045, subtitle, fontsize=12, color=WORLD)
        fig.text(x, y-.095, equation, fontsize=17, color=color)
    fig.text(.055, .10, '$p^{W}=R^{W}_{B}(R^{B}_{S}p^{S}+t^{B}_{S})+t^{W}_{B}$', fontsize=24)
    fig.text(.055, .055, 'Rotate each offset into the destination frame, then add that frame’s translation.', fontsize=15, color=WORLD)
    fig.text(.625, .17, 'P is the same physical point in all three frames.\nMatching body/world numbers here are coincidental.\nAngles are shown in degrees; code uses radians.', fontsize=11, color=WORLD, linespacing=1.5)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix in ['png', 'svg']:
        fig.savefig(OUT / f'frame_chain_illustrated.{suffix}', dpi=180, facecolor='white')
    plt.close(fig)


def draw_point_transform():
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    fig.text(.055, .93, 'Express the same point in another frame', fontsize=28, weight='bold')
    fig.text(.055, .88, 'Robot at (3, 1), facing north   |   Point is 2 m forward   |   Distances in meters',
             fontsize=16, color=WORLD)
    ax = fig.add_axes([.055, .19, .51, .64])
    ax.set(xlim=(-.4, 4.25), ylim=(-.4, 3.8), aspect='equal')
    ax.axis('off')
    orange = '#b75b15'

    def arrow(start, end, color, lw=3, style='-'):
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                    linestyle=style, mutation_scale=19))

    arrow((0, 0), (4, 0), WORLD, lw=2)
    arrow((0, 0), (0, 3.6), WORLD, lw=2)
    ax.text(3.75, -.25, '$X_W$ / east', ha='right', fontsize=14, color=WORLD)
    ax.text(.1, 3.5, '$Y_W$ / north', fontsize=14, color=WORLD)
    ax.text(-.05, -.25, 'World origin', fontsize=12, color=WORLD)
    ax.plot([0, 3, 3], [3, 3, 0], ':', color='#b9c1c8', lw=1.5)
    ax.text(-.15, 3, '3', va='center', fontsize=12, color=WORLD)
    ax.text(3, -.2, '3', ha='center', fontsize=12, color=WORLD)

    # Body silhouette and frame at (3, 1).
    for dx, dy in [(-.25, -.25), (.25, .25), (-.25, .25), (.25, -.25)]:
        ax.plot([3, 3+dx], [1, 1+dy], color='#c1cbd3', lw=6, zorder=1)
        ax.add_patch(Circle((3+dx, 1+dy), .14, facecolor='#eef3f7', edgecolor='#aab6c1', lw=1.5))
    ax.add_patch(FancyBboxPatch((2.9, .82), .2, .36,
                              boxstyle='round,pad=0.02', facecolor='#d8e8f5', edgecolor=BODY))
    arrow((3, 1), (2.25, 1), BODY, lw=2)
    ax.text(1.9, .77, '$Y_B$ / left', fontsize=13, color=BODY)
    ax.text(3.43, .78, 'Body origin\n(3, 1)', fontsize=13, color=BODY)

    # Head-to-tail addition: origin to robot, then robot to the point.
    arrow((0, 0), (3, 1), orange)
    ax.text(1.25, .12, '$t^{W}_{B}=(3,1)$', fontsize=16, color=orange)
    arrow((3, 1), (3, 3), BODY)
    ax.text(3.13, 2.05, '$X_B$ / forward\n2 m north', fontsize=13, color=BODY)
    arrow((0, 0), (3, 3), SENSOR, lw=2.5, style='--')
    ax.text(.65, 1.55, '$p^{W}=(3,3)$', fontsize=16, color=SENSOR, rotation=45)
    ax.plot(3, 3, 'o', color='#171e25', ms=10)
    ax.text(2.1, 3.3, 'Same point P', fontsize=16, weight='bold')

    x = .625
    cards = [
        (.77, '1  DESCRIBE IT IN THE BODY FRAME', '2 m forward; 0 m left.', '$p^{B}=(2,0)$', BODY),
        (.59, '2  ROTATE THE OFFSET INTO WORLD AXES', 'Forward is north because the robot faces 90°.', '$R^{W}_{B}p^{B}=(0,2)$', BODY),
        (.41, '3  ADD THE ROBOT’S WORLD POSITION', 'Start at (3, 1), then go 2 m north.', '$p^{W}=(0,2)+(3,1)=(3,3)$', SENSOR),
    ]
    for y, title, description, equation, color in cards:
        fig.text(x, y, title, fontsize=14, weight='bold', color=color)
        fig.text(x, y-.045, description, fontsize=12, color=WORLD)
        fig.text(x, y-.095, equation, fontsize=20, color=color)
    fig.text(x, .19, 'The point does not move.\nIts coordinates depend on the origin and axes.', fontsize=14,
             color=WORLD, linespacing=1.5)
    fig.text(.055, .105, '$p^{W} = R^{W}_{B}p^{B} + t^{W}_{B}$', fontsize=29)
    fig.text(.055, .055, 'Blue: rotated offset    +    Orange: robot position    =    Green: world point',
             fontsize=15, color=WORLD)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix in ['png', 'svg']:
        fig.savefig(OUT / f'point_in_another_frame.{suffix}', dpi=180, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    draw()
    draw_point_transform()
