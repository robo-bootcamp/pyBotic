from abc import ABC, abstractmethod
import numpy as np
from pybotic.utils.world_utils import load_3d_world_map


class World(ABC):
    """
        This is an abstract class representing world
        Never to be directly used in any applications
    """
    @abstractmethod
    def get_state(self):
        """
            returns the state of the world

            Returns:
                A dictionary containg
                start: (numpy.ndarray) start location
                goal: (numpy.ndarray) goal location
                robot_location: (numpy.ndarray) location of the
                    robot
                Obstacle_state: (numpy.ndarray) state/location of obstacles
                boundary: (numpy.ndarray) boundary of the world

        """
        pass

    @abstractmethod
    def update_state(self, robot_action):
        """
            updates the state of the world, given robot action

            - updates robot's location/state
            - update obstacles
        """
        pass

    @abstractmethod
    def render(self):
        """
            renders the envirnment
        """
        pass


class Continous3D_Static(World):
    """
        Implementation of a continous 3D world
    """

    def __init__(self, start, goal, obstacles, boundary):
        """
            sets up the world

            Args:
                start: (numpy.ndarray) start robot_location
                goal: (numpy.ndarray) goal to reach
                Obstacle: dict{key:(numpy.ndarray)} for each obstacle
                boundary: (numpy.ndarray) bounds of the world

            Returns:
                None

            Raise:
                TypeError
        """
        self.validate_inputs(start, goal, obstacles, boundary)

        self._start = start
        self._goal = goal
        self._obstacles = obstacles
        self._boundary = boundary

    @staticmethod
    def validate_inputs(start, goal, boundary, obstacles):
        """
            function that will run all the validation for
            inputs before it goes to the class

            constraints:
                - start : iterable 3d
                - goal : iterable 3d
                - boundary: iterable 6d (3d_max, 3d_min)
                - obstacles: dic{'key',{6d(3d_max, 3d_min)}}
        """
        # validate start and goal
        for ele in [start, goal]:
            if np.shape(start) not in {(3, 1), (3,)}:
                raise ValueError('wrong shape')

        if np.shape(boundary) not in {(6, 1), (6,)}:
            raise ValueError("wrong boundary shape")

        # type check
        for ele in [start, goal, boundary]:
            if not all([type(e) in [int, float] for e in ele]):
                raise TypeError

        if type(obstacles) is not dict():
            raise TypeError('obstacles should be of type dict')

        for obs_idx in obstacles:
            if np.shape(obstacles[obs_idx]) not in {(6, 1), (6,)}:
                raise ValueError("wrong obstacle shape")

            if not all([type(e) in [int, float] for e in obstacles[obs_idx]]):
                raise TypeError('all obstables should be dict(int,float)')

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
