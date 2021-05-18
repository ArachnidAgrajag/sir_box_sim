import box_class
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation, rc
class Animate:
    def __init__(self,box):
        self.box=box
        self.fig, self.axs = plt.subplots(2,1)
        self.axs[0].set_xlim((self.box.pos[0], self.box.pos[0]+self.box.size[0]))
        self.axs[0].set_ylim((self.box.pos[1], self.box.pos[1]+self.box.size[1]))
        self.axs[1].set_xlim((0, 50))
        self.axs[1].set_ylim((0, 110))
        scatter = self.axs[0].scatter([], [])
        line_inf, =  self.axs[1].plot([], [], color='red')
        #line_sus, =  self.axs[1].plot([], [], color='red')
        #line_rec, =  self.axs[1].plot([], [], color='red')
        #self.plots = [scatter, line_inf,line_rec,line_sus]
        self.plots = [scatter, line_inf]
        self.time = []
        self.inf = []
        self.sus = []
        self.rec = []
        
    def __simulate(self):    
        if (np.round(self.box.p_xy - (self.box.p_dest),2) == np.zeros((2,self.box.num))).all():
           self.box.set_normal_dest()
        self.box.update_infection(0.5)
        self.box.update_recovered(5)
        self.box.move_to_dest(0.1)  

    def __animate(self,i):
        self.__simulate()
        self.plots[0].set_offsets(self.box.p_xy.T) 
        self.plots[0].set_array(self.box.p_state)
        self.time.append(self.box.now)
        self.inf.append(self.box.inf_c)
        #self.sus.append(self.box.sus_c)
        #self.rec.append(self.box.rec_c)
        if self.box.now+40 >= self.axs[1].get_xlim()[1]:
            self.axs[1].set_xlim((0, self.box.now+500))
        self.plots[1].set_data(self.time,self.inf)
        return self.plots

    def run(self):
        anim=animation.FuncAnimation(self.fig, self.__animate, interval=1)
        plt.show()
        