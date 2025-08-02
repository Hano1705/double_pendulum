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
        A test suite for the Pendulum class
    '''
    def test_pendulum_angle(self):

        test_cases= [
            [(1,[0,0],0), (0,-1)],
            [(2,[0,0],0), (0,-2)],
            [(1,[1,1],0), (1, 0)],
            [(1,[0,0], 2*np.pi), (0,-1)],
            [(0, [1,1], 0), (1,1)]
        ]
        for case in test_cases:
            with self.subTest(case):
                input, expected_output = case
                pendulum = Pendulum(length=input[0], origin=input[1])
                pendulum.set_angle(theta=input[2])
                
                self.assertAlmostEqual(pendulum.x, expected_output[0], 10)
                self.assertAlmostEqual(pendulum.y, expected_output[1], 10)
       
if __name__ == '__main__':
    unittest.main(verbosity=2)