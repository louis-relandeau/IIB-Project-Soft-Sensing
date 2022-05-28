from matplotlib import pyplot as plt
import numpy as np
import time

from pathlib import Path
import csv

# name = '_Thu-Nov-11-11.05.00-2021_0_data'
# name = '_Thu-Nov-11-11.12.59-2021_0_data'

name = '_Thu-Nov-11-11.42.47-2021_0_data'
# name = '_Thu-Nov-11-11.45.16-2021_0_data'
skin_data = []
times = []
with open('Generic_ur5_controller/csv_files/' + name + '.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        times.append(row[1])
        skin_data.append(row[-16:])

times = times[3:]
times = list(map(float, times))

skin_data = skin_data[3:]

bench = [skin_data[0]]
path = 'Generic_ur5_controller/plotting/' + 'vid5'
Path(path).mkdir(parents=True, exist_ok=True)

bench = (list(map(float, skin_data[0])))
for i in range(len(skin_data)):
    data = np.reshape(np.array(list(map(float, skin_data[i])))-bench, (4, 4))

    plt.imshow(data, interpolation='nearest', vmin=-50, vmax=150)
    plt.xticks(np.arange(0.0, 2.5, 1), np.arange(0.5, 2, 0.5))
    plt.yticks(np.arange(2, -0.5, -1), np.arange(0.5, 2, 0.5))

    plt.savefig(path + '/im' + str(i) + '.png')
