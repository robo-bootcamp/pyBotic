from pybotic.worlds import Continous3D_Static
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
        self.boundary = np.array([1, 2, 3, 4, 5, 6])
        self.obstacles = {'1': np.array([1]*6)}
        self.start = np.zeros((3, 1))
        self.goal = np.ones((3, 1))
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

        self.rec_check_dict(valid_output, self.c())

    def test_empty(self):
        with self.assertRaises(ValueError):
            Continous3D_Static()

    def test_shape(self):
        # test boundary
        with self.assertRaises(ValueError):
            Continous3D_Static(np.array([1]*5), self.obstacles,
                               self.start, self.goal)

        # test obstacles
        with self.assertRaises(ValueError):
            Continous3D_Static(self.boundary, {'1': np.array([1]*4)},
                               self.start, self.goal)

        # test start
        with self.assertRaises(ValueError):
            Continous3D_Static(self.boundary, self.obstacles,
                               np.zeros((3, 2)), self.goal)

        # test goal
        with self.assertRaises(ValueError):
            Continous3D_Static(self.boundary, self.obstacles,
                               self.start, np.ones((3, 5)))

    def rec_check_dict(self, a, b):
        # check keys
        assert a.keys() == b.keys()

        # ensure that values are same
        for key in a.keys():
            if isinstance(a[key], dict):
                self.rec_check_dict(a[key], b[key])
                continue
            assert all(np.equal(a[key], b[key]))

    def test_update_state(self):
        """
            test features of update state
        """
        self.c.update_state(self.goal)
