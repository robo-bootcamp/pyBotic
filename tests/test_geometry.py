from pybotic.geometry import (
    geometry,
    Point2D,
    Point3D,
    Rectangle,
    Cuboid
)
import unittest
import numpy as np


class TestGeometry(unittest.TestCase):
    """Unit tests for geometry library

    This class will be used to define and test all features of
    geometry objects

    please look at individual tests to see all features tested
    """

    def test_abstract_geometry(self):
        """Abstract object creation test

        make sure that obj of geometry can't be created
        when trying to create an abstract object it should
        raise NotImplementedError
        """
        with self.assertRaises(NotImplementedError):
            geometry()

    def test_valid_point2d(self):
        """Test Point2D behavior when created using valid inputs

        function will test all behaviors of Point2D object
        when created with valid inputs
        """
        # multiple valid inputs
        valid_test_inputs = [(1, 2), (1.0, 2), (1.0, 2.0)]
        self.valid_functionality_points(Point2D, valid_test_inputs)

    def test_valid_point3d(self):
        """Test Point3D behavior when created using valid inputs

        function will test all behaviors of Point3D object
        when created with valid inputs
        """
        # multiple valid inputs
        valid_test_inputs = [(1, 2, 3), (1.0, 2, 3), (1.0, 2.0, 3)]
        self.valid_functionality_points(Point3D, valid_test_inputs)

    def test_rectangles(self):
        """Test Rectangle behavior when created using valid inputs

        function will test all behaviors of Rectangle object
        when created with valid inputs
        """
        # multiple valid inputs
        valid_test_inputs = [(1, 2, 3, 4), (1.0, 2, 3, 4), (1.0, 2.0, 3, 4.0)]
        self.valid_functionality_points(Rectangle, valid_test_inputs)

        # test creation from points
        rectanges = [Rectangle.create_from_points(
            Point2D(*input_[:2]), Point2D(*input_[2:]))
            for input_ in valid_test_inputs]

        # test unpacking works propely
        for point, inp in zip(rectanges, valid_test_inputs):
            self.assertEqual(tuple(point), inp)

    def test_cuboid(self):
        """Test Cuboid behavior when created using valid inputs

        function will test all behaviors of Cuboid object
        when created with valid inputs
        """
        # multiple valid inputs
        valid_test_inputs = [(1, 2, 3, 4, 5, 6),
                             (1.0, 2.0, 3, 4, 5.0, 6),
                             (1.0, 2.0, 3, 4.0, 5, 6.0)]
        self.valid_functionality_points(Cuboid, valid_test_inputs)

        # test creation from points
        cuboids = [Cuboid.create_from_points(
            Point3D(*input_[:3]), Point3D(*input_[3:]))
            for input_ in valid_test_inputs]

        # test unpacking works propely
        for point, inp in zip(cuboids, valid_test_inputs):
            self.assertEqual(tuple(point), inp)

    def valid_functionality_points(self, class_method, test_inputs):
        """Set of tests to run to verify behavior to valid inputs

        This is a function that will be used by other tests to
        verify behavior of point objects under valid inputs


        proper functionality of geometry object
        - create using (x,y,...)
        - create from tuple
        - create from list
        - create from np.ndarray
        """

        # direct init
        objects = [class_method(*input_) for input_ in test_inputs]

        # test unpacking works properly
        for point, inp in zip(objects, test_inputs):
            self.assertEqual(tuple(point), inp)

        # tuple init
        objects = [class_method.create_from_iter(input_)
                   for input_ in test_inputs]

        # test unpacking works properly
        for point, inp in zip(objects, test_inputs):
            self.assertEqual(tuple(point), inp)

        # list init
        objects = [class_method.create_from_iter(list(input_))
                   for input_ in test_inputs]

        # test unpacking works properly
        for point, inp in zip(objects, test_inputs):
            self.assertEqual(tuple(point), inp)

        # numpy init
        objects = [class_method.create_from_iter(np.array(input_))
                   for input_ in test_inputs]

        # test unpacking works properly
        for point, inp in zip(objects, test_inputs):
            self.assertEqual(tuple(point), inp)
