import numpy as np
import math
from numpy.random import default_rng
from matplotlib import pyplot as plt
from matplotlib import animation, rc
#from IPython.display import HTML
rg = default_rng(1234)

# state
# 0 susceptible
# 1 infected
# -1 recovered

# lower and upper bounds for the coordinates
x_lb = 0.0
y_lb = 0.0
y_ub = 10.0
x_ub = 10.0
size = 100


def create_people():
    people = []
    unique = [""]
    string = ""
    i = 0
    while i < size:
        state = rg.choice([-1, 0, 1], p=[0, 0.9, 0.1])
        [x, y] = rg.uniform(low=x_lb, high=x_ub, size=2)
        string = str(round(x, 4))+"+"+str(round(y, 4))
        if string in unique:
            continue
        else:
            unique.append(string)
            people.append({'id': i, 'state': state, 'x': x, 'y': y})
            i += 1
    return people


def move(people, displacement):
    def bounce(x, l, u): return u - abs(u-l-x % (2*(u-l)))
    for p, d in [(p, d) for p in people for d in displacement if p['id'] == d['id']]:
        p['x'] = bounce(p['x']+d['x'], x_lb, x_ub)
        p['y'] = bounce(p['y']+d['y'], y_lb, y_ub)


def create_velocity():
    velocity = []
    for i in range(size):
        [vx, vy] = rg.logistic(loc=0, scale=0.5, size=2)
        velocity.append({'id': i, 'vx': vx, 'vy': vy})
    return velocity


def create_duration():
    dur = []
    for i in range(size):
        v = rg.normal(loc=1, scale=0.5)
        dur.append({'id': i, 'd': v})
    return dur


def create_destination():
    dest = []
    for i in range(size):
        [x, y] = rg.uniform(low=0, high=10, size=2)
        dest.append({'id': i, 'x': x, 'y': y})
    return dest


def create_destination_solo(i, dest):
    #dest = []
    [x, y] = rg.uniform(low=0, high=10, size=2)
    for d in dest:
        if d['id'] == i:
            d.update({'id': i, 'x': x, 'y': y})
    # return dest


def calc_displacement_vel(velocity, time):
    displacement = []
    for v in velocity:
        displacement.append(
            {'id': v['id'], 'x': v['vx']*time, 'y': v['vy']*time})
    return displacement


def calc_displacement_dest(people, dest, dur, time):
    displacement = []
    for p, d, s in [(p, d, s) for p in people for d in dest for s in dur if d['id'] == s['id'] and d['id'] == p['id']]:
        displacement.append({'id': p['id'], 'x': (
            d['x']-p['x']) * time/s['d'], 'y': (d['y']-p['y']) * time/s['d']})
    return displacement


def calc_infected_distance(people):
    dist = []
    co_inf = []
    co_sus = []
    for i in people:
        if i['state'] == 1:
            for j in people:
                if j['state'] == 0:
                    co_inf.append(i['x'])
                    co_inf.append(i['y'])
                    co_sus.append(j['x'])
                    co_sus.append(j['y'])
                    dist.append(
                        {'id_inf': i['id'], 'id_sus': j['id'], 'distance': math.dist(co_inf, co_sus)})
                    co_inf.clear()
                    co_sus.clear()
    return dist


def counts(people):
    infected = len([p for p in people if p['state'] == 1])
    susceptible = len([p for p in people if p['state'] == 0])
    recovered = len([p for p in people if p['state'] == -1])
    return {'sus': susceptible, 'inf': infected, 'rec': recovered}


def calc_rad_inf(people):
    rad = 0.25
    x_cent = 0
    y_cent = 0
    x = 0
    y = 0
    radius_of_infection = []
    for i in people:
        if i['state'] == 1:
            x_cent = i['x']
            y_cent = i['y']
            for j in people:
                if j['state'] == 0 and j['x'] >= x_cent-rad and j['x'] <= x_cent+rad and j['y'] >= y_cent-rad and j['y'] <= y_cent+rad:
                    x = j['x']
                    y = j['y']
                    if (x - x_cent)**2 + (y - y_cent)**2 <= rad**2:
                        radius_of_infection.append(
                            {'id_inf': i['id'], 'id_sus': j['id']})
    return radius_of_infection


def update_infection(people, radius_inf):
    size = len(radius_inf)
    num = int(0.5 * size)
    inf = rg.choice(radius_inf, size=num)
    for p, i in [(p, i) for p in people for i in inf if p['id'] == i['id_sus']]:
        p['state'] = 1


people = create_people()
people_init = people.copy()
dest = create_destination()
""" fig = plt.figure(figsize=(10,10))
ax = plt.axes(xlim=(x_lb, x_ub), ylim=(y_lb, y_ub))
scatter=ax.scatter([],[]) """
fig, axs = plt.subplots(2, 1)
axs[0].set_xlim((x_lb, x_ub))
axs[0].set_ylim((y_lb, y_ub))
axs[1].set_xlim((0, 30))
axs[1].set_ylim((0, 110))
scatter = axs[0].scatter([], [])
line, =  axs[1].plot([], [], color='red')
plots = [scatter, line]


def simulate_vel(i):
    velocity = create_velocity()
    time = 0.1
    rad = calc_rad_inf(people)
    # print(rad)
    update_infection(people, rad)
    move(people, calc_displacement_vel(velocity, time))


def simulate_dest():
    p_x = []
    d_x = []
    p_y = []
    d_y = []
    destsr = dest
    """ for p in people:
        p_x.append((round(p['x'],2),p['id']))
        p_y.append((round(p['y'],2),p['id'])) """
    """for p in destsr:
        d_x.append((round(p['x'],2),p['id']))
        d_y.append((round(p['y'],2),p['id']))"""
    #print(list(map(lambda x,y,x1,y1: x==x1 and y==y1,p_x,p_y,d_x,d_y)))
    # print(d_x[0],p_x[0],d_y[0],p_y[0])
    """  if all(map(lambda x,y,x1,y1: x==x1 and y==y1,p_x,p_y,d_x,d_y)):
        destsr = create_destination() """
    for i, j in [(i, j) for i in destsr for j in people if round(j['x'], 2) == round(i['x'], 2) and round(j['y'], 2) == round(i['y'], 2) and j['id'] == i['id']]:
        create_destination_solo(i['id'], dest)

    dur = create_duration()
    dt = 0.08
    rad = calc_rad_inf(people)
    update_infection(people, rad)

    move(people, calc_displacement_dest(people, destsr, dur, dt))


time = []
inf = []


def animate(i):
    p_x = []
    p_y = []
    p_s = []
    simulate_dest()
    for p in people:
        p_x.append(p['x'])
        p_y.append(p['y'])
        p_s.append(p['state'])
    points = np.column_stack((p_x, p_y))
    color = np.array(p_s)
    plots[0].set_offsets(points)
    plots[0].set_array(color)
    count = counts(people)
    time.append(i)
    inf.append(count['inf'])
    # print(time)
    if i+100 >= axs[1].get_xlim()[1]:
        axs[1].set_xlim((0, i+500))

    plots[1].set_data(time, inf)
    return plots

#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

anim = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
#HTML(anim.to_html5_video())
