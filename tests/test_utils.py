from pybotic.utils.world_utils import load_3d_map_from_file
import unittest


class TestLoad3DWorldMap(unittest.TestCase):
    """
        Tester for load_3d_world_map
        test covered:
            - valid
            - file not found
    """

    def setUp(self):
        # keep track of path for ease of use
        self.path = "tests/map_files/"

    def test_valid_load(self):
        # testing a valid file loading
        f_name = 'tests/map_files/sample_world.txt'
        boundary, obstacles, _, _ = load_3d_map_from_file(f_name)

    def test_invalid_file(self):
        # if file not found
        with self.assertRaises(FileNotFoundError):
            load_3d_map_from_file("invalid")

    def test_not_supported_format(self):
        # format not currently supported
        with self.assertRaises(NotImplementedError):
            load_3d_map_from_file(self.path + "invalid1.invalid")

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
        # if any of the shapes don't match expected shape raise ValueError
        for file in range(1, 4):
            with self.assertRaises(ValueError):
                load_3d_map_from_file(self.path + f'shape_error{file}.txt')

    def test_keyword_missing(self):
        # if any of the keywords are missing raise a warning
        with self.assertWarns(Warning):
            load_3d_map_from_file(self.path + "warn1.txt")
