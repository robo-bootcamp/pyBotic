from pybotic.worlds import Continous3D_Static
from pybotic.utils.world_utils import load_3d_world_map
import numpy as np


def test_continous3d_static():
    # test valid constructor
    boundary = np.array([1, 2, 3, 4, 5, 6])
    obstacles = {'1': np.array([1]*6), '2': np.array([2]*6)}
    start = np.zeros((3, 1))
    goal = np.ones((3, 1))

    c = Continous3D_Static(boundary, obstacles, start, goal)

    assert isinstance(c, Continous3D_Static)

    c()
