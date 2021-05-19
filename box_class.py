import numpy as np
import math
from numpy.random import default_rng
#from IPython.display import HTML
rg = default_rng(1234)

class Box:
    def __init__(self,size,pos): 
        if type(size) == type(int):
            size = (size,size)
        self.size = size
        self.pos = pos
        self.num = 0
        self.p_xy = np.empty((2,0),float)
        self.p_state = np.empty(0,int)
        self.p_dest = np.empty((2,0),float)
        self.now = 0
        self.time_inf = np.empty(0,float)
        self.inf_c = 0
        self.sus_c = 0
        self.rec_c = 0

    def add_people(self,num,inf):
        unique = [""]
        for xy in self.p_xy.T:
            unique.append(str(round(xy[0], 4))+"+"+str(round(xy[1], 4)))
        x_list = []
        y_list = []
        state_l = []
        inf_time = []
        i = 0
        while i < num:
            state = rg.choice([0, 1], p=[1-inf,inf])
            x = rg.uniform(low=self.pos[0], high=self.pos[0]+self.size[0])
            y = rg.uniform(low=self.pos[1], high=self.pos[1]+self.size[1])
            string = str(round(x, 4))+"+"+str(round(y, 4))
            if string in unique:
                continue
            else:
                unique.append(string)
                x_list.append(x)
                y_list.append(y)
                state_l.append(state)
                if state == 1:
                    inf_time.append(0)
                else:
                    inf_time.append(-1)
                i += 1
        self.num = self.num + num
        self.p_xy = np.append(self.p_xy,[x_list,y_list],axis=1)
        self.p_state = np.append(self.p_state,state_l)
        self.time_inf= np.append(self.time_inf,inf_time)
    
    def move_people(self, displacement):
        bounce = lambda x, l, u:u - abs((u-l)- ((x-l) % (2*(u-l))))
        #bounce = lambda x, l, u: x
        self.p_xy[0] = bounce(self.p_xy[0] + displacement[0],self.pos[0],self.pos[0]+self.size[0])
        self.p_xy[1] = bounce(self.p_xy[1] + displacement[1],self.pos[1],self.pos[1]+self.size[1]) 
        self.now = self.now + 0.1

    def update_infection(self,rad):
        inf_id, = np.where(self.p_state == 1)
        sus_id, = np.where(self.p_state == 0)
        cur_inf=[]
        for i in inf_id:
            x_cent = self.p_xy[0][i]
            y_cent = self.p_xy[1][i]
            for j in sus_id:
                if self.p_xy[0][j]>=x_cent-rad and self.p_xy[0][j] <= x_cent+rad and self.p_xy[1][j]>=y_cent-rad and self.p_xy[1][j]<=y_cent+rad:
                    if (self.p_xy[0][j] - x_cent)**2 + (self.p_xy[1][j] - y_cent)**2 <= rad**2:
                        if j not in cur_inf:
                            cur_inf.append(j)
        for i in cur_inf:
            self.p_state[i]=rg.choice([0,1],p=[0.8,0.2]) #probability of infection
            if self.p_state[i] == 1:
                self.time_inf[i]=self.now
        self.counts()
    

    def set_normal_dest(self):
        dest_x = []
        dest_y = []
        for i in range(self.num):
            x = rg.normal(loc=self.p_xy[0][i], scale = rg.uniform(low=0,high=1))
            y = rg.normal(loc=self.p_xy[1][i], scale = rg.uniform(low=0,high=1))
            dest_x.append(x)
            dest_y.append(y)
        self.p_dest=np.array([dest_x,dest_y])
        self.set_dest_bounds()
    
    def move_to_dest(self,speed):
        scale = lambda x : x*speed
        disp = self.p_dest - self.p_xy
        self.move_people(scale(disp))
    
    def counts(self):
        unique,freq = np.unique(self.p_state,return_counts=True)
        none_to_zero = lambda x : 0 if len(x)==0 else x[0]
        self.inf_c = none_to_zero(freq[np.where(unique==1)])
        self.sus_c = none_to_zero(freq[np.where(unique==0)])
        self.rec_c = none_to_zero(freq[np.where(unique==2)])
        #print(self.inf_c,self.sus_c,self.rec_c)
    
    def update_recovered(self,time):
        inf_id, = np.where(self.p_state == 1)
        for i in inf_id:
            if self.now-self.time_inf[i]>=time: #time taken to recover 
                self.p_state[i]=rg.choice([1,2],p=[0.8,0.2]) #probability of recovery
        self.counts()    

    def print_val(self):
        print(self.p_xy,self.p_state,self.p_dest)
    
    def set_dest_bounds(self):
        bounce = lambda x, l, u:u - abs((u-l)- ((x-l) % (2*(u-l))))
        #bounce = lambda x, l, u: x
        self.p_dest[0] = bounce(self.p_dest[0],self.pos[0],self.pos[0]+self.size[0])
        self.p_dest[1] = bounce(self.p_dest[1],self.pos[1],self.pos[1]+self.size[1])
    
