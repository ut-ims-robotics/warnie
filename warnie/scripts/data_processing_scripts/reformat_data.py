import csv
import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from copy import copy
import warnie_trap as wt
import warnie_plot as wp
import warnie_trajectory as wtr

# Get the data directories
in_base_path = str(sys.argv[1])
data_paths_raw = os.listdir(in_base_path)
data_paths = []

# Prepare the plotting things
plt.axis('equal')
plt.axis([-10, 10, -3, 3])
images_dictionary = wp.createImagesDictionary(in_base_path + "/images/")

# Clear out any other irrelevant directories
for path in data_paths_raw:
    if "subject" in path:
        data_paths.append(path)

# Get the data and put it into a dictionary where the key is the name of the trap
# and the value is a list of tuples, where a tuple contains trap info and a trajectory segment
trap_data_dict = wtr.createTrajectoryDataDict(data_paths, in_base_path)

# Balance the trajectory data
trap_data_balanced_dict = {}
min_elements_global = 9999999

for trap_type, trap_tuples in trap_data_dict.iteritems():
    for trap_tuple in trap_tuples:
        trap_class = trap_tuple[0]
        trajectory_segment = trap_tuple[1]
        min_elements = wtr.findMinDataPoints(trajectory_segment[:, 0], trap_class.mean_pos_x)

        if (min_elements < min_elements_global) and (min_elements > 0):
            min_elements_global = min_elements

print "global min elements: ", min_elements_global
losses = []

for trap_type, trap_tuples in trap_data_dict.iteritems():
    for trap_tuple in trap_tuples:
        trap_class = trap_tuple[0]
        trajectory_segment = trap_tuple[1]
        idx = wtr.findXElementIndex(trajectory_segment[:, 0], trap_class.mean_pos_x)

        balanced_trajectory_segment = wtr.balanceData(trajectory_segment, idx, min_elements_global)
        loss = 100*(len(trajectory_segment) - len(balanced_trajectory_segment)) / len(trajectory_segment)
        losses.append(loss)

        # print ("before: ", len(trajectory_segment), ", after:  ", len(balanced_trajectory_segment), ", loss: ", loss)

        trap_inst_tuple = (trap_class, balanced_trajectory_segment)

        # Insert the tuple into the map, but fist check if the key exists or not
        if trap_class.name in trap_data_balanced_dict:
            trap_data_balanced_dict[trap_class.name].append(trap_inst_tuple)
        else:
            trap_data_balanced_dict[trap_class.name] = []
            trap_data_balanced_dict[trap_class.name].append(trap_inst_tuple)

print "Mean loss is:", np.mean(losses), ", with std_dev:", np.std(losses)

# Save the data
single_header = ["x", "y", "z", "yaw", "t", "v"]
# np.set_printoptions(precision=2)

for trap_type, trap_tuples in trap_data_balanced_dict.iteritems():
    # prepare the csv header
    nr_of_subjs = len(trap_tuples)
    header = []
    csv_data_np = copy(trap_tuples[0][1])
    csv_data_np[:, 0] = csv_data_np[:, 0] - trap_tuples[0][0].mean_pos_x

    # Create the header
    for i in range(0, nr_of_subjs):
        header += single_header

    # Assemble the data
    for i in range(1, len(trap_tuples)):
        csv_data_np_add = trap_tuples[i][1]
        csv_data_np_add[:, 0] = csv_data_np_add[:, 0] - trap_tuples[i][0].mean_pos_x
        csv_data_np = np.concatenate((csv_data_np, csv_data_np_add), axis=1)

    output_path = in_base_path + "/data_cropped/" + trap_type + "/"
    os.mkdir(output_path)

    # Write the data to csv file
    csv_data_np = np.round(csv_data_np, decimals=3, out=None)
    output_file_csv = output_path + trap_type + ".csv"
    with open(output_file_csv, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(header)
        writer.writerows(csv_data_np)

    # Write the trap info to json file
    trap_class_json = json.dumps(trap_tuples[0][0], cls=wt.ComplexEncoder, sort_keys=True, indent=2)
    output_file_json = output_path + trap_type + ".json"
    with open(output_file_json, 'w') as jsonfile:
        jsonfile.write(trap_class_json)
