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
            Sets pendulum properties

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

    def set_origin(self, origin: np.ndarray|list):
        '''
            Sets pendulum origin (hang-point)
        
            Parameters:
            -------------------------
            origin: Pendulum hang-point
        '''

        if type(origin) is list:
            self.origin = np.array(origin, dtype=np.float32)
        else:
            self.origin = origin


class DoublePendulum():
    '''
        A double pendulum, consisting of two coupled pendulum objects.
    '''
    def __init__(self, pendulum1: Pendulum, pendulum2: Pendulum):
        
        self.pendulum1 = pendulum1
        self.pendulum2 = pendulum2

    def set_upper_pendulum(self, theta: float|int, w: float|int):
        '''
            Sets upper pendulum, as well as origin for lower pendulum
            
            Parameters:
            ----------------
            theta:  upper pendulum angle
            w:      upper pendulum angular velocity
        '''
        # set upper pendulum
        self.pendulum1.set_angle(theta = theta)
        self.pendulum1.set_angular_velocity(w = w)
        # set lower pendulum origin
        xp1, yp1 = self.pendulum1.x, self.pendulum1.y 
        self.pendulum2.set_origin([xp1, yp1])

    def set_lower_pendulum(self, theta: float|int, w: float|int):
        '''
            Sets lower pendulum angle and angular velocity
            
            Parameters:
            ----------------
            theta:  lower pendulum angle
            w:      lower pendulum angular velocity
        '''
        # set lower pendulum
        self.pendulum2.set_angle(theta = theta)
        self.pendulum2.set_angular_velocity(w = w)


if __name__ == '__main__':
    # instantiate the two pendula making up the double pendulum
    pendulum1 = Pendulum(mass=1, length=1, origin=[0,0])
    pendulum2 = Pendulum(mass=1, length=1)
    # instantiate the double pendulum
    double_pendulum = DoublePendulum(pendulum1=pendulum1, pendulum2=pendulum2)
    double_pendulum.set_upper_pendulum(theta=np.pi/4, w=0)
    double_pendulum.set_lower_pendulum(theta=np.pi/6, w=0)
   

    print("double pendulum instantiated")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    x_points = [double_pendulum.pendulum1.origin[0]
                , double_pendulum.pendulum1.x
                , double_pendulum.pendulum2.x]
    y_points = [double_pendulum.pendulum1.origin[1]
                , double_pendulum.pendulum1.y
                , double_pendulum.pendulum2.y]
    
    double_pendulum_line, = ax.plot(x_points, y_points, 'o-')

    plt.show()
    print("double pendulum plotted")