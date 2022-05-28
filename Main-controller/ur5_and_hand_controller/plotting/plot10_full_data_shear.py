from cmath import pi
from random import sample
from re import S
from matplotlib import pyplot as plt
import numpy as np
import csv
from scipy import signal

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

def smooth2(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def butter_lowpass(cutoff, nyq_freq, order=4):
    normal_cutoff = float(cutoff) / nyq_freq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
    y = signal.filtfilt(b, a, data)
    return y


name = 'shear1/Tue-May-24-13.51.30-2022_data'
name = 'shear1/Tue-May-24-18.55.37-2022_data'

def plot_data(name):
    skin_data = []
    time = []
    pos_data = []
    pinch_data = []
    coords = ['x','y','z','rx','ry','rz']

    with open('Generic_ur5_controller/data/' + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            # print(row)
            if n > 1:
                skin_data.append(row[14:21])
                time.append(row[1])
                pos_data.append(row[2:8])
            else:
                n+=1

    time = list(map(float, time))

    new_skin_data = []
    new_pos_data = []
    for i in range(len(skin_data)):
        new_skin_data.append(list(map(float, skin_data[i])))
        new_pos_data.append(list(map(float, pos_data[i])))

    new_skin_data = np.transpose(new_skin_data)
    new_pos_data = np.transpose(new_pos_data)

    sample_nb = np.linspace(1,len(time),len(time))

    plt.figure()
    index_nums = np.linspace(0,6,num=7,dtype=int)
    # index_nums = [0,7,8,9,14]
    # index_nums = [0,1,2,3,4,5,6,7,8,9,11,12,13,14,15]
    # index_nums = [2,3,8,9,14,15]
    n_trim = 25
    for i in range(len(new_skin_data)):
        if i in index_nums:
            # plt.plot(time[n_trim:-n_trim], smooth2(new_skin_data[i],50)[n_trim:-n_trim], label=i)
            
            plt.plot(time, new_skin_data[i], label=i)
            # plt.plot(time, butter_lowpass_filter(new_skin_data[i],1,5), label=i)
            # plt.plot(sample_nb, smooth2(normalise(new_skin_data[i]),20), label=i)
            # plt.plot(sample_nb, new_skin_data[i], label=i)
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor data") 
    plt.legend()


    vlines = [3.24,6.55,9.24,12.55,15.24,18.55,21.24,24.55,27.24]
    vlines = []
    for v in vlines:
        plt.vlines(v,11400,11800)

    plt.figure()
    plt.xlabel("Time (s)")
    plt.ylabel("Robot hand positions")
    for i in range(len(new_pos_data)):
        # plt.plot(time, new_pos_data[i])
        # plt.plot(sample_nb, new_pos_data[i], label=coords[i])
        plt.plot(time, new_pos_data[i], label=coords[i])
        plt.legend()
        # Put a nicer background color on the legend.
        # legend.get_frame().set_facecolor('C0')

    plt.show()

    # np.savetxt('smoothed_data', 
    # smooth2(normalise(new_skin_data[i]),20),
    # delimiter =",", 
    # fmt ='% s')
    # plt.savefig('Generic_ur5_controller/' + name + '.png')


plot_data(name)
