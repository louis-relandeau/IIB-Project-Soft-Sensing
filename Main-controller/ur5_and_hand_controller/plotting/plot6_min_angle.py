from os import fsencode
from turtle import pos
from matplotlib import pyplot as plt
import numpy as np
import csv
from scipy import signal

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def butter_lowpass(cutoff, nyq_freq, order=4):
    normal_cutoff = float(cutoff) / nyq_freq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
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

    new_skin_data = new_skin_data *5/(2**16) /1.4*100 + 37.5

    ys = new_pos_data[1]
    N = 40
    trim = N//2

    # l = list(zip(ys, new_skin_data[0]))
    # l.sort()
    # # 'unzip'
    # ys, new_skin_data[0] = zip(*l)

    # plt.figure()
    # plt.plot(time, ys)

    # plt.figure()
    # plt.plot(time, new_skin_data[0])
    # plt.plot(time[trim:-trim], smooth(new_skin_data[0], N)[trim:-trim])
    
    sensors = np.linspace(0,15,num=16,dtype=int)
    sensors = [14,3,7,0]
    col = ["green","red","orange","blue"]
    # sensor = 0
    freq = []
    for i in range(len(time)-1):
        freq.append(1/(time[i+1]-time[i]))
    # plt.figure()
    # plt.title('Frequncies')
    # plt.plot(freqs)
    fs = np.mean(freq)
    print(fs)

    thresh = -0.1867 # skips 1st two, too small anyway
    coef = np.polyfit(time, ys, 1)
    poly1d_fn = np.poly1d(coef) # better than horizontal threshold
    below = False
    ind = []
    ind_times = []
    ind.append(0)
    ind_times.append(time[0])
    for i in range(len(ys)):
        if ys[i] < poly1d_fn(time[i]) and below == False:
            ind.append(i)
            ind_times.append(time[i])
            below = True
        elif ys[i] > poly1d_fn(time[i]) and below == True:
            ind.append(i)
            ind_times.append(time[i])
            below = False
    ind.append(len(time))
    ind_times.append(time[-1])



    # plt.figure()
    # plt.plot(time, ys)
    # # plt.hlines(thresh, xmin=time[0], xmax=time[-1], colors='red')
    # plt.plot(time, poly1d_fn(time), '--k')
    # for l in ind_times:
    #     plt.vlines(l, ymin=min(ys), ymax=max(ys), colors='green')
    # plt.title('Position along Y')
    # plt.ylabel('Position (m)')
    # plt.xlabel('Time (s)')

    # averaged = np.zeros_like(ys)
    # for i in range(len(ind)-1):
    #     averaged[ind[i]:ind[i+1]] = np.mean(new_skin_data[sensor][ind[i]:ind[i+1]])
    # averaged_norm = np.zeros_like(ys)
    # for i in range(len(ind)-1):
    #     if i%2 == 0:
    #         try:
    #             averaged_norm[ind[i]:ind[i+1]] = abs(averaged[ind[i+1]] - averaged[ind[i]])
    #         except:
    #             pass
    #     else:
    #         averaged_norm[ind[i]:ind[i+1]] = 0

    # plt.figure()
    # plt.plot(time, averaged, label='averaged')
    # plt.legend()
    
    # plt.figure()
    # plt.plot(time, averaged_norm, label='norm')
    # plt.title('Sensor reading for increasing angle')
    # plt.ylabel('Pressure')
    # plt.xlabel('Time (s)')
    # # plt.legend()

    fig, ax = plt.subplots()

    ax.plot(time, ys, '--', color='black',linewidth=0.5, label=' Y displacement')
    ax.set_ylabel("Hand Position (mm)", fontsize=15)
    ax.set_xlabel('Time (s)', fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)

    ax2=ax.twinx()
    for i in range(len(sensors)):
        # ax.plot(time, new_skin_data[0], label='raw')
        # plt.plot(time[trim:-trim], smooth(new_skin_data[0], N)[trim:-trim], label='smoothed')
        filtered = butter_lowpass_filter(new_skin_data[sensors[i]],1,2*fs) # fs as last arg
        # plt.plot(range(len(filtered)),filtered)
        if i == 0:
            ax2.plot(time,filtered, label = "Sensor # {}".format(sensors[i]),color=col[i])
        else:
            ax2.plot(time,filtered, label = "{}".format(sensors[i]),color=col[i])
        # ax.title('Sensor data')
    ax2.set_ylabel('Sensor Pressure (kPa)', fontsize=15)
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    # ax.legend(loc='lower left')

    plt.tight_layout()
    lgd = fig.legend(ncol = 3, bbox_to_anchor = (0.5,-0.14), loc='lower center', fontsize=15)
    lgd.set_in_layout(True)
    fig.savefig('min_angle_', bbox_extra_artists=(lgd,), bbox_inches='tight')

        
    # ax2.set_ylim(top = -0.175)

    # freqs, times, spectrogram = signal.spectrogram(ys, fs=fs)
    # plt.figure()
    # plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower', extent=[times[0],times[-1],freqs[0],freqs[-1]])
    # plt.title('Spectrogram for position')
    # plt.ylabel('Frequency band')
    # plt.xlabel('Time window')
    # plt.ylim(0, 1)

    # plt.pcolormesh(times, freqs, spectrogram, shading='auto')
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')

    # freqs, times, spectrogram = signal.spectrogram(new_skin_data[sensor])
    # plt.figure()
    # plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower')
    # plt.title('Spectrogram for unfiltered sensor {}'.format(sensor))
    # plt.ylabel('Frequency band')
    # plt.xlabel('Time window')
    # plt.ylim(0, 20)

    # freqs, times, spectrogram = signal.spectrogram(filtered, fs=fs)
    # plt.figure()
    # plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower', extent=[times[0],times[-1],freqs[0],freqs[-1]])
    # plt.title('Spectrogram for filtered sensor {}'.format(sensor))
    # plt.ylabel('Frequency band')
    # plt.xlabel('Time window')
    # plt.ylim(0, 1)



   
    plt.show()

plot_data(name, pinch_state=False)





