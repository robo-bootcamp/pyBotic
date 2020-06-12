import numpy as np
import os.path


def load_3d_world_map(file_name):
    """
        given a map file load 3d map boundary and obstacles

        Args:
            file_name: [str] path to map file

        Returns:
            boundary: [numpy.ndarray] physical limits the world
            obstacles: [numpy.ndarray] physical bounds of obstacles

        Raises:
            FileNotFoundError: if file_name is not a valid file

    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError('file was not found')

    colum_names = ('type', 'xmin', 'ymin', 'zmin',
                   'xmax', 'ymax', 'zmax', 'r', 'g', 'b')

    map_data = np.loadtxt(file_name,
                          dtype={'names': colum_names,
                                 'formats': ('S8', 'f', 'f', 'f', 'f',
                                             'f', 'f', 'f', 'f', 'f')}
                          )
    block_id = map_data['type'] == b'block'
    boundary = np.array(map_data[~block_id][list(colum_names)].tolist())
    obstacles = np.array(map_data[block_id][list(colum_names)].tolist())

    return boundary, obstacles


if __name__ == '__main__':
    file_name = 'tests/sample_world.txt'
    boundary, obstacles = load_3d_world_map(file_name)
