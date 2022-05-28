from matplotlib import pyplot as plt
import numpy as np
import csv
from scipy import signal

def normalise(dat):
    ref = np.mean(dat[:20])
    for i in range(len(dat)):
        dat[i] -= ref
    return dat

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


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
# name = 'hole1/Tue-Feb-1-15.37.19-2022_data' # go with chop pointing towards the hole so it gets stuck in, very god result
# name = 'hole1/Tue-Feb-1-16.44.36-2022_data' # same as before with hole detection

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
    # index_nums = [0,7,8,9,14]
    n_trim = 10
    for i in range(len(new_skin_data)):
        if i in index_nums:
            # plt.plot(time[n_trim:-n_trim], smooth(new_skin_data[i],20)[n_trim:-n_trim], label=i)
            plt.plot(time, new_skin_data[i], label=i)
            # plt.plot(sample_nb, smooth(normalise(new_skin_data[i]),20), label=i)
            # plt.plot(sample_nb, new_skin_data[i], label=i)
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor data")
    plt.legend()

    plt.figure()
    plt.xlabel("Time (s)")
    plt.ylabel("Robot hand positions")
    for i in range(len(new_pos_data)):
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

    for i in range(len(new_skin_data)):
        if i == 0:
            # np.random.seed(0)
            # time_step = .01
            # time_vec = np.arange(0, 70, time_step)
            # # A signal with a small frequency chirp
            # sig = np.sin(0.5 * np.pi * time_vec * (1 + .1 * time_vec))
            # freqs, times, spectrogram = signal.spectrogram(sig)

            # freqs, times, spectrogram = signal.spectrogram(smooth(new_skin_data[i],20))
            freqs, times, spectrogram = signal.spectrogram(new_skin_data[i])
            # plt.figure(figsize=(5, 4))
            plt.figure()
            plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower')
            plt.title('Spectrogram for sensor {}'.format(i))
            plt.ylabel('Frequency band')
            plt.xlabel('Time window')
            # plt.ylim(0.5, 10)
            plt.tight_layout()

    plt.show()


plot_data(name, pinch_state=False)

