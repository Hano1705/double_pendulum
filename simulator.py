import numpy as np
from functools import partial

from types import MethodType, FunctionType

from pendulum import Pendulum
from pendulum import DoublePendulum
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
        '''
        theta, w = state

        thetaDerivative = w
        wDerivative = - 9.82 * np.sin(theta) / length

        return np.array([thetaDerivative, wDerivative]
                         , dtype=np.float32)
    
class DoublePendulumSimulation():
    '''
        A double pendulum simulator
    '''
    def __init__(self):
        pass
    
    def run_simulation(self, double_pendulum: DoublePendulum
                           , propagator: MethodType|FunctionType
                           , simulation_time: float|int
                           , timestep: float):
        '''
            Calculates the path of the pendulum

            :param rhsFunc: a function defining the rhs of the EOM, given
                            the projectile state.  
        '''
        # initialize result lists
        self.time = np.array([0], dtype=np.float32)
        self.x1 = np.array([double_pendulum.pendulum1.x], dtype=np.float32)
        self.y1 = np.array([double_pendulum.pendulum1.y], dtype=np.float32)
        self.x2 = np.array([double_pendulum.pendulum2.x], dtype=np.float32)
        self.y2 = np.array([double_pendulum.pendulum2.y], dtype=np.float32)

        # local variables for simulation
        time = 0
        state = np.array([double_pendulum.pendulum1.theta
                          , double_pendulum.pendulum2.theta
                          , double_pendulum.pendulum1.w
                          , double_pendulum.pendulum2.w]
                         , dtype=np.float32)
        
        # setting the function for the EOM 
        properties = np.array([double_pendulum.pendulum1.mass
                                , double_pendulum.pendulum2.mass
                                , double_pendulum.pendulum1.length
                                , double_pendulum.pendulum2.length]
                                , dtype=np.float32)

        func = partial(self.double_pendulum_dynamics, properties=properties)

        while self.time[-1] < simulation_time:
            # update time and state
            time, state = propagator(rhsFunc=func
                                      , time=time
                                      , state=state
                                      , timestep=timestep)
            # reset pendulum position
            double_pendulum.set_double_pendulum(theta1=state[0], w1=state[2]   
                                               , theta2=state[1], w2=state[3])

            # append results to result lists
            self.time = np.append(self.time, time)
            self.x1 = np.append(self.x1, double_pendulum.pendulum1.x)
            self.y1 = np.append(self.y1, double_pendulum.pendulum1.y)         
            self.x2 = np.append(self.x2, double_pendulum.pendulum2.x)
            self.y2 = np.append(self.y2, double_pendulum.pendulum2.y)
                                

    def double_pendulum_dynamics(self, state: np.ndarray
                                 , properties: np.ndarray):
        
        theta1, theta2, w1, w2 = state
        mass1, mass2, length1, length2 = properties
        
        # calculate alphas
        alpha1 = (length2 / length1 * mass2 / (mass1 + mass2)
                   * np.cos(theta1-theta2) )
        alpha2 = length1 / length2 * np.cos(theta1-theta2)
        # calculate fs
        f1 = (- length2/length1 * mass2/(mass1+mass2) 
              * w1**2 * np.sin(theta1-theta2) 
              - 9.82/length1 * np.sin(theta1)
                )
        f2 = (length1/length2 * w1**2 * np.sin(theta1-theta2)
              - 9.82/length2 * np.sin(theta2)
                )
        # calculate gs
        g1 = (f1 - alpha1*f2) / (1-alpha1*alpha2)
        g2 = (f2 - alpha2*f1) / (1-alpha1*alpha2)

        # define derivative of state variables
        deriv_theta1 = w1
        deriv_theta2 = w2
        deriv_w1 = g1
        deriv_w2 = g2

        return np.array([deriv_theta1, deriv_theta2, deriv_w1, deriv_w2]
                        , dtype=np.float32)
        
    
if __name__ == '__main__':

    # instantiate the two pendula making up the double pendulum
    pendulum1 = Pendulum(mass=1, length=1, origin=[0,0])
    pendulum2 = Pendulum(mass=1, length=1)
    # instantiate the double pendulum
    double_pendulum = DoublePendulum(pendulum1=pendulum1, pendulum2=pendulum2)
    double_pendulum.set_double_pendulum(theta1=np.pi/4, w1=0
                                       , theta2=np.pi/6, w2=0)
    print("double pendulum instantiated")
    
    rk_solver = RungeKuttaIntegrator()

    my_simulation = DoublePendulumSimulation()
    my_simulation.run_simulation(double_pendulum=double_pendulum
                                , propagator=rk_solver.propagateState
                                , simulation_time=10
                                , timestep=0.01)
    print('finished simulation')