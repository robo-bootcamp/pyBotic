from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np
from typing import Dict
from typeguard import typechecked, check_type

from pybotic.utils.world_utils import load_3d_world_map
from pybotic.geometry import Point3D, Cuboid


@dataclass
class World(ABC):
    """Abstaract World class

    This is an abstract class representing world
    Never to be directly used in any applications
    """
    _boundary: np.ndarray = field(default=None)
    _obstacles: Dict[str, np.ndarray] = field(default=None)
    _start: np.ndarray = field(default=None)
    _goal: np.ndarray = field(default=None)

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

            boundary: (numpy.ndarray) boundary of the world
            start: (numpy.ndarray) start location
            goal: (numpy.ndarray) goal location
            robot_location: (numpy.ndarray) location of the
                robot
            Obstacle_state: (numpy.ndarray) state/location of obstacles

        """
        return dict(self.__iter__())

    def __call__(self):
        """map to .get_state()

        make use of __call__ to ease of use
            __cal__ -> .get_state()
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
        raise NotImplementedError("abstractmethod")

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
            name: (str) demangled name
            content: (any) content associated with name
        """
        for name in self.__dict__:
            yield name[1:], self.__dict__[name]


@dataclass
class Continous3D_Static(World):
    """Continous 3d static world based on World

    This will be the main obect that will keep track of
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
    _obstacles: Dict[str, Cuboid]
    _start: Point3D
    _goal: Point3D

    @classmethod
    def create_from_file(cls, f_name: str):
        """Create object from file

        make use of the given file to load the world config

        Args:
            f_name: (str) path to file

        Returns:
            object: (Continous3D_Static) object of class
        """
        boundary, obstacles, start, goal = load_3d_world_map(f_name)
        if start is None:
            start = Point3D.create_from_iter(np.zeros((3, 1)))
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
            robot_action: (iterable 3d) robot pose

        Raises:
            ValueError: if robot_action is of wrong shape
            TypeError: if robot_action is of wrong type
        """
        self._robot_pose = new_robot_pose
