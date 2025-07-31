import numpy as np

from types import MethodType, FunctionType

from particle import Particle
from integrations import RungeKuttaIntegrator
 

class PendulumSimulator:

    def __init__(self):
        pass

    def run_simulation(self, particle: Particle
                           , propagator: MethodType|FunctionType
                           , timestep: float):
        '''
            Calculates the path of the pendulum

            :param rhsFunc: a function defining the rhs of the EOM, given
                            the projectile state.  
        '''
        # initialize result lists
        self.time = np.array([0], dtype=np.float32)
        self.x = np.array([particle.x], dtype=np.float32)
        self.y = np.array([particle.y], dtype=np.float32)
        
        # local variables for simulation
        time = 0
        state = np.array([particle.theta, particle.w]
                         , dtype=np.float32)
        
        func = self.single_pendulum_dynamics

        while self.time[-1] <= 5:
            # update time and state
            time, state = propagator(rhsFunc=func
                                      , time=time
                                      , state=state
                                      , timestep=timestep)
            # reset particle properties
            new_position = np.array([particle.r, state[0]])
            new_velocity = np.array([0, state[1]])

            particle.set_position(position=new_position, coord_sys='polar')
            particle.set_velocity(velocity=new_velocity, coord_sys='polar')

            # append results to result lists
            self.time = np.append(self.time, time)
            self.x = np.append(self.x, particle.x)
            self.y = np.append(self.y, particle.y)

        return (self.time, self.x, self.y)

    def single_pendulum_dynamics(self, state: np.ndarray):
        '''
            Function defines the RHS of a single pendulum
            :param state: the present particle state
        '''
        theta, w = state
        r = 1
        thetaDerivative = w
        wDerivative = - 9.82 * np.cos(theta) / r

        return np.array([thetaDerivative, wDerivative]
                         , dtype=np.float32)
    
if __name__ == '__main__':

    my_pendulum = Particle(mass=1)
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