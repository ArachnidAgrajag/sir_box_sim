import numpy as np
import math
from numpy.random import default_rng
from matplotlib import pyplot as plt
from matplotlib import animation, rc
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
        self.p_state= np.empty((1,0),int)

    def add_people(self,num,inf):
        unique = [""]
        for xy in self.p_xy.T:
            unique.append(str(round(xy[0], 4))+"+"+str(round(xy[1], 4)))
        x_list = []
        y_list = []
        state_l = []
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
                i += 1
        self.num = self.num + num
        self.p_xy = np.append(self.p_xy,[x_list,y_list],axis=1)
        self.p_state = np.append(self.p_xy,state_l,axis=1)
    
    def move_people(self, displacement):
        bounce = lambda x, l, u:u - abs(u-l-x % (2*(u-l)))
        self.p_xy[0] = bounce(self.p_xy[0] + displacement[0],self.pos[0],self.pos[0]+self.size[0])
        self.p_xy[1] = bounce(self.p_xy[1] + displacement[1],self.pos[1],self.pos[1]+self.size[1]) 
    