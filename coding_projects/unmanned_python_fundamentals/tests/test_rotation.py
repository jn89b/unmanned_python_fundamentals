import numpy as np
import pytest
from lecture_02.rotations import rotation_matrix


@pytest.mark.parametrize("angle, expected", [(0, [2, 0]), (90, [0, 2]),
                                              (180, [-2, 0]), (270, [0, -2])])
def test_cardinal_rotations(angle, expected):
    assert np.allclose(rotation_matrix(np.deg2rad(angle)) @ [2, 0], expected)


@pytest.mark.parametrize("theta", [-3.1, -0.5, 0, 0.6, 2.7, 8.2])
def test_rotation_preserves_length_and_inverse(theta):
    matrix = rotation_matrix(theta)
    vector = np.array([1.7, -0.8])
    assert np.isclose(np.linalg.norm(matrix @ vector), np.linalg.norm(vector))
    assert np.allclose(matrix.T @ matrix, np.eye(2))
    assert np.isclose(np.linalg.det(matrix), 1)
