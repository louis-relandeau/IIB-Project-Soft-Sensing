from matplotlib import pyplot as plt
import numpy as np
import csv
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

def butter_lowpass(cutoff, nyq_freq, order=4):
    normal_cutoff = float(cutoff) / nyq_freq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
    y = signal.filtfilt(b, a, data)
    return y

name = 'demo_IROS_hole/Sun-Mar-6-11.44.19-2022_data' # pick
# name = 'demo_IROS_hole/Sun-Mar-6-10.58.45-2022_data' # hole

def plot_data(name, pinch_state=False):
    skin_data = []
    time = []
    pos_data = []
    pinch_data = []
    coords = ['x','y','z','rx','ry','rz']

    # for hole:
    start = 18
    end = 45

    # for pick:
    start = 0
    end = 100000

    with open('Generic_ur5_controller/data/' + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            # print(row)
            if n > 1 and float(row[1])>=start and float(row[1])<=end:
                skin_data.append(row[14:30])
                time.append(row[1])
                pos_data.append(row[2:5]) #replace 5 by 8 to add rotations
                if pinch_state:
                    pinch_data.append(row[-1])
            else:
                n+=1

    time = np.array(list(map(float, time)))
    time = time - time[0]

    new_skin_data = []
    new_pos_data = []
    for i in range(len(skin_data)):
        new_skin_data.append(list(map(float, skin_data[i])))
        new_pos_data.append(list(map(float, pos_data[i])))

    new_skin_data = np.transpose(new_skin_data)
    new_pos_data = np.transpose(new_pos_data)

    ######################################

    fig, ax1 = plt.subplots()
    index_nums = np.linspace(0,15,num=16,dtype=int)
    # index_nums = [0,7,8,9,14]
    # index_nums = [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15]
    # index_nums = [2,3,8,9,14,15]
    index_nums = [7,9,12,3,6,5]
    cmap = matplotlib.cm.get_cmap('hot')
    sp = np.linspace(0,1,10)
    colors = [cmap(s) for s in sp]

    for i in range(len(index_nums)):
        ax1.plot(time, new_skin_data[index_nums[i]], label=index_nums[i], color=colors[i])
            # plt.plot(time, butter_lowpass_filter(new_skin_data[i],1,5), label=i)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Sensor data")
    ax1.set_ylim(ymin=12750, ymax=13300) #ymax=13200 for hole

    cmap = matplotlib.cm.get_cmap('winter')
    sp = np.linspace(0,1,3)
    colors = [cmap(s) for s in sp]
    ax2 = plt.twinx(ax1)
    ax2.set_ylabel("Robot hand positions")
    for i in range(len(new_pos_data)):
        ax2.plot(time, new_pos_data[i], label=coords[i], color=colors[i])
    ax2.set_ylim(ymin=-0.75,ymax=3)
    
    fig.legend(loc='upper center', ncol = 3, bbox_to_anchor=[0.5, 0.95])
    fig.tight_layout()
    plt.show()

    fps=len(time)/time[-1]
    print(fps)

    # ################################
    
    x_data = []
    y7_data = [] #    index_nums = [7,9,12,3,6,5]
    y9_data = []
    y12_data = []
    y3_data = []
    y6_data = []
    y5_data = []
    posx_data = []
    posy_data = []
    posz_data = []

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Raw sensor data")
    margin = 1
    ax1.set_xlim(-margin, time[-1]+margin)
    ax1.set_ylim(ymin=12750, ymax=13300) #ymax=13200 for hole
    cmap = matplotlib.cm.get_cmap('hot')
    sp = np.linspace(0,1,10)
    colors = [cmap(s) for s in sp]
    line7, = ax1.plot(0, 0, label='sensor 7', color = colors[0])
    line9, = ax1.plot(0, 0, label='sensor 9', color = colors[1])
    line12, = ax1.plot(0, 0, label='sensor 12', color = colors[2])
    line3, = ax1.plot(0, 0, label='sensor 3', color = colors[3])
    line6, = ax1.plot(0, 0, label='sensor 6', color = colors[4])
    line5, = ax1.plot(0, 0, label='sensor 5', color = colors[5])

    ax2 = plt.twinx(ax1)
    ax2.set_ylabel("Robot hand positions (m)")
    cmap = matplotlib.cm.get_cmap('winter')
    sp = np.linspace(0,1,3)
    colors = [cmap(s) for s in sp]
    linex, = ax2.plot(0, 0, label='x pos', color = colors[0])
    liney, = ax2.plot(0, 0, label='y pos', color = colors[1])
    linez, = ax2.plot(0, 0, label='z pos', color = colors[2])
    ax2.set_ylim(ymin=-0.75,ymax=3)

    fig.legend(loc='upper center', ncol = 3, bbox_to_anchor=[0.5, 0.95])
    fig.tight_layout()


    def animation_frame(i):
        x_data.append(time[i])

        y7_data.append(new_skin_data[7][i]) #    index_nums = [7,9,12,3,6,5]
        y9_data.append(new_skin_data[9][i])
        y12_data.append(new_skin_data[12][i])
        y3_data.append(new_skin_data[3][i])
        y6_data.append(new_skin_data[6][i])
        y5_data.append(new_skin_data[5][i])

        posx_data.append(new_pos_data[0][i])
        posy_data.append(new_pos_data[1][i])
        posz_data.append(new_pos_data[2][i])

        line7.set_xdata(x_data)
        line9.set_xdata(x_data)
        line12.set_xdata(x_data)
        line3.set_xdata(x_data)
        line6.set_xdata(x_data)
        line5.set_xdata(x_data)

        linex.set_xdata(x_data)
        liney.set_xdata(x_data)
        linez.set_xdata(x_data)

        line7.set_ydata(y7_data)
        line9.set_ydata(y9_data)
        line12.set_ydata(y12_data)
        line3.set_ydata(y3_data)
        line6.set_ydata(y6_data)
        line5.set_ydata(y5_data)

        linex.set_ydata(posx_data)
        liney.set_ydata(posy_data)
        linez.set_ydata(posz_data)
        return line7, line9, line12, line3, line6, line5, linex, liney, linez,

    animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, len(time), 1), interval=10)
    animation.save('Generic_ur5_controller/data/' + name + '.mp4', fps=len(time)/time[-1]) 
    # fps lower for the hole detection so divide by 30/25=1.2 --- (fps=len(time)/time[-1])
    plt.show()
    

plot_data(name, pinch_state=False)

