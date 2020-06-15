import os
import re
import warnings
import numpy as np


def load_3D_map_from_file(file_name):
    """map loader from file

    given path to file, load 3D world map

    Args:
        file_name (str): Path to 3D world map data

    Returns:
        boundary (numpy.ndarray, shape=(6,)): physical limits of the world
        obstacles (numpy.ndarray, shape=(6,)): physical bounds of obstacles
        start (numpy.ndarray, shape=3,)): start location
        goal (numpy.ndarray, shape=(3,)): goal location

    Raises:
        FileNotFoundError: if file_name is not a valid file
        NotImplementedError: if file format is not supported
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError("No such file found")

    # Check format
    file_ext = os.path.splitext(file_name)[-1]

    if file_ext not in ['txt']:
        raise NotImplementedError("File format is not supported,\
                                   give .txt file")

    return load_3D_map_from_txt(file_name)


def load_3D_map_from_txt(file_name):
    """map loader from text file

    given path to txt file, load 3D world map

    Args:
        file_name (str): Path to .txt file

    Returns:
        boundary (numpy.ndarray, shape=(6,)): physical limits of the world
        obstacles (numpy.ndarray, shape=(6,)): physical bounds of obstacles
        start (numpy.ndarray, shape=3,)): start location
        goal (numpy.ndarray, shape=(3,)): goal location

    Raises:

    """
    # Key words dictionary for boundary, start, goal,
    # to error out for repeating arguments
    key_words = {}
    # Set of obstacles to warn for repeating obstacle values
    obstacles = set()
    # Read all lines from file
    with open(file_name) as f:
        for i, line in enumerate(f.readlines()):
            sl = re.split(': |, |\n| |,', line)[:-1]
            word = sl[0]
            if word == "#" or not word:
                continue
            array = str_conversion(sl[1:])
            # taking care of invalid statements
            if len(array) == 0:
                raise SyntaxError("Invalid statement \"{}\"".format(word))
            # taking care of boundary, start, goal and their repetitions
            if word in ["boundary", "start", "goal"]:
                if word not in key_words:
                    key_words[word] = str_conversion(array)
                else:
                    raise ValueError(f"File has mutiple {word} keyword")
            # taking care of obstacles
            elif word == "obstacle":
                obstacle = tuple(array)
                key = "obstacles"
                if obstacle in obstacles:
                    warnings.warn(f"Repeating obstacle {array}, if not"
                                  f" expected, remove them", RuntimeWarning)
                if key not in key_words:
                    key_words[key] = {word+'_0': array}
                elif key in key_words:
                    key_words[key][word+'_'+str(len(key_words[key]))] = array
                obstacles.add(tuple(array))
            # taking care of invalid key words
            else:
                raise ValueError("Invalid key word, not in "
                                 "(boundary, obstacles, start, goal)")

    # validating boundary, obstacles, start, goal
    key_words = validate_output(key_words)

    return (key_words['boundary'], key_words["obstacles"],
            key_words['start'], key_words['goal'])


def validate_output(key_words):
    """validating boundary, obstacles, start, goal

    given a dictionary of boundary, obstacles, start, goal with
    respective arrays, return validated dictionary
    for existence and array shapes

    Args:
        key_words (dict{str: numpy.ndarray}): dict of key words to numpy arrays

    Returns:
        same or updated dictionary

    Raises:
        ValueError: if boundary, goal or both not found
        ValueError: if required lengths do not match

    Warnings:
        RuntimeWarning: if start location is not given
    """
    if 'boundary' not in key_words and 'goal' not in key_words:
        raise ValueError("boundary and goal not specified in the file")
    if 'boundary' not in key_words:
        raise ValueError("boundary not specified in the file")
    if 'goal' not in key_words:
        raise ValueError("goal not specified in the file")

    for key, val in key_words.items():
        if key == 'boundary':
            if len(val) != 6:
                raise ValueError(f"Invalid {key} value, has {len(val)} items")
        if key == 'start' or key == 'goal':
            if len(val) != 3:
                raise ValueError(f"Invalid {key} value, has {len(val)} items")

    if "start" not in key_words:
        warnings.warn("start loc not given,assuming (0, 0, 0)", RuntimeWarning)
        key_words["start"] = np.zeros((3))

    if "obstacles" not in key_words:
        key_words["obstacles"] = None
    else:
        for i, (obs, val) in enumerate(key_words["obstacles"].items()):
            if len(val) != 6:
                raise ValueError(f"Invalid obstacle value,"
                                 f" has {len(val)} items")

    return key_words


def str_conversion(arr):
    """convert list of str to numpy array

    Given a list of strings, convert it to numpy array of float

    Args:
        arr (list[str]): List of str to be converted

    Returns:
        converted numpy.ndarray[float]

    Raises:
        ValueError: if elements like str/empty are not convertible to float
    """
    return np.array(arr).astype(np.float)


if __name__ == "__main__":
    file_name = "/home/gunjan/projects/pyBotic/tests/new_world.txt"

    b, o, s, g = load_3D_map_from_txt(file_name)
    print("b", b)
    print("o", o)
    print("s", s)
    print("g", g)
