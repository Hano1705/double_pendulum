# --------------
# A script to define integrator classes
# --------------
import numpy as np
from types import FunctionType
class RungeKuttaIntegrator():
    '''
        A class of RK integrators to propagate newtonian particles
    '''
    def __init__(self):
        pass

    def propagateState(self, rhsFunc: FunctionType 
                       , time: float, state: np.ndarray 
                       , timestep: float) -> tuple:
        '''
            method for propagating a newtonian particle.
            
            :param rhsFunc: a function defining the rhs of the EOM, given
                            the projectile state.
            :param state: current state of the object to be propagated, passed
                          to rhsFunc.
            :param timestep: timestep of propagation

            Returns:
            ---------
            tuple: (float, np.ndarray)
        '''
        # calculate k1 and check that is is numpy array type
        k1 = rhsFunc(state)
        if type(k1) is not np.ndarray:
            raise TypeError(f"Your RHS function must return a numpy ndarray, yours returned: {type(rhsFunc(state))}")
        # calculate rest of Runge-Kutta parameters
        k2 = rhsFunc(state + timestep * k1/2)
        k3 = rhsFunc(state + timestep * k2/2)
        k4 = rhsFunc(state + timestep * k3)
        # final state
        state = state + timestep/6 * (k1 + 2*k2 + 2*k3 + k4)
        time = time + timestep

        return time, state