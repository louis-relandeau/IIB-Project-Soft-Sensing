import os
import glob
import pandas as pd
import copy
import csv
import numpy as np

def combine(path, name):
    # os.chdir("Generic_ur5_controller/data/test4-chopstick-angle-change-c4/untrimmed/")
    os.chdir(path)

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # print(all_filenames)
    # print(all_filenames[2:]) # to skip first two

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f, sep=' ') for f in all_filenames[2:] ])
    combined_csv_list = combined_csv.values.tolist()
    combined_csv_list = [c[0].split(',') for c in combined_csv_list]
    # print(combined_csv_list)

    #need to change index and timestamp for continuous sequence
    fake_time = 0.
    previous_time = 0.
    fake_index = 0
    continuous_file = []
    # with open(name, 'w') as f:
    #     write = csv.writer(f)
    for s in combined_csv_list:
        new_s = copy.copy(s)
        fake_index += 1
        sample_time = float(s[1])
        diff = sample_time-previous_time
        if diff > 0:
            fake_time += diff
        previous_time = sample_time

        # print(s[0], fake_index, sample_time, fake_time)
        new_s[0] = fake_index
        new_s[1] = fake_time
        # print(new_s)
        # write.writerow(new_s)
        if float(new_s[3]) <= -0.067:
            continuous_file.append(new_s)

    # print(continuous_file)
    # #export to csv
    # with open(name, 'w') as f:
    #     write = csv.writer(f)
    #     write.writerows(continuous_file)
    np.savetxt(name, 
        continuous_file,
        delimiter =",", 
        fmt ='% s')


if __name__ == '__main__':
    path = "Generic_ur5_controller/data/rerun_chop4"
    name = "combined.csv"
    combine(path, name)