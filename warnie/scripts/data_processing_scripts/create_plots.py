import csv
import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from copy import copy
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
trajectory_data_dict = wtr.createTrajectoryDataDict(data_paths, in_base_path)


for trap_type, trap_tuples in trajectory_data_dict.iteritems():

    print "Working on trap '" + trap_type + "'"
    # plt.subplot(2, 1, 1)
    # plt.tight_layout()
    plt.axis([-10, 10, -3, 3])

    # plt.axis('square')
    #plt.gca().set_aspect('equal')


    wp.addTrackEdges(plt, 20, 5.45)
    wp.addBoxImages(trap_tuples[0][0], plt, images_dictionary, 0.35)

    # Plot position - Iterate through all trap data segments per current trap type
    for trap_tuple in trap_tuples:
        trap_class = trap_tuple[0]
        trajectory_segment = trap_tuple[1]

        plt.plot(trajectory_segment[:, 0] - trap_class.mean_pos_x, trajectory_segment[:, 1], "k-", alpha=0.2)

    # plt.subplot(2, 1, 2)
    # plt.axis('equal')
    # plt.axis([-10, 10, 0, 4])

    # # Plot velocity - Iterate through all trap data segments per current trap type
    # for trap_tuple in trap_tuples:
    #     trap_class = trap_tuple[0]
    #     trajectory_segment = trap_tuple[1]

    #     plt.plot(trajectory_segment[:, 0] - trap_class.mean_pos_x, trajectory_segment[:, 5], "k-", alpha=0.2)

    #Save the figure
    plt.savefig("testu.svg", format="svg", dpi=500, frameon=None)
    break
    # plt.savefig(in_base_path + "/data_visual/data_vis_vel/" + trap_type, dpi=500)

    # Clear the plot
    # plt.clf()
    # plt.show()
    # break

print "Finished. All images saved to " + in_base_path + "/data_visual/data_vis_vel/"
