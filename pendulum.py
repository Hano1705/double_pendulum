#######
#    This module defines the particle class
#######
import numpy as np
from helper import calculate_angle

class Particle():
    '''
        The particle class, with attributes corresponding to a particles physical state, and its features, such as mass.
    '''
    def __init__(self, mass: float|int = 1
                 , cDrag: float|int = 0
                 , area: float|int = 0):

        self.mass = mass
        self.cDrag = cDrag
        self.area = area

    def set_position(self, position: np.ndarray, coord_sys: str = 'cartesian'):
        '''
            Set particle position.
            -----------------------
            Parameters:

            position: np.ndarray of dimension (2,)
            coord_sys: coordinate system of input. Default: 'cartesian'
        '''
        if coord_sys.lower() == 'cartesian':
            self.x, self.y = position[0], position[1]
            try:
                self.theta =  calculate_angle(self.x, self.y)
                self.r = np.sqrt(self.x**2 + self.y**2)
            except ValueError:
                print("For (x,y)=(0,0), polar coordinates omitted.")

        elif coord_sys.lower() == 'polar':
            if position[0]==0:
                raise ValueError("r=0 is singular point in polar coordinates. Consider switching to cartesian, if this point is important.")
            else:
                self.r, self.theta = position[0], position[1]
                self.x = self.r * np.cos(self.theta)
                self.y = self.r * np.sin(self.theta)

        else:
            raise ValueError(f'Input either "cartesian" or "polar" for coord_sys. Your input: {coord_sys}')        
        
    def set_velocity(self, velocity: np.ndarray, coord_sys: str = 'cartesian'):
        '''
            Set particle position.
            -----------------------
            Parameters:

            velocity: np.ndarray of dimension (2,)
            coord_sys: coordinate system of input. Default: 'cartesian'
        '''
        try:
            if coord_sys.lower() == 'cartesian':
                self.vx, self.vy = velocity[0], velocity[1]
                self.vr = (self.x*self.vx + self.y*self.vy) / self.r
                self.w = (self.x*self.vy - self.y*self.vx) / self.r**2

            elif coord_sys.lower() == 'polar':
                self.vr, self.w = velocity[0], velocity[1]
                self.vx = (self.vr * np.cos(self.theta) 
                          - self.r * self.w * np.sin(self.theta))
                self.vy = (self.vr * np.sin(self.theta) 
                          + self.r * self.w * np.cos(self.theta))
            else:
                raise ValueError(f'Input either "cartesian" or "polar" for coord_sys. Your input: {coord_sys}')
            
        except NameError:
            return "Set position before velocity"

    def set_properties(self, mass: int|float
                      , cDrag: int|float = 0
                      , area: int|float = 0):
        '''
            Sets particle properties

            Parameters:
            -------------------------
            mass:   Particle mass  
            cDrag:  Particle drag coefficient
            area:   Particle reference area
        '''
        if type(mass) is not int|float:
            raise TypeError("mass must be a decimal number")
        if type(cDrag) is not int|float:
            raise TypeError("drag coefficient must be a decimal number")
        if type(area) is not int|float:
            raise TypeError("area must be a decimal number")
        
        self.mass = mass
        self.cDrag = cDrag
        self.area = area

if __name__ == '__main__':
    myParticle = Particle()