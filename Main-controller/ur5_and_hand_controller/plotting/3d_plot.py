import matplotlib.pyplot as plt
import numpy as np
import csv
import random


name = 'index_fingertip_table/100moves'

def plot_data(name):
    rot_data = []

    with open('Generic_ur5_controller/csv_files/' + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            if n > 0:
                rot_data.append(row[5:8])
            else:
                n+=1

    
    float_rot_data = []
    for i in range(len(rot_data)):
        float_rot_data.append(list(map(float, rot_data[i])))

    new_rot_data = random.sample(float_rot_data,50)   
    
    print(len(new_rot_data)) 



    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for r in new_rot_data:
        xs = r[0]
        ys = r[1]
        zs = r[2]
        ax.scatter(xs, ys, zs)

    ax.set_xlabel('RX')
    ax.set_ylabel('RY')
    ax.set_zlabel('RZ')

    plt.show()

plot_data(name)

