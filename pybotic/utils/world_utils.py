import os
import re
import warnings
import numpy as np
from typing import Tuple, Dict, Generator, Optional, Union


# Custom types
Map_File_Type = Tuple[
    np.ndarray, Union[Dict[str, np.ndarray], dict], np.ndarray, Optional[np.ndarray]
]


def load_3d_map_from_file(file_name: str) -> Map_File_Type:
    """map loader from file

    given path to file, load 3D world map

    Args:
        file_name (str): Path to 3D world map data

    Returns:
        boundary (numpy.ndarray, shape=(6,)): physical limits of the world
        obstacles Dict[str, (numpy.ndarray, shape=(6,))]: physical bounds of obstacles
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

    if file_ext not in [".txt"]:
        raise NotImplementedError("File format is not supported give .txt file")

    return load_3d_map_from_txt(file_name)


def init_parse(f_name: str) -> Generator[Tuple[str, np.ndarray], None, None]:
    """initial text parser

    given path to txt file, parse to tag, value pair

    Args:
        file_name (str): Path to .txt file

    Yields:
        tag (str): keyword tag
        val (np.ndarray): the value associated with the tag

    Raises:

    """
    assert isinstance(f_name, str)
    with open(f_name) as f:
        for line in f.readlines():
            line = line.strip("\n")
            if not line or line[0] == "#":
                continue
            try:
                tag, val = line.split(":")
                val = np.array(re.split(" ,|,", val)).astype(float)
            except ValueError:
                raise SyntaxError("Invalid Syntax")
            assert isinstance(tag, str)
            assert isinstance(val, np.ndarray)

            if tag not in {"boundary", "obstacle", "start", "goal"}:
                raise SyntaxError("Invalid keyword")
            if tag in {"boundary", "obstacle"}:
                if len(val) != 6:
                    raise ValueError("Invalid Size")
            else:
                if len(val) != 3:
                    raise ValueError("Invalid Size")

            yield tag, val


def load_3d_map_from_txt(f_name: str) -> Map_File_Type:
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
    obstacles = {}
    unique_obstacles = set()
    res = {}
    for tag, val in init_parse(f_name):
        if tag in {"start", "goal", "boundary"}:
            if tag not in res:
                res[tag] = val
            else:
                raise ValueError("repeating keyword")
        else:  # if tag == "obstacle":
            obstacles[f"obstacle_{len(obstacles)}"] = val
            obstacle = tuple(val)
            if obstacle in unique_obstacles:
                warnings.warn(f"Repeating obstacle {val}")
            unique_obstacles.add(obstacle)

    if "boundary" not in res:
        raise KeyError("boundary not specified in the file")

    if "start" not in res:
        warnings.warn("start not given,assuming (0, 0, 0)")
        start = np.zeros((3))
    else:
        start = res["start"]

    if "goal" not in res:
        warnings.warn("goal not given, assuming 'None'")
        goal = None
    else:
        goal = res["goal"]

    return res["boundary"], obstacles, start, goal
