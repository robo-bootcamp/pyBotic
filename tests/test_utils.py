from pybotic.utils.world_utils import load_3d_map_from_file
import numpy as np
import unittest


class TestLoad3DWorldMap(unittest.TestCase):
    """
        Tester for load_3d_world_map
        test covered:
            - valid
            - file not found
    """

    def test_valid_load(self):
        f_name = 'tests/sample_world.txt'
        boundary, obstacles, _, _ = load_3d_map_from_file(f_name)
        pass

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            load_3d_map_from_file("invalid")
