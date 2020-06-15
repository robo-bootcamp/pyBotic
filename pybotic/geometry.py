from dataclasses import dataclass, astuple
from typing import Union
from abc import ABC
from typeguard import typechecked, check_type
import numpy as np


@dataclass
class geometry(ABC):
    """
        This is actually an abstract class
        not to be used
    """

    def __init__(self):
        """
            Need to explicitly rewrite since @dataclass overrides ABC
        """
        raise NotImplementedError("this is abstaract")

    def __post_init__(self):
        """
            Enforce Strcit Type check for all geometry objects
        """
        for (name, field_type) in self.__annotations__.items():
            check_type(argname=name, value=self.__dict__[name],
                       expected_type=field_type)

    @staticmethod
    def convert_type(arr):
        """
            support:
                np.int* -> int
                np.float* -> float
        """
        if isinstance(arr, np.ndarray):
            return arr.tolist()
        else:
            return arr

    @classmethod
    def create_from_iter(cls, arr):
        """
            Creates the class after unpacking and converting iterables
        """
        return cls(*cls.convert_type(arr))

    def __iter__(self):
        yield from astuple(self)


@dataclass
class point(geometry):
    """ point object

    This will be the parent class of all point objects
    will be used for meta typing and testing moslty
    """
    pass


@dataclass
class shape(geometry):
    """ shape object

    This will be the parent for all nd shape objects
    will be used to metatyping and testing
    """
    pass


@dataclass(frozen=True, unsafe_hash=True)
class Point3D(point):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Point2D(point):
    x: Union[float, int]
    y: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Cuboid(shape):
    x_min: Union[float, int]
    y_min: Union[float, int]
    z_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]
    z_max: Union[float, int]

    @classmethod
    @typechecked
    def create_from_points(cls, p1: Point3D, p2: Point3D):
        return cls(*p1, *p2)


@dataclass(frozen=True, unsafe_hash=True)
class Rectangle(shape):
    x_min: Union[float, int]
    y_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]

    @classmethod
    @typechecked
    def create_from_points(cls, p1: Point2D, p2: Point2D):
        return cls(*p1, *p2)
