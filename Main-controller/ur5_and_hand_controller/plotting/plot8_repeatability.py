from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import csv, copy
from scipy import signal

def normalise(dat):
    ref = np.mean(dat[:5])
    for i in range(len(dat)):
        dat[i] -= ref
    return dat

def butter_lowpass(cutoff, nyq_freq, order=4):
    normal_cutoff = float(cutoff) / nyq_freq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
    y = signal.filtfilt(b, a, data)
    return y

name = 'repeatability/Wed-Feb-23-13.32.39-2022_data'
name = 'repeatability/Wed-Feb-23-17.02.43-2022_data'
name = 'repeatability/Wed-Feb-23-17.33.51-2022_data' # nice
# name = 'repeatability/Fri-Feb-25-15.19.45-2022_data' # trim in half

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

    # index_nums = [2,3,8,9,14,15]
    # distances = []
    # for points in new_skin_data:
    #     dists = []
    #     for i in range(len(points)):
    #         for j in range(len(points)):
    #             if i != j and i in index_nums and j in index_nums:
    #                 dists.append(abs(points[i]-points[j]))
    #     distances.append(np.mean(dists))

    new_skin_data = np.transpose(new_skin_data)
    new_pos_data = np.transpose(new_pos_data)

    new_skin_data = new_skin_data *5/(2**16) /1.4*100 - 69.05

    # diffs = np.zeros_like(new_skin_data)
    # for j in range(len(diffs)):
    #     for i in range(len(diffs[j])-1):
    #         diffs[j][i+1] = new_skin_data[j][i+1] - new_skin_data[j][i]

    
    start, end = 0, len(new_skin_data[0]) # 75 start at 3.5s
    # start, end = 32012, 32266

    inds = []
    dat = copy.copy(new_skin_data[14])
    toggle = False
    thresh = 0.75 #12800 when raw data, 0.975 when voltage, 100.75 when pressure, 0.75 for gauge pressure
    for i in range(len(dat)): 
        if dat[i] >= thresh and toggle == False:
            toggle = True
            inds.append(i)
        if dat[i] < thresh and toggle == True:
            toggle = False
    # print(len(inds))


    plt.figure()
    index_nums = np.linspace(0,15,num=16,dtype=int)
    index_nums = [14,15,3,2,8,9]
    index_nums = [14]
    for i in index_nums:
        plt.plot(time[start:end], new_skin_data[i][start:end], label=i)

    # for j in range(500):
    #     plt.vlines(j*4.021+start, ymin = 12600, ymax=13100)
    # for j in range(len(inds)):
    #     plt.vlines(time[inds[j]], ymin = 12600, ymax=13100, colors='tab:orange')
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Sensor Gauge Pressure (kPa)", fontsize=20) 
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.tight_layout()

    cut = 80
    samples = np.linspace(0,cut-1,num=cut,dtype=int)
    mse = []

    cmap = matplotlib.cm.get_cmap('coolwarm')
    plt.figure()
    ax = plt.subplot()
    for i in index_nums:
        for j in range(len(inds)-1):
            # print(j)
            # plt.plot(samples, normalise(new_skin_data[i][inds[j]-10:inds[j]+70]), label=i)
            # if j >= 450:
            ax.plot(samples, new_skin_data[i][inds[j]-10:inds[j]+70], color=cmap(j/500))
            difference_array = abs(np.subtract(new_skin_data[i][inds[j]-10:inds[j]+70], new_skin_data[i][inds[-2]-10:inds[-2]+70])) /  new_skin_data[i][inds[-2]-10:inds[-2]+70] # error percentage
            squared_array = np.square(difference_array)
            mse.append(difference_array.mean())
    plt.xlabel("Samples", fontsize=20)
    plt.ylabel("Sensor Gauge Pressure (kPa)", fontsize=20) 
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    # plt.legend(fontsize=20)
    plt.tight_layout()

    # fig, ax = plt.subplots(figsize=(1.5, 5))
    # fig.subplots_adjust(bottom=0.5)
    # norm = matplotlib.colors.Normalize(vmin=0, vmax=500)
    # cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap,
    #                                 norm=norm,
    #                                 orientation='vertical')
    # cb1.set_label('Iteration number', fontsize=20)
    # plt.yticks(fontsize=20)
    # plt.tight_layout()

    # print(mse)
    plt.figure()
    plt.plot(mse)
    plt.xlabel("Iterations", fontsize=20)
    plt.ylabel("Mean Squared Error", fontsize=20) 
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    # plt.legend(fontsize=20)
    plt.tight_layout()


    # plt.figure()
    # index_nums = np.linspace(0,15,num=16,dtype=int)
    # index_nums = [2,3,8,9,14,15]
    # plt.plot(time[start:end], distances[start:end], '--', color='black')
    # for i in range(len(diffs)):
    #     if i in index_nums:
    #         plt.plot(time[start:end], butter_lowpass_filter(diffs[i],5,21)[start:end], label=i)
    #         plt.xlabel("Time (s)")
    # plt.ylabel("Sensor data - change") 
    # plt.legend()

    # plt.figure()
    # plt.xlabel("Time (s)")
    # plt.ylabel("Robot hand positions")
    # for i in range(len(new_pos_data)):
    #     # plt.plot(time, new_pos_data[i])
    #     # plt.plot(sample_nb, new_pos_data[i], label=coords[i])
    #     plt.plot(time, new_pos_data[i], label=coords[i])
    #     plt.legend()

    plt.show()

plot_data(name)
