import matplotlib.pyplot as plt
import seaborn; seaborn.set_theme()
import numpy as np

from matplotlib import animation

from simulator import PendulumSimulator
from particle import Particle
from integrations import RungeKuttaIntegrator

class ProjectileAnimation():
    '''
        A class for projectile animations.
    '''
    def __init__(self, simulation: PendulumSimulator
                 , particle: Particle):
        '''
            Initializes the animation object, given the results of a projectile simulation
        '''
        self.t = simulation.time
        self.x = simulation.x
        self.y = simulation.y

        self.particle = particle

    def initializeAnimation(self):
        '''
            Initializes the animation of the projectile
        '''
        # name variables for brevity
        t, x, y = self.t, self.x, self.y

        # globalise plot variables
        global fig, ax, pendulum, trace

        fig, ax = plt.subplots()

        # set axis limits
        ax.set_xlim(left=-2, right=2)
        ax.set_ylim(bottom=-2, top=2)

        # axis labels
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')

        # set ax as square
        ax.set_aspect('equal', adjustable='box')

        # define artists for projectile and path plotting
        pendulum = ax.plot([0,x[0]],[0,y[0]],'o-', color='blue')[0]
        trace = ax.plot(x[0],y[0], '-.', color='red',alpha=0.3)[0]

    def updateFrame(self, frame):
        '''
            updates the frames for the projectile animation
            :param frame: the present frame
            :params x,y: the position coordinates of the full projectile path.
        '''
        # name variables for brevity
        t, x, y = self.t, self.x, self.y

        # update the pendulum plot
        pendulum.set_xdata(np.array([0, x[frame]]))
        pendulum.set_ydata(np.array([0, y[frame]]))

        # update trace plot
        trace.set_xdata(x[:frame])
        trace.set_ydata(y[:frame])

        return (pendulum, trace)

    def showProjectileAnimation(self):
        '''
            shows the projectile animation
        '''
        # initialize animation
        self.initializeAnimation()

        # instantiate animation
        ani = animation.FuncAnimation(fig=fig, func=self.updateFrame, 
                                    frames=len(self.t), interval=20, repeat_delay=1000)
        plt.show()


if __name__ == '__main__':

    my_pendulum = Particle(mass=1)
    my_pendulum.set_position(position=np.array([1, 7 * np.pi / 4])
                            , coord_sys='polar')
    my_pendulum.set_velocity(velocity=np.array([0, 0])
                            , coord_sys='polar')
    
    rk_solver = RungeKuttaIntegrator()

    my_simulation = PendulumSimulator()
    my_simulation.run_simulation(particle=my_pendulum
                                    , propagator=rk_solver.propagateState
                                    , timestep=0.01)
    print('finished simulation')
    my_animation = ProjectileAnimation(simulation=my_simulation
                                      , particle=my_pendulum)
    my_animation.showProjectileAnimation()
    print('finished animation')