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
    # Key words of interest, to check for repeating arguments
    key_words = {'boundary': 0, 'start': 0, 'goal': 0}
    key_set = set()
    # To create a dictionary of unique obstacles
    obstacles = {}
    # Read all lines from file
    with open(file_name) as f:
        for i, line in enumerate(f.readlines()):
            sl = re.split(': |, |\n| |,', line)[:-1]
            if sl[0] == "#" or not sl[0]:
                continue
            print("sl:", sl)
            array = str_conversion(sl[1:])
            print("array:", array)
            if len(array) == 0:
                raise SyntaxError("Invalid statement \"{}\"".format(sl[0]))
            if sl[0] in key_words:
                if sl[0] not in key_set:
                    key_set.add(sl[0])
                    key_words[sl[0]] = str_conversion(sl[1:])
                elif sl[0] in key_set:
                    raise ValueError("File has mutiple {} argument".format(sl[0]))


    validate_output(key_set, key_words)
    obstacles = get_obstacles_dict(obstacles)

    #return boundary, obstacles, start, goal


def validate_output(key_set, key_words):
    if 'boundary' not in key_set and 'goal' not in key_set:
        raise ValueError("boundary and goal not specified in the file")
    if 'boundary' not in key_set:
        raise ValueError("boundary not specified in the file")
    if 'goal' not in key_set:
        raise ValueError("goal not specified in the file")

    for key, val in key_words.items():
        if key == 'boundary':
            if len(val) != 6:
                raise ValueError("Invalid {} argument has {} items".format(key, len(val)))
        if key == 'start' or key == 'goal':
            if len(val) != 3:
                raise ValueError("Invalid {} argument".format(key))


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


if __name__ == "__main__":
    file_name = "/home/gunjan/projects/pyBotic/tests/new_world.txt"

    load_3D_map_from_txt(file_name)
    """
    print("b", b)
    print("o", o)
    print("s", s)
    print("g", g)
    """
