import numpy as np
from functools import partial

from types import MethodType, FunctionType

from pendulum import Pendulum
from integrations import RungeKuttaIntegrator
 

class PendulumSimulator:

    def __init__(self):
        pass

    def run_simulation(self, pendulum: Pendulum
                           , propagator: MethodType|FunctionType
                           , timestep: float):
        '''
            Calculates the path of the pendulum

            :param rhsFunc: a function defining the rhs of the EOM, given
                            the projectile state.  
        '''
        # initialize result lists
        self.time = np.array([0], dtype=np.float32)
        self.x = np.array([pendulum.x], dtype=np.float32)
        self.y = np.array([pendulum.y], dtype=np.float32)
        
        # local variables for simulation
        time = 0
        state = np.array([pendulum.theta, pendulum.w]
                         , dtype=np.float32)
        
        func = partial(self.single_pendulum_dynamics, length=pendulum.length)

        while self.time[-1] <= 5:
            # update time and state
            time, state = propagator(rhsFunc=func
                                      , time=time
                                      , state=state
                                      , timestep=timestep)
            # reset pendulum position
            pendulum.set_angle(theta=state[0])
            pendulum.set_angular_velocity(w=state[1])

            # append results to result lists
            self.time = np.append(self.time, time)
            self.x = np.append(self.x, pendulum.x)
            self.y = np.append(self.y, pendulum.y)

        return (self.time, self.x, self.y)

    def single_pendulum_dynamics(self, state: np.ndarray, length: float|int):
        '''
            Function defines the RHS of a single pendulum
            :param state: the present particle state
        '''
        theta, w = state

        thetaDerivative = w
        wDerivative = - 9.82 * np.sin(theta) / length

        return np.array([thetaDerivative, wDerivative]
                         , dtype=np.float32)
    
if __name__ == '__main__':

    my_pendulum = Pendulum(mass=1, length=1, origin=np.array([0,0]))
    my_pendulum.set_position(position=np.array([1, 7*np.pi / 4])
                            , coord_sys='polar')
    my_pendulum.set_velocity(velocity=np.array([0, 0])
                            , coord_sys='polar')
    
    rk_solver = RungeKuttaIntegrator()

    my_simulation = PendulumSimulator()
    my_simulation.run_simulation(particle=my_pendulum
                                    , propagator=rk_solver.propagateState
                                    , timestep=0.01)
    print('finished simulation')