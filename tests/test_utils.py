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

    def setUp(self):
        self.path = "tests/map_files/"

    def test_valid_load(self):
        f_name = 'tests/map_files/sample_world.txt'
        boundary, obstacles, _, _ = load_3d_map_from_file(f_name)
        pass

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            load_3d_map_from_file("invalid")

    def test_not_supported_format(self):
        with self.assertRaises(NotImplementedError):
            load_3d_map_from_file(self.path + "invalid1.json")

    def test_invalid_syntax(self):
        # wrong key "asdfjkjlfskd: 1, 2, 3, 4, 5, 6"
        with self.assertRaises(SyntaxError):
            load_3d_map_from_file(self.path + 'syntax_err1.txt')
        # random txt "ajlkflkfsdajlkf:"
        with self.assertRaises(SyntaxError):
            load_3d_map_from_file(self.path + 'syntax_err2.txt')

    def test_value_errors(self):
        # repeating keyword
        with self.assertRaises(ValueError):
            load_3d_map_from_file(self.path + "value_err1.txt")

    def test_repeated_obstacle_warnings(self):
        # same obstacle repeated
        with self.assertWarns(Warning):
            load_3d_map_from_file(self.path + "warn_obs_repeat.txt")

    def test_missing_boundary(self):
        # missing boundary
        with self.assertRaises(KeyError):
            load_3d_map_from_file(self.path + "no_bound.txt")

    def test_shape_errors(self):
        for file in range(1, 4):
            with self.assertRaises(ValueError):
                load_3d_map_from_file(self.path + f'shape_error{file}.txt')

    def test_keyword_missing(self):
        with self.assertWarns(Warning):
            load_3d_map_from_file(self.path + "warn1.txt")
