import numpy as np
import math
from numpy.random import default_rng
from matplotlib import pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
rg = default_rng(12345)


#state
#0 susceptible
#1 infected
#-1 recovered

#lower and upper bounds for the coordinates
x_lb=0.0
y_lb=0.0
y_ub=10.0
x_ub=10.0
size=100


def create_people():
    people =[]
    unique = [""]
    string = ""
    i=0
    while i<size:
        state = rg.choice([-1,0,1],p=[0,0.9,0.1])
        [x,y] = rg.uniform(low=x_lb,high=x_ub,size=2)
        string = str(round(x,4))+"+"+str(round(y,4))
        if string in unique:
            continue
        else:
            unique.append(string)
            i+=1
            people.append({'id':i,'state':state,'x':x,'y':y})
    return people


def move(people, displacement):
    bounce = lambda x,l,u : u - abs(u-l-x%(2*(u-l))) 
    for p,d in [(p,d) for p in people for d in displacement if p['id']==d['id']]:
        p['x']=bounce(p['x']+d['x'],x_lb,x_ub)
        p['y']=bounce(p['y']+d['y'],y_lb,y_ub)

def create_velocity():
    velocity=[]        
    for i in range(size):
        [vx,vy]=rg.normal(loc=0,scale=0.5,size=2)
        velocity.append({'id':i,'vx':vx,'vy':vy})
    return velocity

def calc_displacement(velocity,time):
    displacement=[]
    for v in velocity:
        displacement.append({'id':v['id'],'x':v['vx']*time, 'y':v['vy']*time})
    return displacement

def calc_infected_distance(people):
    dist=[]
    co_inf=[]
    co_sus=[]
    for i in people:
        if i['state']==1:
            for j in people:
                if j['state']==0:
                    co_inf.append(i['x'])
                    co_inf.append(i['y'])
                    co_sus.append(j['x'])
                    co_sus.append(j['y'])
                    dist.append({'id_inf':i['id'],'id_sus':j['id'],'distance':math.dist(co_inf,co_sus)})
                    co_inf.clear()
                    co_sus.clear()
    return dist
def counts(people):
    infected=[p for p in people if p['state']==1].count()
    susceptible = [p for p in people if p['state']==0].count()
    recovered = [p for p in people if p['state']==-1].count()
    return {'sus':susceptible,'inf':infected,'rec':recovered}

def calc_rad_inf(people):
    rad = 0.25
    x_cent = 0
    y_cent = 0
    x = 0
    y = 0
    radius_of_infection = []
    for i in people:
        if i['state']==1:
            x_cent = i['x']
            y_cent = i['y']
            for j in people:
                if j['state']==0:
                    x = j['x']
                    y = j['y']
                    if (x - x_cent)**2 + (y - y_cent)**2 <= rad**2:
                        radius_of_infection.append({'id_inf':i['id'],'id_sus':j['id']})
    return radius_of_infection                

def update_infection(people,radius_inf):
    size = len(radius_inf)
    num = int(0.5 * size)
    inf = rg.choice(radius_inf,size=num)
    for p,i in [(p,i) for p in people for i in inf if p['id']==i['id_sus']]:
        p['state']=1


people = create_people()
fig = plt.figure(figsize=(10,10))
ax = plt.axes(xlim=(x_lb, x_ub), ylim=(y_lb, y_ub))
scatter=ax.scatter([],[])


def simulate(i):
    velocity=create_velocity()
    time = 0.1
    rad=calc_rad_inf(people)
    #print(rad)
    update_infection(people,rad)
    move(people,calc_displacement(velocity,time))  

def animate(i):
    p_x=[]
    p_y=[]
    p_s=[]
    simulate(i)
    for p in people:
        p_x.append(p['x'])
        p_y.append(p['y']) 
        p_s.append(p['state'])
    points =np.column_stack((p_x,p_y))
    color = np.array(p_s)
    scatter.set_offsets(points)
    scatter.set_array(color)
    return scatter

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(fig, animate, interval=10,frames=10)
HTML(anim.to_html5_video())
