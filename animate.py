import box_class
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation, rc
from matplotlib import patches


class Animate:
    def __init__(self, box):
        if type(box) == box_class.Box:
            box = [box]
        self.box = box
        self.fig, self.axs = plt.subplots(nrows=2, ncols=1, figsize=(12, 10),
                                          gridspec_kw={'height_ratios': [5, 2],
                                                       'wspace': 0.4,
                                                       'hspace': 0.4})
        self.set_axis_limit()
        self.time = []
        self.inf = []
        self.sus = []
        self.rec = []
        self.borders = []
        self.colormap = np.array(['g', 'r', 'b'])
        scatter = []
        for b in box:
            scatter.append(self.axs[0].scatter([], []))
        line_inf, =  self.axs[1].plot(
            [], [], color=self.colormap[1], label='Infected')
        line_sus, =  self.axs[1].plot(
            [], [], color=self.colormap[0], label='Susceptible')
        line_rec, =  self.axs[1].plot(
            [], [], color=self.colormap[2], label='Recovered')
        handles, labels = self.axs[1].get_legend_handles_labels()
        self.fig.legend(handles, labels, loc='upper right')
        lines = [line_sus, line_inf, line_rec]
        self.plots = [scatter, lines]
        self.add_borders()
        self.axs[0].set_title("Simulation")
        self.axs[1].set_title("Trend")
        self.reach_time = -1

    def __simulate(self):
        for i in range(len(self.box)):
            if self.box[i].sim_type == 'comm':
                self.__simulate_common(i)
            else:
                self.__simulate_normal(i)
            # if(self.box[i].now >= 5 and self.box[i].now<=5.1):
            # print("updating")
            #self.box[i].pos = tuple(map(sum, zip(self.box[i].pos, (1,1))))
            # self.box[i].set_dest_bounds()
        # self.set_borders()
        # self.set_axis_limit()
        
    def __simulate_normal(self,i):
        if np.absolute((np.round(self.box[i].p_xy - (self.box[i].p_dest), 2)) <= np.full((2, self.box[i].num), 0.5)).all():
            self.box[i].set_normal_dest(1)
        self.box[i].update_infection(0.25)
        self.box[i].update_recovered(50)
        self.box[i].move_to_dest(0.05)

    def __simulate_common(self,i):
        if self.box[i].now == 0:
            self.box[i].set_common_dest()

        if np.absolute((np.round(self.box[i].p_xy - (self.box[i].p_dest), 2)) <= np.full((2, self.box[i].num), 1)).all() and self.reach_time == -1:
            self.box[i].set_initial_dest()
            self.reach_time = self.box[i].now

        self.box[i].update_infection(0.2)
        self.box[i].update_recovered(50)
        if self.box[i].now - self.reach_time <= 5 and self.reach_time != -1:
            self.box[i].inc_time()
        else:
            self.box[i].move_to_dest(0.05)
            # print(2)
        if np.absolute((np.round(self.box[i].p_xy - (self.box[i].p_dest), 2)) <= np.full((2, self.box[i].num), 1)).all() and self.reach_time != -1:
            self.box[i].set_sim_type('normal')

    def __animate(self, i):
        self.__simulate()
        inf_c = 0
        rec_c = 0
        sus_c = 0
        for i in range(len(self.box)):
            self.plots[0][i].set_offsets(self.box[i].p_xy.T)
            self.plots[0][i].set_color(self.colormap[self.box[i].p_state])
            inf_c += self.box[i].inf_c
            rec_c += self.box[i].rec_c
            sus_c += self.box[i].sus_c
        self.time.append(self.box[0].now)
        self.inf.append(inf_c)
        self.sus.append(sus_c)
        self.rec.append(rec_c)
        if self.box[0].now+2 >= self.axs[1].get_xlim()[1]:
            self.axs[1].set_xlim((0, self.box[0].now+52))
        self.plots[1][1].set_data(self.time, self.inf)
        self.plots[1][0].set_data(self.time, self.sus)
        self.plots[1][2].set_data(self.time, self.rec)
        return self.plots

    def run(self):
        anim = animation.FuncAnimation(self.fig, self.__animate, interval=1)
        plt.show()

    def add_borders(self):
        for b in self.box:
            p = patches.Rectangle(
                b.pos, b.size[0], b.size[1], fill=False, color='black', lw=2)
            self.axs[0].text(b.pos[0], b.pos[1]+b.size[1], b.name,
                             horizontalalignment='left', verticalalignment='bottom')
            self.borders.append(self.axs[0].add_artist(p))

    def set_borders(self):
        for i in range(len(self.box)):
            self.borders[i].set_xy(self.box[i].pos)

    def set_axis_limit(self):
        self.axs[0].axis('square')
        pos = []
        pos_max = []
        y1_max = 0
        for b in self.box:
            y1_max += b.num
            pos.append(b.pos)
            pos_max.append(tuple(map(sum, zip(b.pos, b.size))))
        pos_ar = np.array(pos).T
        pos_m_ar = np.array(pos_max).T
        x_min = min(pos_ar[0])
        y_min = min(pos_ar[1])
        x_max = max(pos_m_ar[0])
        y_max = max(pos_m_ar[1])
        self.axs[0].set_xlim(
            (x_min-0.02*(x_max-x_min), x_max+0.02*(x_max-x_min)))
        self.axs[0].set_ylim(
            (y_min-0.03*(x_max-x_min), y_max+0.03*(x_max-x_min)))
        self.axs[1].set_xlim((0, 50))
        self.axs[1].set_ylim((-5, y1_max+5))
