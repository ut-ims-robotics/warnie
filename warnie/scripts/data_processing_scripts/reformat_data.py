import csv
import sys
import os
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
trap_data_dict = {}

print "Extracting trap data and trajectory segments"
for data_path in data_paths:
    # first get the trap info
    data_full_path = in_base_path + "/" + data_path
    precat_trap_data = wt.precategorizeTrapData(data_full_path + "/track_layout.csv")
    trap_classes = wt.rawTrapToClass(precat_trap_data)

    # Get the trajectory file
    trajectory_data_np = np.genfromtxt(data_full_path + "/husky_trajectory.csv", delimiter=',', skip_header=1)

    # Organize the data into "trap_data_dict"
    for trap_class in trap_classes:

        # Prepare the trap data + trajectory tuple
        trajectory_segment = wtr.getTrajectorySegment(trajectory_data_np, 20, trap_class.mean_pos_x)
        trap_inst_tuple = (trap_class, trajectory_segment)

        # Dont append bad data
        if len(trajectory_segment) <= 0:
            continue

        # Insert the tuple into the map, but fist check if the key exists or not
        if trap_class.name in trap_data_dict:
            trap_data_dict[trap_class.name].append(trap_inst_tuple)
        else:
            trap_data_dict[trap_class.name] = []
            trap_data_dict[trap_class.name].append(trap_inst_tuple)

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
single_header = ["x", "y", "z", "yaw", "t"]
# np.set_printoptions(precision=2)

for trap_type, trap_tuples in trap_data_balanced_dict.iteritems():
    # prepare the csv header
    nr_of_subjs = len(trap_tuples)
    header = []
    csv_data_np = copy(trap_tuples[0][1])
    csv_data_np[:, 0] = csv_data_np[:, 0] - trap_tuples[0][0].mean_pos_x

    for i in range(0, nr_of_subjs):
        header += single_header

    for i in range(1, len(trap_tuples)):
        csv_data_np_add = trap_tuples[i][1]
        csv_data_np_add[:, 0] = csv_data_np_add[:, 0] - trap_tuples[i][0].mean_pos_x
        csv_data_np = np.concatenate((csv_data_np, csv_data_np_add), axis=1)

    csv_data_np = np.round(csv_data_np, decimals=3, out=None)

    output_file = in_base_path + "/data_cropped/" + trap_type + ".csv"

    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(header)
        writer.writerows(csv_data_np)

# Create trajectory images, one per each trap type
# print "Creating trajectory images"
# for trap_type, trap_tuples in trap_data_balanced_dict.iteritems():
#
#     print "Working on trap '" + trap_type + "'"
#     plt.axis('equal')
#     plt.axis([-10, 10, -3, 3])
#     wp.addTrackEdges(plt, 20, 5.45)
#     wp.addBoxImages(trap_tuples[0][0], plt, images_dictionary, 0.35)
#
#     # Iterate through all trap data segments per current trap type
#     for trap_tuple in trap_tuples:
#         trap_class = trap_tuple[0]
#         trajectory_segment = trap_tuple[1]
#
#         plt.plot(trajectory_segment[:, 0] - trap_class.mean_pos_x, trajectory_segment[:, 1], "k-", alpha=0.2)
#
#     # Save the figure
#     plt.savefig(in_base_path + "/data_visual/data_vis_trim/" + trap_type, dpi=500)
#
#     # Clear the plot
#     plt.clf()
#
# print "Finished. All images saved to " + in_base_path + "/data_visual/data_vis_trim/"