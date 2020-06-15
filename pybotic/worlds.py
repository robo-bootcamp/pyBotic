from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
from typing import Dict
from typeguard import typechecked, check_type

from pybotic.utils.world_utils import load_3d_map_from_file
from pybotic.geometry import Point3D, Cuboid, point, shape


@dataclass
class World(ABC):
    """Abstract World class

    This is an abstract class representing world
    Never to be directly used in any applications

    This object should keep track of
    - world state
    - robot state
    - provides rendering capability

    Args:
        _boundary (shape): shape object marking limits of the world
        _obstacles (Dict[str, shape]): dictionary of obstacles
                                        {name:nd shape}
        _start (point): nd point representing start
        _goal (point): nd point representing goal/target
    """
    _boundary: shape = field(default=None)
    _obstacles: Dict[str, shape] = field(default=None)
    _start: point = field(default=None)
    _goal: point = field(default=None)

    def __post_init__(self):
        """Validate inputs

        This is used to validate the inputs
        initializes _robot_pose
        """
        self._robot_pose = self._start

        for (name, field_type) in self.__annotations__.items():
            check_type(argname=name, value=self.__dict__[name],
                       expected_type=field_type)

    def get_state(self):
        """Get World State

        returns the state of the world

        Returns:
            A dictionary containg

            boundary (numpy.ndarray): boundary of the world
            Obstacle_state (numpy.ndarray): state/location of obstacles

            start (numpy.ndarray): start location
            goal (numpy.ndarray): goal location
            robot_location (numpy.ndarray): location of the robot
        """
        return dict(self.__iter__())

    def __call__(self):
        """map to .get_state()

        make use of __call__ to ease of use
            __call__ -> .get_state()
        """
        return self.get_state()

    @abstractmethod
    def update_state(self, new_robot_pose):
        """Update the state of the world

        Args:
            new_robot_pose (any): new robot pose

        Raises:
            NotImplementedError: always
        """
        # can't have pass here for coverage reasons

    @abstractmethod
    def render(self):
        """Renders the world

        renders the world, but currently abstarct
        """
        # can't have pass here for coverage reasons

    def __iter__(self):
        """Support easy unpacking

        This allows better unpacking support

        Yields:
            name (str): demangled name
            content (any): content associated with name
        """
        for name in self.__dict__:
            yield name[1:], self.__dict__[name]


@dataclass
class Continous3D_Static(World):
    """Continous 3d static world based on World

    This will be the main object that will keep track of
    - world state
    - robot state
    - provides rendering capability (todo)

    Args:
        _boundary (Cuboid): Cuboid marking limits of the world
        _obstacles (Dict[str, Cuboid]): dictionary of obstacles
                                        {name:Cuboid}
        _start (Point3D): 3D point representing start
        _goal (Point3D): 3d point representing goal/target
    """
    _boundary: Cuboid
    _obstacles: Dict[str, Cuboid] = field(default_factory={})
    _start: Point3D = field(default_factory=Point3D(0, 0, 0))
    _goal: Point3D = field(default_factory=None)

    @classmethod
    def create_from_file(cls, f_name: str):
        """Create object from file

        make use of the given file to load the world config

        Args:
            f_name (str): path to file

        Returns:
            object (Continous3D_Static): object of class
        """
        boundary, obstacles, start, goal = load_3d_map_from_file(f_name)
        if goal is None:
            goal = Point3D.create_from_iter(np.zeros((3, 1)))
        boundary = Cuboid.create_from_iter(boundary)
        for obstacle in obstacles:
            obstacles[obstacle] = Cuboid.create_from_iter(obstacles[obstacle])

        return cls(boundary, obstacles, start, goal)

    def render(self):
        """Renders the world

        renders the world, but currently todo
        """
        # TODO: write a good 3d render
        pass

    @typechecked
    def update_state(self, new_robot_pose: Point3D) -> None:
        """Update the state of the world

        Validates the inputs and then updates robot_pose

        Args:
            robot_action (Point3D): robot pose
        """
        self._robot_pose = new_robot_pose
