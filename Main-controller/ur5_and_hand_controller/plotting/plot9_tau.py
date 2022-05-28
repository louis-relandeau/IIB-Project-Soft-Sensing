from cmath import pi
import random
from re import S
from matplotlib import colors, pyplot as plt
import numpy as np
import csv
from scipy import signal, optimize
from scipy.optimize import curve_fit
from matplotlib.ticker import StrMethodFormatter

def butter_lowpass(cutoff, nyq_freq, order=4):
    normal_cutoff = float(cutoff) / nyq_freq
    b, a = signal.butter(order, normal_cutoff, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, cutoff_freq, nyq_freq, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    b, a = butter_lowpass(cutoff_freq, nyq_freq, order=order)
    y = signal.filtfilt(b, a, data)
    return y

name = 'tau1/Wed-Feb-23-18.25.15-2022_data'
# name = 'tau1/Wed-Feb-23-18.44.03-2022_data'
name = 'tau2/Wed-Feb-23-18.54.15-2022_data'
# name = 'tau1/Thu-Feb-24-20.48.56-2022_data'
name = 'tau2/Fri-Feb-25-14.04.22-2022_data'                 # time decay
# name = 'recording_impulse/Fri-Feb-25-14.33.20-2022_data'    # step response
# name = 'tau2/Fri-Feb-25-14.04.22-2022_data'

########################################
skin_data = []
time = []
pos_data = []
pinch_data = []
coords = ['x','y','z','rx','ry','rz']
pinch_state = False

with open('Generic_ur5_controller/data/' + name + '.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    n = 0
    for row in csvreader:
        # print(row)
        if n > 1:
            skin_data.append(row[14:15])
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

cst = -65.5 # step response
cst = -67.9 # time decay

new_skin_data = new_skin_data *5/(2**16) /1.4*100 + cst
# time = (np.array(time) - 49)*1000 # step response
time = (np.array(time) - 135) # time decay

###################################################

# trim1 = 9346
# # trim1 = 11000
# trim2 = 46832

# trim1 = 8500
# trim2 = 47500 # for time decay

# x = time[trim1:trim2]
# # start = x[0]
# # x = np.array(x) - start
# y = new_skin_data[0][trim1:trim2]

# # m = 100
# # x, y = zip(*random.sample(list(zip(x, y)), m))
# x = np.array(x)
# y = np.array(y)

# def func(x, a, b, c):
#     return a * np.exp(-b * x) + c

# # popt, pcov = curve_fit(func, x, y, maxfev=5000)
# fit_x = []
# fit_y = []
# with open('fit.csv', newline='') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         # print(row)
#         fit_x.append(float(row[0]))
#         fit_y.append(float(row[1]))

# print(type(fit_x[10]))

# plt.figure()

# plt.plot(x, y, 'ko', label="my data")
# plt.plot(fit_x, fit_y, label="Fitted Curve")
# # plt.plot(x, func(x, *popt), 'r-', label="Fitted Curve")
# # print(*popt)
# # plt.plot(x,func(x,35,0.007,12650), label="Fitted Curve")
# plt.legend()
# plt.show()


# # p = func(x,35,0.007,12650)
# # with open('saving_data.csv', 'w', newline='') as csvfile:
# #         csvwriter = csv.writer(csvfile)
# #         for i in range(len(x)):
# #             csvwriter.writerow([x[i]+start, p[i]])

# # determine quality of the fit
# squaredDiffs = np.square(y - func(x,35,0.007,12650))
# squaredDiffsFromMean = np.square(y - np.mean(y))
# rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
# print(f"R² = {rSquared}")

###################################################

trim1 = 8500
trim2 = 47500 # for time decay
# trim1 = 9346
# trim2 = 46832

# trim1 = 3066
# trim2 = 3085 # for step response

x = time[trim1:trim2]
y = new_skin_data[0][trim1:trim2]
x = np.array(x)
y = np.array(y)

# x = np.array(time)
# y = np.array(new_skin_data)

fit_x = []
fit_y = []
with open('fit.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        fit_x.append(float(row[0])-135)
        fit_y.append(float(row[1]))
        
fit_y = np.array(fit_y) *5/(2**16) /1.4*100 + cst

fig, ax1 = plt.subplots()
index_nums = np.linspace(0,15,num=16,dtype=int)
index_nums = [0]
for i in range(len(new_skin_data)):
    if i in index_nums:
        ax1.plot(x, y, color = 'orange', label='sensor pressure')

ax1.plot(fit_x, fit_y, label="exponential decay fit", color='red') # for time decay
ax1.set_xlabel("Time (s)", fontsize=20)
ax1.set_ylabel("Sensor Gauge Pressure (kPa)", fontsize=20) 
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
# plt.hlines(12650*5/(2**16) /1.4*100 + cst,xmin=30,xmax=95)
# plt.hlines(12000*5/(2**16) /1.4*100 + cst,xmin=95,xmax=320)
# plt.vlines(95, ymin=12000*5/(2**16) /1.4*100 + cst, ymax=12650*5/(2**16) /1.4*100 + cst, label='pinching state')
# plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))
ax1.set_ylim(ymin=12400*5/(2**16) /1.4*100 + cst, ymax=12900*5/(2**16) /1.4*100 + cst)

ax2=ax1.twinx()
ax2.set_ylabel("Fingertip Position (mm)", fontsize=20)
ax2.plot(time[trim1:trim2], new_pos_data[0][trim1:trim2], label='fingertip position',color='tab:blue')
ax2.set_ylim(ymin=-0.69, ymax=-0.58)
plt.yticks(fontsize=20)

# lgd = fig.legend(ncol = 3, bbox_to_anchor = (0.5,0.85), loc='upper right', fontsize=20)
# lgd.set_in_layout(True)
# fig.savefig('time_decay_', bbox_extra_artists=(lgd,), bbox_inches='tight')

fig.legend(loc='upper right', bbox_to_anchor = (0.9,0.875), fontsize=20)
fig.savefig('time_decay_', bbox_inches='tight')
# fig.savefig('step_response_', bbox_inches='tight')

plt.show()


