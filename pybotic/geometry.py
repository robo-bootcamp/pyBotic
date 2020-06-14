from dataclasses import dataclass, astuple
from typing import Union
from abc import ABC
from typeguard import typechecked, check_type
import numpy as np


class geometry(ABC):
    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            check_type(argname=name, value=self.__dict__[name],
                       expected_type=field_type)

    @staticmethod
    def convert_type(arr):
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


@dataclass(frozen=True, unsafe_hash=True)
class Point3D(geometry):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Point2D(geometry):
    x: Union[float, int]
    y: Union[float, int]


@dataclass(frozen=True, unsafe_hash=True)
class Cuboid(geometry):
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
class Rectangle(geometry):
    x_min: Union[float, int]
    y_min: Union[float, int]
    x_max: Union[float, int]
    y_max: Union[float, int]

    @classmethod
    @typechecked
    def create_from_points(cls, p1: Point2D, p2: Point2D):
        return cls(*p1, *p2)
