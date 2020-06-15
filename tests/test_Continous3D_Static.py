from pybotic.worlds import Continous3D_Static
from pybotic.geometry import Point3D, Cuboid

import unittest
import numpy as np


class TestContinous3DStatic(unittest.TestCase):
    """Tester for Continous3D_Static

    test covered:
        - valid
        - file not found
    """

    def setUp(self):
        """initializes test object

        equivalent of __init__()

        sets_up:
            -boundary (Cuboid)
            -obstacles (Dict[str,Cuboid])
            -start (Point3D)
            -goal (Point3D)
            -
        """
        self.boundary = Cuboid.create_from_iter([1, 2, 3, 4, 5, 6])
        self.obstacles = {'1': Cuboid.create_from_iter([1]*6)}
        self.start = Point3D.create_from_iter(np.zeros((3, 1)))
        self.goal = Point3D.create_from_iter(np.ones((3, 1)))
        self.cworld = Continous3D_Static(self.boundary, self.obstacles,
                                         self.start, self.goal)
        self.file_path = 'tests/map_files/'

    def test_valid(self):
        """Test under valid inputs

        this is will check valid cases
        - valid construction
        - get state

        """
        # valid construction
        self.assertIsInstance(self.cworld, Continous3D_Static)

        valid_output = {'boundary': self.boundary,
                        'obstacles': self.obstacles,
                        'start': self.start,
                        'goal': self.goal,
                        'robot_pose': self.start}

        self.assertEqual(self.cworld(), valid_output)

        # support empty obstacles
        Continous3D_Static(self.boundary, {}, self.start, self.goal)

    def test_empty(self):
        """Empty check

        Tries to create an object with empty inputs
        makes sure it triggers TypeError
        """
        with self.assertRaises(TypeError):
            Continous3D_Static()

    def test_update(self):
        """Update state check

        Make sure that update state works properly
        """
        self.cworld.update_state(self.goal)
        self.assertEqual(self.goal, self.cworld._robot_pose)

    def test_render(self):
        """test the rendering engine

        Currely a dummy test need to write the renderer first
        """
        self.cworld.render()

    def test_load_3d_map_from_file(self):
        Continous3D_Static.create_from_file(self.file_path+'sample_world.txt')
