from pybotic.worlds import Continous3D_Static
from pybotic.geometry import Point3D, Cuboid

import unittest
import numpy as np


class TestContinous3DStatic(unittest.TestCase):
    """
        Tester for Continous3D_Static
        test covered:
            - valid
            - file not found
    """

    def setUp(self):
        self.boundary = Cuboid.create_from_iter([1, 2, 3, 4, 5, 6])
        self.obstacles = {'1': Cuboid.create_from_iter([1]*6)}
        self.start = Point3D.create_from_iter(np.zeros((3, 1)))
        self.goal = Point3D.create_from_iter(np.ones((3, 1)))
        self.c = Continous3D_Static(self.boundary, self.obstacles,
                                    self.start, self.goal)

    def test_valid(self):
        """
            this is will check all the valid cases
            - valid construction
            - get state

        """
        # valid construction
        self.assertIsInstance(self.c, Continous3D_Static)

        valid_output = {'boundary': self.boundary,
                        'obstacles': self.obstacles,
                        'start': self.start,
                        'goal': self.goal,
                        'robot_pose': self.start}

        self.assertEqual(self.c(), valid_output)

    def test_empty(self):
        with self.assertRaises(TypeError):
            Continous3D_Static()

    def test_update(self):
        self.c.update_state(self.goal)

        self.assertEqual(self.goal, self.c._robot_pose)

    def test_render(self):
        # dummy test since render is pass
        self.c.render()
