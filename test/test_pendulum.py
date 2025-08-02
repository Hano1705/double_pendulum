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
            Tests the positions of the two pendula composing the double pendulum.
        '''
        input_upper_pendulum = [
            (1, [0,0], 0, 0),
        ]

        input_lower_pendulum = [
            (1, 0, 0)
        ]

        expected_output = [
            ()
        ]

        for case in test_cases:
            with self.subTest(case):
                # name test data
                input1, input2, expected_output = case
                # initiate double pendulum
                upper_pendulum = Pendulum(length=input1[0], origin=input1[1])
                lower_pendulum = Pendulum(length=input2[0])
                double_pendulum = DoublePendulum(pendulum1=upper_pendulum
                                                 , pendulum2=lower_pendulum)
                # set upper pendulum
                double_pendulum.set_upper_pendulum(theta=input1[2], w=input1[3])
                
                # check for equality
                self.assertAlmostEqual(pendulum.x, expected_output[0], 10)
                self.assertAlmostEqual(pendulum.y, expected_output[1], 10)

    def test_pendulum_angular_velocity(self):   
    

if __name__ == '__main__':
    unittest.main(verbosity=1)