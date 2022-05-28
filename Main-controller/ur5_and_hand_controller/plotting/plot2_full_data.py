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


name = 'index_fingertip_table/1move'
name = 'cam2/Fri-Nov-19-15.27.33-2021_0_data'
name = 'chopstick-angle-change-with-pictures-offset-c4/combined' # this one has no position change it seems
name = 'test6-varying-hand-angle-c5-testing/combined' # sus
name1 = 'pick-up/Thu-Dec-2-09.15.14-2021_data' # interesting to plot spectrum of a typical pick up
name2 = 'empty-open-close/Thu-Dec-2-09.33.19-2021_data' # plot next to the above and compare, then can be used for segmentation#
name = 'rerun_chop4\combined\combined_old'
# name = 'rerun_chop4\combined_removed_base_pos_trimmed'
# name = 'rerun_chop4\combined\combined'
# name = 'rerun_chop4\Mon-Dec-20-11.55.08-2021_data' # data points could be trimmed to remove start and end but shouldn't matter
# name = 'contour1\Mon-Jan-31-16.08.56-2022_data' # best run?
# name = 'cantilever1/Tue-Jan-25-15.27.19-2022_data'
name = 'hole1/Mon-Jan-31-17.39.48-2022_data'
name = 'hole1/Mon-Jan-31-17.56.51-2022_data' # it's around 8s somewhere
# name = 'hole1/Mon-Jan-31-17.57.27-2022_data' # same
# name = 'hole1/Mon-Jan-31-17.58.04-2022_data' # same
# name = 'hole1/Mon-Jan-31-18.06.03-2022_data' # this is using a very large hole
# name = 'hole1/Mon-Jan-31-18.09.35-2022_data' # small variation considering object
# name = 'hole1/Tue-Feb-1-15.37.19-2022_data' # go with chop pointing towards the hole so it gets stuck in, good result
# name = 'hole1/Tue-Feb-1-16.44.36-2022_data' # same as before with hole detection
# name = 'contour2/Wed-Feb-2-17.58.00-2022_data'
# name = 'speed1/Thu-Feb-3-14.10.17-2022_data'
# name = 'min_angle1/Thu-Feb-3-14.53.20-2022_data'
# name = 'contour3/Fri-Feb-4-15.29.01-2022_data'
name = 'hole2/Tue-Feb-8-17.11.29-2022_data' # small holes
# name = 'hole2/Tue-Feb-8-17.08.31-2022_data' # large holes
name = 'hole2/Wed-Feb-9-13.59.47-2022_data' # 5-9mm
name = 'hole2/Wed-Feb-9-14.08.55-2022_data' # 9.5-13.5mm
name = 'hole2/Fri-Feb-11-13.55.05-2022_data' # 9.5-13.5mm very good all 9
name = 'hole2/Fri-Feb-11-13.58.25-2022_data' # even better
name = 'hole2/Fri-Feb-11-13.59.27-2022_data' # nice
name = 'hole2/32.5/Mon-Feb-21-12.53.15-2022_data' #calibrate vlines
name = 'tau1/Wed-Feb-23-18.15.28-2022_data'
name = 'orientation-repeat/Fri-Feb-25-18.26.34-2022_data'
name = 'demo_IROS_hole/Sun-Mar-6-11.44.19-2022_data'

def plot_data(name, pinch_state=False):
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
                skin_data.append(row[14:30])
                time.append(row[1])
                pos_data.append(row[2:8])
                if pinch_state:
                    pinch_data.append(row[-1])
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
    index_nums = np.linspace(0,15,num=16,dtype=int)
    index_nums = [0,7,8,9,14]
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

    if pinch_state:
        plt.figure()
        plt.plot(time, pinch_data)
        plt.xlabel("Time (s)")
        plt.ylabel("Pinch state")

    plt.show()

    # np.savetxt('smoothed_data', 
    # smooth2(normalise(new_skin_data[i]),20),
    # delimiter =",", 
    # fmt ='% s')
    # plt.savefig('Generic_ur5_controller/' + name + '.png')

def find_range(name, pinch_state=False):

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
                skin_data.append(row[14:30])
                time.append(row[1])
                pos_data.append(row[2:8])
                if pinch_state:
                    pinch_data.append(row[-1])
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

    # make data:
    np.random.seed(1)
    x = np.linspace(1,16,num=16,dtype=int)
    means = []
    errs = [[],[]]
    for i in range(len(x)):
               
        means.append(np.mean(smooth2(normalise(new_skin_data[i]),20)))
        errs[0].append(abs(np.min(smooth2(normalise(new_skin_data[i]),20))))
        errs[1].append(np.max(smooth2(normalise(new_skin_data[i]),20)))

        # means.append(np.mean(normalise(new_skin_data[i])))
        # errs[0].append(abs(np.min(normalise(new_skin_data[i]))))
        # errs[1].append(np.max((normalise(new_skin_data[i]))))
    
    return x,means,errs
    # plt.savefig('Generic_ur5_controller/' + name + '.png')

plot_data(name, pinch_state=False)

# for the pick up exp:

# x1, y1, yerr1 = find_range(name1)
# x2, y2, yerr2 = find_range(name2)
# # print(yerr1)
# fig, ax = plt.subplots()
# ax.errorbar(x1, y1, yerr1, fmt='none', linewidth=2, capsize=6, label='with chopstick')
# ax.errorbar(x2, y2, yerr2, fmt='none', linewidth=2, capsize=6, label='without chopstick')
# ax.legend()
# plt.xlabel("Sensor number")
# plt.ylabel("Filtered and normalised pressure values")
# ax.set(xlim=(0, 17), xticks=np.arange(1, 17))
# plt.show()