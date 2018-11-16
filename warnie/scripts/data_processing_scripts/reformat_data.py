import csv
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import warnie_trap as wt
import warnie_plot as wp
import warnie_trajectory as wtr

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   "MAIN"
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Get the paths to trajectory data, track layout data and JSON output data
'''
in_file_trajectory_file = str(sys.argv[1])
in_file_track_layout = str(sys.argv[2])
out_file_json = str(sys.argv[3])
'''

'''
# Extract the trap classes
precat_trap_data = precategorizeTrapData(in_file_track_layout)
trap_classes = rawTrapToClass(precat_trap_data)
'''

# Write the trap data to a JSON file
# trap_classes_json = json.dumps(trap_classes, cls=ComplexEncoder, sort_keys=True, indent=2)
# with open(out_file_json, 'w') as out_file:
#     out_file.write(trap_classes_json)

# Open the trajectory file and convert it into numpy array


# Get the data directories
in_base_path = str(sys.argv[1])
data_paths_raw = os.listdir(in_base_path)
data_paths = []

# Prepare the plotting things
# fig, plot = plt.subplots()
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

        # Insert the tuple into the map, but fist check if the key exists or not
        if trap_class.name in trap_data_dict:
            trap_data_dict[trap_class.name].append(trap_inst_tuple)
        else:
            trap_data_dict[trap_class.name] = []
            trap_data_dict[trap_class.name].append(trap_inst_tuple)

# Create trajectory images, one per each trap type
print "Creating trajectory images"
for trap_type, trap_tuples in trap_data_dict.iteritems():

    print "Working on trap '" + trap_type + "'"
    plt.axis('equal')
    plt.axis([-10, 10, -3, 3])
    wp.addTrackEdges(plt, 20, 5.45)
    wp.addBoxImages(trap_tuples[0][0], plt, images_dictionary, 0.35)

    # Iterate through all trap data segments per current trap type
    for trap_tuple in trap_tuples:
        trap_class = trap_tuple[0]
        trajectory_segment = trap_tuple[1]

        plt.plot(trajectory_segment[:, 0] - trap_class.mean_pos_x, trajectory_segment[:, 1], "k-", alpha=0.2)

    # Save the figure
    plt.savefig(in_base_path + "/data_visual/" + trap_type, dpi=500)

    # Clear the plot
    plt.clf()

print "Finished. All images saved to " + in_base_path + "/data_visual/"