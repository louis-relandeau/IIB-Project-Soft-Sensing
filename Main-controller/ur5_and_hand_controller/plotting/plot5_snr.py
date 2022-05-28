from matplotlib import pyplot as plt
import numpy as np
import csv
from scipy import signal
from scipy.stats import norm

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def normalise(dat):
    ref = np.mean(dat[:20])
    for i in range(len(dat)):
        dat[i] -= ref
    return dat

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

name = 'min_angle1/Thu-Feb-3-14.53.20-2022_data'

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
    index_nums = [0]
    n_trim = 25
    for i in range(len(new_skin_data)):
        if i in index_nums:
            plt.plot(time[n_trim:-n_trim], smooth(new_skin_data[i],50)[n_trim:-n_trim], label=i)
            # plt.plot(time, new_skin_data[i], label=i)
            # plt.plot(sample_nb, smooth(normalise(new_skin_data[i]),20), label=i)
            # plt.plot(sample_nb, new_skin_data[i], label=i)
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor data")
    plt.legend()

    plt.figure()
    plt.xlabel("Time (s)")
    plt.ylabel("Robot hand positions")
    for i in range(len(new_pos_data)):
        # plt.plot(time, new_pos_data[i])
        # plt.plot(sample_nb, new_pos_data[i], label=coords[i])
        plt.plot(time, new_pos_data[i], label=coords[i])
        plt.legend()

    if pinch_state:
        plt.figure()
        plt.plot(time, pinch_data)
        plt.xlabel("Time (s)")
        plt.ylabel("Pinch state")

    filtered = butter_highpass_filter(new_skin_data[index_nums[0]],10,21.281274703115496)
    plt.figure()
    plt.plot(range(len(filtered)),filtered)
    plt.title('filtered signal')

    plt.figure()
    n, bins, patches = plt.hist(filtered, bins=50, density=True, facecolor='g', alpha=0.75)
    (mu, sigma) = norm.fit(filtered)
    # print('Mean is: ' + str(mu) + ' standard deviation is: ' + str(sigma))
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, norm.pdf(x, mu, sigma))

    plt.xlabel('Sensor noise')
    plt.ylabel('Probability')
    plt.grid(True)

    plt.show()

    arr = new_skin_data[0]
    snr = signaltonoise(arr)
    print(snr)

plot_data(name, pinch_state=False)





