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
        
    def set_angular_velocity(self, w: float|int, set_cart: bool=True):
        '''
            Set angular velocity, also sets cartesian velocity.
            -----------------------
            Parameters:
            -----------------------
            w: angular velocity.
        '''
        self.w = w
        if set_cart == True:
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

    def set_double_pendulum(self, theta1: float|int, w1: float|int
                            , theta2: float|int, w2: float|int):
        '''
            Sets upper pendulum, as well as origin for lower pendulum
            
            Parameters:
            ----------------
            theta1:  upper pendulum angle
            w1:      upper pendulum angular velocity
            theta2:  lower pendulum angle
            w2:      lower pendulum angular velocity
        '''
        # set upper pendulum
        self.pendulum1.set_angle(theta = theta1)
        self.pendulum1.set_angular_velocity(w = w1)
        # set lower pendulum origin
        xp1, yp1 = self.pendulum1.x, self.pendulum1.y 
        self.pendulum2.set_origin([xp1, yp1])
        # set lower pendulum
        self.pendulum2.set_angle(theta = theta2)
        self.pendulum2.set_angular_velocity(w = w2, set_cart=False)
        self.pendulum2.vx = (self.pendulum1.vx 
                             + self.pendulum2.length*self.pendulum2.w
                             *np.cos(self.pendulum2.theta) )
        self.pendulum2.vy = (self.pendulum1.vy 
                             + self.pendulum2.length*self.pendulum2.w
                             *np.sin(self.pendulum2.theta) )


if __name__ == '__main__':
    # instantiate the two pendula making up the double pendulum
    pendulum1 = Pendulum(mass=1, length=1, origin=[0,0])
    pendulum2 = Pendulum(mass=1, length=1)
    # instantiate the double pendulum
    double_pendulum = DoublePendulum(pendulum1=pendulum1, pendulum2=pendulum2)
    double_pendulum.set_double_pendulum(theta1=np.pi/4, w1=0
                                        , theta2=np.pi/6, w2=0)
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