import box_class
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation, rc
class Animate:
    def __init__(self,box):
        self.box=box
        self.fig, self.axs = plt.subplots(2,1)
        self.fig.set_size_inches(12,9)
        self.axs[0].set_xlim((self.box.pos[0], self.box.pos[0]+self.box.size[0]))
        self.axs[0].set_ylim((self.box.pos[1], self.box.pos[1]+self.box.size[1]))
        self.axs[1].set_xlim((0, 50))
        self.axs[1].set_ylim((-5, 110))
        self.colormap = np.array(['g', 'r', 'b'])
        scatter = self.axs[0].scatter([], [])
        line_inf, =  self.axs[1].plot([], [], color=self.colormap[1])
        line_sus, =  self.axs[1].plot([], [], color=self.colormap[0])
        line_rec, =  self.axs[1].plot([], [], color=self.colormap[2])
        lines = [line_sus,line_inf,line_rec]
        self.plots = [scatter, lines]
        self.time = []
        self.inf = []
        self.sus = []
        self.rec = []
        
    def __simulate(self):
        if np.absolute((np.round(self.box.p_xy - (self.box.p_dest),2)) <= np.full((2,self.box.num),0.5)).all():
           self.box.set_normal_dest()
        self.box.update_infection(0.5)
        self.box.update_recovered(50)
        self.box.move_to_dest(0.03)  

    def __animate(self,i):
        self.__simulate()
        self.plots[0].set_offsets(self.box.p_xy.T)
        self.plots[0].set_color(self.colormap[self.box.p_state])
        self.time.append(self.box.now)
        self.inf.append(self.box.inf_c)
        self.sus.append(self.box.sus_c)
        self.rec.append(self.box.rec_c)
        if self.box.now+2 >= self.axs[1].get_xlim()[1]:
            self.axs[1].set_xlim((0, self.box.now+52))
        self.plots[1][1].set_data(self.time,self.inf)
        self.plots[1][0].set_data(self.time,self.sus)
        self.plots[1][2].set_data(self.time,self.rec)
        return self.plots

    def run(self):
        anim=animation.FuncAnimation(self.fig, self.__animate, interval=1)
        plt.show()
        