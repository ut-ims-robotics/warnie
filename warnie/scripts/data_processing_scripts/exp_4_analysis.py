# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Usage:
#       1) Populate the "trap_names.txt" file with traps you want to analyze
#       2) Run the script from commandline:
#             python2.7 continuous_data.py <path/to/data_folders> <path/to/trap_name_file>/trap_names.txt
#          Example:
#             python2.7 /home/scripts/continuous_data.py /home/data /home/data/trap_names.txt
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
import sys
import numpy as np

# ------------------------------------  Start of function definitions  ------------------------------------

#
# Function for extracting the trap names from a trap_list.txt file
#
def getTrapList(trap_list_path):
    trap_names = []
    with open(trap_list_path, "r") as f:
        trap_names = f.read().splitlines()
    return trap_names

#
# Returns the index of the datapoint where the subject crosses the trap
#
def getCrossingIndex(trajectory_data):
    crossing_idx = 0

    for idx, trajectory_point in enumerate(trajectory_data):
        if trajectory_point >= 0:
            crossing_idx = idx - 1
            break

    return crossing_idx

#
# Reformats the data
# 
def reformatOutput(interception_data):
    data_dict = dict()

    for i_d in interception_data:
        if i_d[1] in data_dict:
            data_dict[i_d[1]].append(i_d[0])
        else:
            data_dict[i_d[1]] = []
            data_dict[i_d[1]].append(i_d[0])

    return data_dict

# ------------------------------------  End of function definitions  ------------------------------------

# Get the path that was specified from the command line
in_data_base_path = str(sys.argv[1])
trap_list_path = str(sys.argv[2])

# Get the names of the traps on which the data analysis will be performed
trap_names = getTrapList(trap_list_path)

# Create a datastructure for stroring Y intersection data
i_d_dict = {}

# Extract the data per each trap
for trap_name in trap_names:

    # Get the trajectory file
    traj_file_path = in_data_base_path + "/" + trap_name + "/" + trap_name + ".csv"
    trajectory_data_np = np.genfromtxt(traj_file_path, delimiter=',', skip_header=1)

    cols_per_subj = 6 # The data has 6xn columns where n is the number of subjects
    nr_of_cols = trajectory_data_np.shape[1] # Get the number of columns
    nr_of_subjs = nr_of_cols/cols_per_subj     # Get the number of subjects

    i_d_dict[trap_name] = [0, 0, 0, 0.0, 0.0]

    # Extract the Y coordinate of the crossing point
    for subj_idx in range(0, nr_of_subjs):
        x_cols = trajectory_data_np[:, subj_idx * cols_per_subj]
        y_cols = trajectory_data_np[:, subj_idx * cols_per_subj + 1]

        crossing_idx = getCrossingIndex(x_cols)
        # print "crossing_idx = ", crossing_idx

        x1 = x_cols[crossing_idx]
        y1 = y_cols[crossing_idx]
        x2 = x_cols[crossing_idx + 1]
        y2 = y_cols[crossing_idx + 1]

        y_intercept = y2 - (y2-y1)/(x2-x1)*x2
        y_intercept = round(y_intercept, 4)

        if y_intercept > 0:
            i_d_dict[trap_name][0] += 1
        else:
            i_d_dict[trap_name][1] += 1

    i_d_dict[trap_name][2] = i_d_dict[trap_name][0] + i_d_dict[trap_name][1]
    i_d_dict[trap_name][3] = i_d_dict[trap_name][0] / float(i_d_dict[trap_name][2])
    i_d_dict[trap_name][4] = i_d_dict[trap_name][1] / float(i_d_dict[trap_name][2])

# Print the data out
for name, d in i_d_dict.iteritems():
    print name, d[0], d[1], d[2], d[3], d[4]

# Convert to dictionary format
#data_dict = reformatOutput(interception_data)

#for key, value in data_dict.iteritems():
#    print key

#    print len(value)

#    print "--------"

#output_file_csv = in_data_base_path + "/continuous_5block_1.csv"
#with open(output_file_csv, 'wb') as f:  # Just use 'w' mode in 3.x
#    w = csv.writer(f, delimiter = "\t")
#    w.writerow(data_dict.keys())
#    w.writerows(zip(*[data_dict[key] for key in data_dict.keys()]))

#
# UNCOMMENT THE FOLLOWING CODE IF YOU WANT TO STORE THE DATA
#

# Save the data to a CSV file
# output_file_csv = in_data_base_path + "/continuous_5block.csv"
# with open(output_file_csv, 'w') as csvfile:
#    writer = csv.writer(csvfile, delimiter=",")
#    writer.writerows(interception_data)




