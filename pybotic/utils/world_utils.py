import numpy as np
import os
import re


def load_3D_map_from_file(file_name):
    """
        given path to file, load 3D world map

        Args:
            file_name: (str) Path to 3D world map data

        Returns:
            boundary: (numpy.ndarray) physical limits of the world
            obstacles: (numpy.ndarray) physical bounds of obstacles
            start: (numpy.ndarray) start location of robot
            goal: (numpy.ndarray) goal location

        Raises:
            FileNotFoundError: if file_name is not a valid file
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError("No such file found")

    # Check format
    file_ext = os.path.splitext(file_name)[-1]

    if file_ext not in ['txt', 'json']:
        raise NotImplementedError("File format is not supported,\
                                   give txt/json file")

    if file_ext == 'txt':
        return load_3D_map_from_txt(file_name)
    elif file_ext == 'json':
        return load_3D_map_from_json(file_name)


def load_3D_map_from_txt(file_name):
    """
        given path to txt file, load 3D world map

        Args:
            file_name: (str) Path to .txt file

        Returns:
            boundary: (numpy.ndarray) physical limits of the world
            obstacles:(numpy.ndarray) physical bounds of obstacles
            start: (numpy.ndarray) start location of robot
            goal: (numpy.ndarray) goal location
    """
    # Read all lines from file
    with open(file_name) as f:
        content = f.readlines()

    # Key words of interest, to check for repeating arguments
    key_words = {'boundary': 0, 'start': 0, 'goal': 0}

    # To create a dictionary of unique obstacles
    obstacles = set()

    for i, line in enumerate(content):
        sl = re.split(' |, |\n', line)[:-1]
        if sl[0] in key_words:
            key_words[sl[0]] += 1
        if sl[0] == "boundary":
            boundary = str_conversion(sl[1:])
        elif sl[0] == 'obstacle':
            obstacles.add(tuple(str_conversion(sl[1:])))
        elif sl[0] == 'start':
            start = str_conversion(sl[1:])
        elif sl[0] == 'goal':
            goal = str_conversion(sl[1:])

    # Validate key word inputs
    validate_inputs(key_words)
    obstacles = get_obstacles_dict(obstacles)

    return boundary, obstacles, start, goal


def get_obstacles_dict(arr):
    """
        Given a set of obstacles, return dictionary of obstacles

        Args:
            arr: (set[tuple[int/float]]) set of obstacles

        Returns:
            dict{str: numpy.ndarray[int] or numpy.ndarray[float]}
    """
    obstacles = {}
    for i, obs in enumerate(arr):
        obstacles['obstacle_'+str(i+1)] = np.array(obs)
    return obstacles


def validate_inputs(key_words):
    """
        Given dictionary of key words, validate it for non repetitions

        Args:
            key_words: (dict[str:int]) dictionary of key words

        Returns:
            None

        Raises:
            ValueError if any of the key words is written more than once
            in the file

    """
    for key, val in key_words.items():
        if key in ['boundary', 'start', 'goal']:
            if val > 1:
                raise ValueError("File has mutiple {} argument".format(key))


def str_conversion(arr):
    """
        Given a list of strings, convert it to numpy array of int/float

        Args:
            arr: (list[str]) List of str to be converted

        Returns:
            numpy.ndarray[int] or numpy.ndarray[float]

        Raises:
            ValueError if any element is not convertible to int/float
    """
    try:
        return np.array(arr).astype(np.int)
    except ValueError:
        return np.array(arr).astype(np.float)


def load_3D_map_from_json(file_name):
    """
        given path to json file, load 3D world map

        Args:
            fname: [str] Path to .json file

        Returns:
            boundary: [numpy.ndarray] physical limits of the world
            obstacles: [numpy.ndarray] physical bounds of obstacles
            start: [numpy.ndarray] start location of robot
            goal: [numpy.ndarray] goal location
    """
    raise NotImplementedError
