from matplotlib import pyplot as plt
import numpy as np
import csv, math

def get_angles_and_skin(name):
    skin_data = []
    time = []
    pos_data = []
    # coords = ['x','y','z','rx','ry','rz']

    with open('Generic_ur5_controller/data/' + name + '.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        n = 0
        for row in csvreader:
            # print(row)
            if n > 1:
                skin_data.append(row[14:30])
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

    skins = []
    index_nums = [0,7,8,9]
    for i in range(len(new_skin_data)):
        if i in index_nums:
            skins.append(new_skin_data[i])

    L = 0.16
    ys = new_pos_data[1]
    start_y = ys[0]
    ang = [math.asin((y-start_y)/L)*180/math.pi for y in ys]

    return time, ang, np.transpose(skins)

name = 'cantilever1/Tue-Jan-25-15.27.19-2022_data'
# trim_start = 100
# trim_stop = -100
t, angles, skin = get_angles_and_skin(name)
start_trim = 100
end_trim = 4342
t = t[108:4342]
angles = angles[108:4342]
skin = skin[108:4342,:]
# skin = [:][108:4342]

plt.figure()
plt.plot(t,angles)
plt.xlabel("Time (s)")
plt.ylabel("Angles (°)")

plt.figure()
plt.plot(t,skin)
plt.xlabel("Time (s)")
plt.ylabel("Raw sensor data")

plt.figure()
index_nums = [0,7,8,9]
skin = np.transpose(skin)
for i in range(len(skin)):
    plt.scatter(angles, skin[i], s=3, label=index_nums[i])
plt.xlabel("Angle of chopstick (°)")
plt.ylabel("Raw sensor data (label is sensor number)")
plt.legend()

plt.show()

