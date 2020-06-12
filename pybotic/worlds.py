from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
from typing import Dict

from pybotic.utils.world_utils import load_3d_world_map


@dataclass
class World(ABC):
    """
        This is an abstract class representing world
        Never to be directly used in any applications
    """
    _boundary: np.ndarray = field(default=None)
    _obstacles: Dict[str, np.ndarray] = field(default=None)
    _start: np.ndarray = field(default=None)
    _goal: np.ndarray = field(default=None)

    def __pre_init__(self):
        print("asgdags")

    def __post_init__(self):
        """
            This is used to validate the inputs
        """
        self._robot_pose = self._start
        for (name, field_type) in self.__annotations__.items():
            try:
                if not isinstance(self.__dict__[name], field_type):
                    current_type = type(self.__dict__[name])
                    raise ValueError(
                        f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
            except Exception as e:
                if e == "Subscripted generics cannot be used with class and instance checks":
                    print(name, field_type, type(self.__dict__[name]))
                    continue

        # validate start and goal
        if np.shape(self._start) not in {(3, 1), (3,)}:
            raise ValueError(f'wrong shape {np.shape(self._start)}, {self._start}')

        if np.shape(self._goal) not in {(3, 1), (3,)}:
            raise ValueError(f'wrong shape {np.shape(self._goal)}')

        if np.shape(self._boundary) not in {(6, 1), (6,)}:
            raise ValueError(f"wrong boundary shape {np.shape(self._boundary)}")

        for obs_idx in self._obstacles:
            if np.shape(self._obstacles[obs_idx]) not in {(6, 1), (6,)}:
                raise ValueError(f"wrong obstacle shape {np.shape(self._obstacles[obs_idx])}")

    def get_state(self):
        """
            returns the state of the world

            Returns:
                A dictionary containg.__annotations__
                boundary: (numpy.ndarray) boundary of the world

                start: (numpy.ndarray) start location
                goal: (numpy.ndarray) goal location
                robot_location: (numpy.ndarray) location of the
                    robot
                Obstacle_state: (numpy.ndarray) state/location of obstacles

        """
        return dict(self.__iter__())

    def __call__(self):
        return self.get_state()

    def update_state(self, robot_action):
        """
            currently just pass through

            Args:
                robot_action: (iterable 3d) robot pose
        """
        if np.shape(robot_action) not in {(3, 1), (3,)}:
            raise ValueError('wrong shape')

        self._robot_pose = robot_action

    @abstractmethod
    def render(self):
        """
            renders the envirnment
        """
        pass

    def __iter__(self):
        for name in self.__dict__:
            yield name[1:], self.__dict__[name]


@dataclass
class Continous3D_Static(World):
    """
        Implementation of a continous 3D world
    """

    @classmethod
    def create_from_txt_file(cls, f_name):
        """
            make use of the given file to load the world config

            Args:
                f_name: (str) path to file

            returns:

        """
        start, goal, obstacles, boundary = load_3d_world_map(f_name)
        if start is None:
            start = np.zeros((3, 1))
        return cls(start, goal, obstacles, boundary)

    def render(self):
        # TODO: render
        pass
