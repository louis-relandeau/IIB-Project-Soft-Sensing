import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import csv

from numpy.core.fromnumeric import shape

path = 'Generic_ur5_controller/data/cam2/' 
name = 'Fri-Nov-19-15.27.33-2021_0_data'

def normalise(dat):
    ref = np.mean(dat[:20])
    for i in range(len(dat)):
        dat[i] -= ref
    return dat

def smooth(dat):
    kernel = 9
    new_dat = []
    for i in range(kernel):
        new_dat.append(dat[i])
    for i in range(len(dat)-2*kernel):
        new_dat.append(np.mean(dat[i:i+2*kernel+1]))
    for i in range(kernel):
        new_dat.append(dat[kernel-i])
    return new_dat

def get_time_pos_skin():
    skin_data = []
    time = []
    pos_data = []

    with open(path + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            if n > 0:
                time.append(row[1])
                pos_data.append(row[2:8])
                skin_data.append(row[14:30])
            else:
                n+=1

    time = list(map(float, time))

    new_skin_data = []
    new_pos_data = []
    for i in range(len(skin_data)):
        new_skin_data.append(list(map(float, skin_data[i])))
        new_pos_data.append(list(map(float, pos_data[i])))

    #new_skin_data = np.transpose(new_skin_data)
    new_pos_data = np.transpose(new_pos_data)

    return time, new_pos_data, new_skin_data

times, pos, skin = get_time_pos_skin()
print(shape(times[:1]))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 18), ylim=(-50, 450))
line, = ax.plot(times[:1], skin[:1], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data(times[:1], skin[:1])
    return line,

# animation function.  This is called sequentially
def animate(i):
    global times, skin
    # print(i)
    x = times[:i]
    print(shape(x))
    y = skin[:i]
    print(shape(y))
    # print(x,y)
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(times), interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

