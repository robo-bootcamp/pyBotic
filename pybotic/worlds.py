# this file contains implementations for abstract world class


class world:
    """
        This is an abstract class representing world
        Never to be directly used in any applications
    """

    def get_state(self):
        """
            returns the state of the world

            Returns:
                A dictionary containg
                start: [numpy.ndarray] start location
                goal: [numpy.ndarray] goal location
                robot_location: [numpy.ndarray] location of the
                    robot
                Obstacle_state: [numpy.ndarray] state/location of obstacles
                boundary: [numpy.ndarray] boundary of the world

        """
        raise NotImplementedError('This is an abstract method')

    def update_state(self, robot_action):
        """
            updates the state of the world, given robot action

            - updates robot's location/state
            - update obstacles
        """
        raise NotImplementedError('This is an abstract method')

    def render(self):
        """
            renders the envirnment
        """
        raise NotImplementedError("This is an abstract method")


def test():
    return "Hello"
