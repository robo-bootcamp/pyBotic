from pybotic.utils.world_utils import load_3d_world_map
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
        boundary, obstacles = load_3d_world_map(f_name)
        boundary_ = np.array([[b'boundary', b'0.0', b'-5.0', b'0.0', b'10.0',
                               b'20.0', b'6.0', b'120.0', b'120.0', b'120.0']],
                             dtype='|S8')

        obstacle_ = np.array([[b'block', b'0.0', b'2.0', b'0.0', b'10.0',
                               b'2.5', b'1.5', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'0.0', b'2.0', b'4.5', b'10.0',
                               b'2.5', b'6.0', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'0.0', b'2.0', b'1.5', b'3.0',
                               b'2.5', b'4.5', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'7.0', b'2.0', b'1.5', b'10.0',
                               b'2.5', b'4.5', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'3.0', b'0.0', b'2.4000000953674316',
                               b'7.0', b'0.5', b'4.5', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'0.0', b'15.0', b'0.0', b'10.0',
                               b'20.0', b'1.0', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'0.0', b'15.0', b'1.0', b'10.0',
                               b'16.0', b'3.5', b'120.0', b'120.0', b'120.0'],
                              [b'block', b'0.0', b'18.0', b'4.5', b'10.0',
                               b'19.0', b'6.0', b'120.0', b'120.0', b'120.0']],
                             dtype='|S18')

        assert np.all(boundary == boundary_), "Load error"
        assert np.all(obstacles == obstacle_), "Load error"

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            load_3d_world_map("invalid")
