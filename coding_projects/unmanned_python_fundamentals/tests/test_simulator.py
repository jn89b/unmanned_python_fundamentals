import numpy as np
import pytest
from lecture_02.controller import distance_to, waypoint_command
from lecture_02.demo import compare_models
from lecture_02.motion_models import HolonomicModel, MotionModel, UnicycleModel
from lecture_02.pose import Pose2D
from lecture_02.rotations import rotation_matrix
from lecture_02.simulator import Simulator


def test_forward_euler_uses_old_yaw_and_does_not_mutate_pose():
    old = Pose2D(1, 2, np.pi / 2)
    new = HolonomicModel().step(old, 1, 0.5, 1, 0.1)
    assert np.allclose([new.x, new.y, new.yaw], [0.95, 2.1, np.pi / 2 + 0.1])
    assert (old.x, old.y, old.yaw) == (1, 2, np.pi / 2)
    assert new is not old


def test_unicycle_discards_lateral_velocity():
    pose = Pose2D(yaw=np.pi / 2)
    result = UnicycleModel().step(pose, 1, 99, 0.2, 0.1)
    assert np.allclose([result.x, result.y, result.yaw], [0, 0.1, np.pi / 2 + 0.02])


@pytest.mark.parametrize("dt", [0, -1, np.nan, np.inf])
def test_invalid_timestep(dt):
    for model in [HolonomicModel(), UnicycleModel()]:
        with pytest.raises(ValueError):
            model.step(Pose2D(), 1, 0, 0, dt)
    with pytest.raises(ValueError):
        Simulator(None, dt)


def test_base_class_requires_implementation():
    with pytest.raises(NotImplementedError):
        MotionModel().step(Pose2D(), 1, 0, 0, 0.1)


def test_controller_transforms_world_command_and_caps_speed():
    pose = Pose2D(yaw=1.2)
    vx, vy, omega = waypoint_command(pose, [0, 10])
    assert np.allclose(rotation_matrix(pose.yaw) @ [vx, vy], [0, 1])
    assert omega == 0
    assert waypoint_command(pose, [0, 0]) == (0, 0, 0)
    assert distance_to(pose, [3, 4]) == 5


def test_history_stores_values_not_mutable_pose_references():
    # Test double isolates history management from the student's missing move.
    class CountingRobot:
        def __init__(self):
            self.pose = Pose2D()

        def move(self, vx, vy, omega, dt):
            self.pose.x += 1

    robot = CountingRobot()
    simulator = Simulator(robot, 0.1)
    simulator.run(0, 0, 0, 3)
    assert len(simulator.history) == 4
    assert simulator.history[0] == (0, 0, 0, 0)
    assert np.allclose(simulator.history[-1], (0.3, 3, 0, 0))
    robot.pose.x = 50
    assert simulator.history[-1][1] == 3


def test_comparison_has_distinct_paths_and_same_yaw():
    histories = compare_models()
    holo = np.array(histories["HolonomicModel"])
    uni = np.array(histories["UnicycleModel"])
    assert holo.shape == uni.shape == (101, 4)
    assert np.allclose(holo[:, 3], uni[:, 3])
    assert not np.allclose(holo[:, 1:3], uni[:, 1:3])


def test_worked_example_moves_north():
    pose = Pose2D(yaw=np.pi / 2)
    updated = HolonomicModel().step(pose, 1.0, 0.0, 0.0, 0.1)
    assert np.allclose([updated.x, updated.y, updated.yaw], [0, 0.1, np.pi / 2])
    assert pose.y == 0


@pytest.mark.parametrize("compare", [False, True])
def test_demo_cli_selects_models_and_preserves_output(monkeypatch, compare):
    from lecture_02 import demo

    captured = {}

    def capture_plot(trajectories, output):
        captured.update(trajectories=trajectories, output=output)

    args = ["demo", "--output", "trajectory.png"]
    if compare:
        args.append("--compare")
    monkeypatch.setattr("sys.argv", args)
    monkeypatch.setattr(demo, "plot_trajectories", capture_plot)
    demo.main()
    expected = {"HolonomicModel", "UnicycleModel"} if compare else {"HolonomicModel"}
    assert set(captured["trajectories"]) == expected
    assert captured["output"] == "trajectory.png"
    assert np.allclose(captured["trajectories"]["HolonomicModel"][1],
                       [0.1, 0.1, 0.05, 0.02])
