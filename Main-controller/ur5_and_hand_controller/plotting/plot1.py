from matplotlib import pyplot as plt
import numpy as np
import csv

from numpy.core.fromnumeric import mean

def normalise(dat):
    ref = np.mean(dat[:20])
    for i in range(len(dat)):
        dat[i] -= ref
    return dat

# name = 'data/archive/_Thu-Nov-11-11.05.00-2021_0_data'
# name = 'data/archive/_Thu-Nov-11-11.12.59-2021_0_data'

# name = 'data/archive/_Thu-Nov-11-11.42.47-2021_0_data'
# name = 'data/archive/_Thu-Nov-11-11.45.16-2021_0_data'

# name = 'data/archive/Mon-Nov-15-14.35.15-2021_0_data'
# name = 'data/archive/Mon-Nov-15-15.24.07-2021_0_data'
# name = 'data/archive/Mon-Nov-15-15.25.52-2021_0_data'

name = 'data/archive/test7/Thu-Nov-18-11.23.18-2021_0_data'




def plot_data(name):
    skin_data = []
    time = []
    sensors = [2,3,8,9,14,15]
    with open('Generic_ur5_controller/' + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            if n > 0:
                l = []
                # skin_data.append(row[-16:])
                for s in sensors:
                    l.append(row[-16+s])
                print(l)
                if is_valid(l, len(sensors)):
                    skin_data.append(l)
                    time.append(row[1])
            else:
                n+=1

    print(skin_data)

    time = list(map(float, time))

    new_skin_data = []
    for s in skin_data:
        new_skin_data.append(list(map(float, s)))
        

    new_skin_data = np.transpose(new_skin_data)


    for data in new_skin_data:
        plt.plot(time, normalise(data))
        plt.xlabel("Time (s)")
        plt.ylabel("Raw")

    plt.show()
    # plt.savefig('Generic_ur5_controller/' + name + '.png')

def is_valid(data, length):
    if len(data) == length:
        for value in data:
            if float(value) <= 11500 or float(value) >= 25000:
                return False
    else:
        return False
    return True


plot_data(name)