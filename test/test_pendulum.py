# -----------
#    Tests for the Pendulum and DoublePendulum classes
# -----------
import os, sys
# add parent directory to path, to import classes
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
import unittest
import numpy as np

from pendulum import Pendulum
from pendulum import DoublePendulum


class PendulumTests(unittest.TestCase):
    '''
        A test case for the Pendulum class
    '''
    def test_pendulum_angle(self):
        '''
            Tests the "Pendulum.set_angle" method against a set of test cases.
        '''
        # test cases, first tuple is (length, origin, theta),
        # second tuple is (x_expected, y_expected)
        test_cases= [
            [(1,[0,0],0), (0,-1)],
            [(2,[0,0],0), (0,-2)],
            [(1,[1,1],0), (1, 0)],
            [(1,[0,0], 2*np.pi), (0,-1)],
            [(0, [1,1], 0), (1,1)]
        ]
        for case in test_cases:
            with self.subTest(case):
                # name case data
                input, expected_output = case
                # set pendulum
                pendulum = Pendulum(length=input[0], origin=input[1])
                pendulum.set_angle(theta=input[2])
                # test for equality
                self.assertAlmostEqual(pendulum.x, expected_output[0], 10)
                self.assertAlmostEqual(pendulum.y, expected_output[1], 10)

    def test_pendulum_angular_velocity(self):
        '''
            Tests the "Pendulum.set_angular_velocity" method
        '''
        # first tuple in list is (length, theta, w), second is 
        # (x_expected,y_expected)
        test_cases= [
            [(1, 0, 0), (0, 0)],
            [(1, 0, 1), (1, 0)],
            [(2, 0, 1), (2, 0)],
            [(1, np.pi/2 , 1), (0, 1)],
            [(1, np.pi/2, -1), (0,-1)]
        ]

        for case in test_cases:
            with self.subTest(case):
                # name case data
                input, expected_output = case
                # set pendulum
                pendulum = Pendulum(length=input[0])
                pendulum.set_angle(theta=input[1])
                pendulum.set_angular_velocity(w=input[2])
                # test for equality
                self.assertAlmostEqual(pendulum.vx, expected_output[0], 10)
                self.assertAlmostEqual(pendulum.vy, expected_output[1], 10)

class DoublePendulumTests(unittest.TestCase):
    '''A test case for the double pendulum class'''
    def test_double_pendulum_positions(self):
        '''
            Tests the cartesian coordinates of the two pendula composing the double pendulum, after setup.
        '''
        # properties list, length1, origin1, length2
        properties = [
            (1, [0,0], 1)
            ,(2, [0,0], 2)
            ,(1, [1,1], 1)
            ,(1, [0,0], 1)
            ,(1, [0,0], 1)
            ,(1, [0,0], 1)
        ]
        # cases for pendulum state
        state= [
            {'theta1': 0, 'theta2': 0, 'w1': 0, 'w2': 0}
            ,{'theta1': 0, 'theta2': 0, 'w1': 0, 'w2': 0}
            ,{'theta1': 0, 'theta2': 0, 'w1': 0, 'w2': 0}
            ,{'theta1': np.pi/2, 'theta2': 0, 'w1': 0, 'w2': 0}
            ,{'theta1': np.pi/2, 'theta2': np.pi, 'w1': 0, 'w2': 0}
            ,{'theta1': -np.pi/2, 'theta2': -np.pi, 'w1': 0, 'w2': 0}
        ]
        # expected cartesian coordinates for each pendulum
        expected_output = [
            ([0,-1], [0,-2])
            ,([0,-2], [0,-4])
            ,([1,0], [1,-1])
            ,([1,0], [1,-1])
            ,([1,0], [1,1])
            ,([-1,0], [-1,1])
        ]
        # test the defined cases
        test_cases = zip(properties, state, expected_output)
        for case in test_cases:
            with self.subTest(case):
                # name test data
                properties, state, expected_output = case
                # initiate double pendulum
                upper_pendulum = Pendulum(length=properties[0]
                                          , origin=properties[1])
                lower_pendulum = Pendulum(length=properties[2])
                double_pendulum = DoublePendulum(pendulum1=upper_pendulum
                                                 , pendulum2=lower_pendulum)
                # set upper pendulum
                double_pendulum.set_double_pendulum(**state)
                
                # check for equality
                self.assertAlmostEqual(double_pendulum.pendulum1.x
                                       , expected_output[0][0], 10)
                self.assertAlmostEqual(double_pendulum.pendulum1.y
                                       , expected_output[0][1], 10)
                self.assertAlmostEqual(double_pendulum.pendulum2.x
                                       , expected_output[1][0], 10)
                self.assertAlmostEqual(double_pendulum.pendulum2.y
                                       , expected_output[1][1], 10)
                
    def test_double_pendulum_velocities(self):
        '''
            Tests the cartesian velocities of the two pendula composing the double pendulum, after setup.
        '''
        # pendulum properties, length1, length2
        properties = [
            (1, 1)
            , (1, 1)
            , (1, 1)
            , (1, 2)
        ]
        # cases for pendulum state
        state= [
            {'theta1': 0, 'theta2': 0, 'w1': 0, 'w2': 0}
            , {'theta1': 0, 'theta2': 0, 'w1': 1, 'w2': 1}
            , {'theta1': np.pi/2, 'theta2': 0, 'w1': 1, 'w2': 1}
            , {'theta1': 0, 'theta2': np.pi/2, 'w1': 2, 'w2': 1}
        ]
        # expected cartesian velocities for each pendulum
        expected_output = [
            ([0,0], [0,0])
            ,([1,0], [2,0])
            ,([0,1], [1,1])
            ,([2,0], [2,2])
        ]
        # test the defined cases
        test_cases = zip(properties, state, expected_output)
        for case in test_cases:
            with self.subTest(case):
                # name test data
                properties, state, expected_output = case
                # initiate double pendulum
                upper_pendulum = Pendulum(length=properties[0])
                lower_pendulum = Pendulum(length=properties[1])
                double_pendulum = DoublePendulum(pendulum1=upper_pendulum
                                                 , pendulum2=lower_pendulum)
                # set upper pendulum
                double_pendulum.set_double_pendulum(**state)
                
                # check for equality
                self.assertAlmostEqual(double_pendulum.pendulum1.vx
                                       , expected_output[0][0], 10)
                self.assertAlmostEqual(double_pendulum.pendulum1.vy
                                       , expected_output[0][1], 10)
                self.assertAlmostEqual(double_pendulum.pendulum2.vx
                                       , expected_output[1][0], 10)
                self.assertAlmostEqual(double_pendulum.pendulum2.vy
                                       , expected_output[1][1], 10)

if __name__ == '__main__':
    unittest.main(verbosity=1)