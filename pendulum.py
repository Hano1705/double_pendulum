#######
#    This module defines the pendulum
#######
import numpy as np
from functools import partial

from helper import calculate_angle
calculate_angle = partial(calculate_angle, offset= -np.pi/2)

class Pendulum():
    '''
        The pendulum class, with attributes corresponding to its physical features.
    '''
    def __init__(self, mass: float|int = 1
                 , length: float|int = 1
                 , origin: np.ndarray|list = np.array([0,0], dtype=np.float32)):

        self.mass = mass
        self.length = length
        if origin is list:
            self.origin = np.array(origin, dtype=np.float32)
        else:
            self.origin = origin

    def set_angle(self, theta: float|int):
        '''
            Set pendulum angle, also sets cartesian coordinates.
            -----------------------
            Parameters:

            theta: pendulum angle, starting from negative y-axis.
        '''
        self.theta = theta
        self.x = self.length * np.sin(self.theta) + self.origin[0]
        self.y = - self.length * np.cos(self.theta) + self.origin[1]
        
    def set_angular_velocity(self, w: float|int):
        '''
            Set angular velocity, also sets cartesian velocity.
            -----------------------
            Parameters:
            -----------------------
            w: angular velocity.
        '''
        self.w = w
        self.vx = self.length * self.w * np.cos(self.theta)
        self.vy = self.length * self.w * np.sin(self.theta)

    def set_properties(self, mass: int|float
                      , length: int|float):
        '''
            Sets particle properties

            Parameters:
            -------------------------
            mass:   Pendulum mass
            length: Pendulum length
        '''
        if type(mass) is not int|float:
            raise TypeError("mass must be a decimal number")
        if type(length) is not int|float:
            raise TypeError("length must be a decimal number")
        
        self.mass = mass
        self.length = length

if __name__ == '__main__':
    unit_pendulum = Pendulum(mass=1, length=1)
    unit_pendulum.set_angle(theta = np.pi/4)
    unit_pendulum.set_angular_velocity(w = np.pi)
    print('Pendulum has been created')