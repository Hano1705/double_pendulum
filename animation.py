import matplotlib.pyplot as plt
import seaborn; seaborn.set_theme()
import numpy as np

from matplotlib import animation

from simulator import PendulumSimulator
from pendulum import Pendulum
from integrations import RungeKuttaIntegrator

class PendulumAnimation():
    '''
        A class for pendulum animations.
    '''
    def __init__(self, simulation: PendulumSimulator
                 , pendulum: Pendulum):
        '''
            Initializes the animation object, given the results of a projectile simulation
        '''
        self.t = simulation.time
        self.x = simulation.x
        self.y = simulation.y

        self.pendulum = pendulum

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
        x0, y0 = self.pendulum.origin
        width = self.pendulum.length*1.5
        ax.set_xlim(left=x0-width, right=x0+width)
        ax.set_ylim(bottom=y0-width, top=y0+width)

        # axis labels
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')

        # set ax as square
        ax.set_aspect('equal', adjustable='box')

        # define artists for projectile and path plotting
        pendulum = ax.plot([x0, x[0]],[y0, y[0]],'o-', color='blue')[0]
        trace = ax.plot(x[0],y[0], color='red',alpha=0.3)[0]

    def updateFrame(self, frame):
        '''
            updates the frames for the projectile animation
            :param frame: the present frame
            :params x,y: the position coordinates of the full projectile path.
        '''
        # name variables for brevity
        t, x, y = self.t, self.x, self.y
        x0, y0 = self.pendulum.origin
        # update the pendulum plot
        pendulum.set_xdata(np.array([x0, x[frame]]))
        pendulum.set_ydata(np.array([y0, y[frame]]))

        # update trace plot
        if frame>100:
            trace.set_xdata(x[frame-100:frame])
            trace.set_ydata(y[frame-100:frame])
        else:
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

    my_pendulum = Pendulum(mass=1, length=1, origin=[1,1])
    my_pendulum.set_angle(theta= np.pi /4)
    my_pendulum.set_angular_velocity(w = 0)
    
    rk_solver = RungeKuttaIntegrator()

    my_simulation = PendulumSimulator()
    my_simulation.run_simulation(pendulum=my_pendulum
                                , propagator=rk_solver.propagateState
                                , timestep=0.01)
    print('finished simulation')
    my_animation = PendulumAnimation(simulation=my_simulation
                                      , pendulum=my_pendulum)
    my_animation.showProjectileAnimation()
    print('finished animation')