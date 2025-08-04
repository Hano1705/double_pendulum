import matplotlib.pyplot as plt
import seaborn; seaborn.set_theme()
import numpy as np

from matplotlib import animation

from simulator import PendulumSimulator
from simulator import DoublePendulumSimulation
from pendulum import Pendulum
from pendulum import DoublePendulum

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

    def initialize_animation(self):
        '''
            Initializes the animation of the projectile
        '''
        # name variables for brevity
        t, x, y = self.t, self.x, self.y

        # globalise plot variables
        #global fig, ax, pendulum, trace

        self._fig, self._ax = plt.subplots()

        # set axis limits
        x0, y0 = self.pendulum.origin
        width = self.pendulum.length*1.5
        self._ax.set_xlim(left=x0-width, right=x0+width)
        self._ax.set_ylim(bottom=y0-width, top=y0+width)

        # axis labels
        self._ax.set_xlabel('x (m)')
        self._ax.set_ylabel('y (m)')

        # set ax as square
        self._ax.set_aspect('equal', adjustable='box')

        # define artists for projectile and path plotting
        self._pendulum, = self._ax.plot([x0, x[0]],[y0, y[0]]
                                       ,'o-', color='blue')
        self._trace, = self._ax.plot(x[0],y[0], color='red',alpha=0.3)

    def update_frame(self, frame):
        '''
            updates the frames for the projectile animation
            :param frame: the present frame
            :params x,y: the position coordinates of the full projectile path.
        '''
        # name variables for brevity
        t, x, y = self.t, self.x, self.y
        x0, y0 = self.pendulum.origin
        # update the pendulum plot
        self._pendulum.set_xdata(np.array([x0, x[frame]]))
        self._pendulum.set_ydata(np.array([y0, y[frame]]))

        # update trace plot
        if frame>100:
            self._trace.set_xdata(x[frame-100:frame])
            self._trace.set_ydata(y[frame-100:frame])
        else:
            self._trace.set_xdata(x[:frame])
            self._trace.set_ydata(y[:frame])

        return (self._pendulum, self._trace)

    def showProjectileAnimation(self):
        '''
            shows the projectile animation
        '''
        # initialize animation
        self.initialize_animation()

        # instantiate animation
        ani = animation.FuncAnimation(fig=self._fig, func=self.update_frame, 
                                    frames=len(self.t), interval=20, repeat_delay=1000)
        plt.show()

class DoublePendulumAnimation():
    '''
        A class for double pendulum animations.
    '''
    def __init__(self, simulation: DoublePendulumSimulation
                 , double_pendulum: DoublePendulum):
        '''
            Initializes the animation object, given the results of a projectile simulation
        '''
        self.t = simulation.time
        self.x1 = simulation.x1
        self.y1 = simulation.y1
        self.x2 = simulation.x2
        self.y2 = simulation.y2

        self.double_pendulum = double_pendulum

    def initialize_animation(self):
        '''
            Initializes the animation of the projectile
        '''
        # name variables for brevity
        t, x1, y1, x2, y2 = self.t, self.x1, self.y1, self.x2, self.y2

        self._fig, self._ax = plt.subplots()

        # set axis limits
        x0, y0 = self.double_pendulum.pendulum1.origin
        width = self.double_pendulum.pendulum1.length*2*1.5
        self._ax.set_xlim(left=x0-width, right=x0+width)
        self._ax.set_ylim(bottom=y0-width, top=y0+width)

        # axis labels
        self._ax.set_xlabel('x (m)')
        self._ax.set_ylabel('y (m)')

        # set ax as square
        self._ax.set_aspect('equal', adjustable='box')

        # define artists for projectile and path plotting
        self._pendulum_artist, = self._ax.plot([x0, x1[0], x2[0]]
                                            ,[y0, y1[0], y2[0]]
                                            ,'o-', color='blue')
        self._trace_artist, = self._ax.plot(x2[0],y2[0], color='red',alpha=0.3)
        self._text_artist = self._ax.text(0.1, 0.9, s=f"t = {t[0]:.1f} s"
                              , transform=self._ax.transAxes
                              , bbox={'facecolor':'green','alpha':0.2})

    def update_frame(self, frame):
        '''
            updates the frames for the projectile animation
            :param frame: the present frame
            :params x,y: the position coordinates of the full projectile path.
        '''
        # name variables for brevity
        t, x1, y1, x2, y2 = self.t, self.x1, self.y1, self.x2, self.y2
        x0, y0 = self.double_pendulum.pendulum1.origin
        # update the pendulum plot
        self._pendulum_artist.set_xdata(np.array([x0, x1[frame], x2[frame]]))
        self._pendulum_artist.set_ydata(np.array([y0, y1[frame], y2[frame]]))

        # update trace plot
        tail_length = len(self.t)//10
        if frame>tail_length:
            self._trace_artist.set_xdata(x2[frame-tail_length:frame])
            self._trace_artist.set_ydata(y2[frame-tail_length:frame])
        else:
            self._trace_artist.set_xdata(x2[:frame])
            self._trace_artist.set_ydata(y2[:frame])

        # update text
        self._text_artist.set_text(s=f"t = {t[frame]:.1f} s")

        return (self._pendulum_artist, self._trace_artist)

    def show_projectile_animation(self):
        '''
            shows the projectile animation
        '''
        # initialize animation
        self.initialize_animation()

        # instantiate animation
        ani = animation.FuncAnimation(fig=self._fig, func=self.update_frame, 
                                    frames=len(self.t), interval=20, repeat_delay=1000)
        plt.show()


if __name__ == '__main__':

    # instantiate the two pendula making up the double pendulum
    pendulum1 = Pendulum(mass=0.1, length=1, origin=[0,0])
    pendulum2 = Pendulum(mass=0.1, length=1)
    # instantiate the double pendulum
    double_pendulum = DoublePendulum(pendulum1=pendulum1, pendulum2=pendulum2)
    double_pendulum.set_double_pendulum(theta1=4*np.pi/6, w1=0,
                                       theta2=-np.pi/6, w2=0)
    print("double pendulum instantiated")
    
    rk_solver = RungeKuttaIntegrator()

    my_simulation = DoublePendulumSimulation()
    my_simulation.run_simulation(double_pendulum=double_pendulum
                                , propagator=rk_solver.propagate_state
                                , simulation_time=10
                                , timestep=0.02)
    print('finished simulation')
    my_animation = DoublePendulumAnimation(simulation=my_simulation
                                        , double_pendulum=double_pendulum)
    my_animation.show_projectile_animation()
    print('finished animation')