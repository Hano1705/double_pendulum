import numpy as np

from types import MethodType, FunctionType

from particle import Particle
from integrations import RungeKuttaIntegrator
 

class PendulumSimulator:

    def __init__(self):
        pass

    def simulateProjectile(self, particle: Particle
                           , propagator: MethodType|FunctionType
                           , timestep: float):
        '''
            Calculates the path of the pendulum

            :param rhsFunc: a function defining the rhs of the EOM, given
                            the projectile state.  
        '''
        # initialize result lists
        self.time = [0]
        self.x = [particle.position[0]]
        self.y = [particle.position[1]]

        self.vx = [particle.velocity[0]]
        self.vy = [particle.velocity[1]]
        
        # local variables for simulation
        time = 0
        state = np.array([self.x[0], self.y[0], self.vx[0], self.vy[0]]
                         , dtype=np.float32)
        
        func = self.single_pendulum_dynamics(state=state)_

        while particle.position[1] >= 0:
            # update time and state
            time, state = propagator(rhsFunc=func
                                      , time=time
                                      , state=state
                                      , timestep=timestep)
            # reset particle properties
            particle.position = [state[0], state[1]]
            particle.velocity = [state[2], state[3]]

            # append results to result lists
            self.time.append(time)
            self.x.append(state[0])
            self.y.append(state[1])
            self.vx.append(state[2])
            self.vy.append(state[3])

        return (self.time, self.x, self.y, self.vx, self.vy)

    def single_pendulum_dynamics(self, state: np.ndarray):
        '''
            Function defines the RHS of a single pendulum
            :param state: the present particle state
        '''
        x0, y0, vx0, vy0 = state

        xDerivative = vx0
        yDerivative = vy0
        vxDerivative = 0
        vyDerivative = -9.82

        return np.array([xDerivative,yDerivative,vxDerivative,vyDerivative]
                         , dtype=np.float32)
    
if __name__ == '__main__':
    import particle
    import integrations

    myProjectile = particle.Particle()
    myProjectile.setParameters(position=[0,1], velocity=[1,2]
                               , mass=1, cDrag=0.47, area=0.01)
    
    rkSolver = integrations.RungeKuttaIntegrator()

    mySimulation = ProjectileSimulator()
    mySimulation.simulateProjectile(particle=myProjectile
                                    , propagator=rkSolver.propagateState
                                    , particleDynamics='drag'
                                    , timestep=0.01)
    print('finished simulation')