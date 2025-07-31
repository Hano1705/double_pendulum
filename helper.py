import numpy as np

def calculate_angle(x:float|int, y:float|int, offset: float|int = 0):
    '''
        helper function, computes angle from cartesian coordinates
    '''
    if x > 0 and y > 0:
        return np.arctan(y / x) - offset
    elif x < 0 and y > 0:
        return np.pi - np.arctan(y / np.abs(x)) - offset
    elif x < 0 and y < 0:
        return np.pi + np.arctan(y / x) - offset
    elif x > 0 and y < 0:
        return 2*np.pi + np.arctan(y / x) - offset
    elif x == 0 and y != 0:
        return np.sign(y) * np.pi / 2 - offset
    elif x > 0 and y == 0:
        return 0 - offset
    elif x < 0 and y == 0:
        return np.pi - offset
    else:
        raise ValueError("Angle ill-defined for (x,y)=(0,0)")