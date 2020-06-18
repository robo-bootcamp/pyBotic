from dataclasses import dataclass, astuple
from typing import Union, Iterable, Any, Generator
from abc import ABC
from typeguard import typechecked, check_type
import numpy as np


@dataclass
class geometry(ABC):
    """Abstact parent class geometry

    This is actually an abstract class not to be used
    """

    def __init__(self) -> None:
        """init

        Need to explicitly rewrite since @dataclass overrides ABC

        Raises:
            NotImplementedError: always
        """
        # this is enable static typing
        self.__annotations__ = {'dummy': None}
        raise NotImplementedError("this is abstaract")

    def __post_init__(self) -> None:
        """Validation helper

        Enforce Strict Type check for all geometry objects
        """
        for (name, field_type) in self.__annotations__.items():
            check_type(
                argname=name, value=self.__dict__[name], expected_type=field_type
            )

    @staticmethod
    def convert_type(arr: Iterable[Any]) -> Iterable[Union[int, float]]:
        """convert type helper

        This is to help deal with annoyance of typechecking numpy
        Currently done by mapping
            np.int* -> int
            np.float* -> float

        Args:
            arr (numpy.ndarray, list, tuple): array to convert

        Returns:
            arr (list, tuple): after converting numpy
        """
        if isinstance(arr, np.ndarray):
            return arr.ravel().tolist()
        return arr

    @classmethod
    def create_from_iter(cls, arr: Iterable[Any]):
        """create from iterable

        Creates the class after unpacking and converting iterables

        Args:
            arr (iterables): iterable to be used for creating

        Returns:
            object (geometry): object created from this iter
        """
        return cls(*cls.convert_type(arr))

    def __iter__(self) -> Generator[Union[int, float], None, None]:
        """easy unpacking

        This is to support easy unpacking of containers

        Yields:
            element (any): content of container
        """
        yield from astuple(self)


@dataclass
class point(geometry):
    """point object

    This will be the parent class of all point objects
    will be used for meta typing and testing moslty
    """


@dataclass
class shape(geometry):
    """shape object

    This will be the parent for all nd shape objects
    will be used to metatyping and testing
    """


@dataclass(frozen=True, unsafe_hash=True)
class Point3D(point):
    """3D point

    High performance container for 3d points

    Args:
        x (Union[float,int]): x-coordinate of the point
        y (Union[float,int]): y-coordinate of the point
        z (Union[float,int]): z-coordinate of the point
    """

    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Point2D(point):
    """2D point

    High performance container for 2d points

    Args:
        x (Union[float,int]): x-coordinate of the point
        y (Union[float,int]): y-coordinate of the point
    """

    x: Union[float, int]
    y: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Cuboid(shape):
    """Cuboid

    High performance container for 3d Cuboid

    Args:
        x_min (Union[float,int]): x-coordinate of the min point
        y_min (Union[float,int]): y-coordinate of the min point
        z_min (Union[float,int]): z-coordinate of the min point
        x_max (Union[float,int]): x-coordinate of the max point
        y_max (Union[float,int]): y-coordinate of the max point
        z_max (Union[float,int]): z-coordinate of the max point
    """

    x_min: Union[float, int]
    y_min: Union[float, int]
    z_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]
    z_max: Union[float, int]

    @classmethod
    @typechecked
    def create_from_points(cls, p1: Point3D, p2: Point3D):
        """method to create cls obj from 2 poitns

        This method can be used to create a cuboid object
        from two 3d points that correspond to
        start and end of any of the major diagonal
        """
        return cls(*p1, *p2)


@dataclass(frozen=True, unsafe_hash=True)
class Rectangle(shape):
    """Rectangle

    High performance container for 2d rectangle

    Args:
        x_min (Union[float,int]): x-coordinate of the min point
        y_min (Union[float,int]): y-coordinate of the min point
        x_max (Union[float,int]): x-coordinate of the max point
        y_max (Union[float,int]): y-coordinate of the max point
    """

    x_min: Union[float, int]
    y_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]

    @classmethod
    @typechecked
    def create_from_points(cls, p1: Point2D, p2: Point2D):
        return cls(*p1, *p2)
