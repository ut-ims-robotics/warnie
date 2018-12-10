import random
import numpy as np
import warnie_trap as wt

#
# Segments the data based on the center point and the range around the center
#
def getTrajectorySegment(trajectory_data, range, center_point):
    start_idx = 0
    end_idx = 0

    start_dist = center_point - range/2
    end_dist = center_point + range/2

    start_idx_found = False

    for idx, trajectory_point in enumerate(trajectory_data):
        if start_idx_found != True and trajectory_point[0] >= start_dist:
            start_idx = idx
            start_idx_found = True

        if trajectory_point[0] >= end_dist:
            end_idx = idx
            break

    return trajectory_data[start_idx:end_idx + 1]

#
# Finds the index of the element, which has its "x" closest to given value
#
def findXElementIndex(trajectory_data, x_val):
    min_diff_idx = 0
    min_x_val_diff = 9999999

    for idx, trajectory_point in enumerate(trajectory_data):
        x_val_diff = abs(trajectory_point - x_val)

        if x_val_diff < min_x_val_diff:
            min_diff_idx = idx
            min_x_val_diff = x_val_diff

    return min_diff_idx

#
# Finds the min nr of datapoints from given value
#
def findMinDataPoints(trajectory_data, x_val):
    idx = findXElementIndex(trajectory_data, x_val)
    nr_of_elems_left = idx
    nr_of_elems_right = len(trajectory_data) - nr_of_elems_left - 1

    # minim = min(nr_of_elems_left, nr_of_elems_right)
    # print "right: ", nr_of_elems_right, ", left: ", nr_of_elems_left, ", min: ", minim, ", total: ", len(trajectory_data)
    return min(nr_of_elems_left, nr_of_elems_right)

#
# Removes the given amount of points in the data
#
def removeDatapoints(trajectory_data, nr_of_points):
    idxs = random.sample(range(len(trajectory_data)), nr_of_points)
    new_array = np.delete(trajectory_data, idxs, axis=0)
    # print "removed", len(trajectory_data) - len(new_array), "datapoints"
    #return np.delete(trajectory_data, idxs)
    return new_array

#
# Balances the amount of datapoints to given amount around given index
#
def balanceData(trajectory_data, center_idx, balance_count):
    data_left = trajectory_data[0: center_idx]
    data_right = trajectory_data[center_idx + 1:]
    data_center = trajectory_data[center_idx]

    # print "left: ", len(data_left), ", right: ", len(data_right), ", total: ", len(trajectory_data), ", center: ", data_center[0], " at_idx: ", center_idx

    balance_diff_left = len(data_left) - balance_count
    balance_diff_right = len(data_right) - balance_count

    # print "diff_left: ", balance_diff_left, ", diff_right: ", balance_diff_right

    if balance_diff_left > 0:
        data_left = removeDatapoints(data_left, balance_diff_left)

    if balance_diff_right > 0:
        data_right = removeDatapoints(data_right, balance_diff_right)

    balanced_array = np.concatenate((data_left, [data_center]), axis=0)
    balanced_array = np.concatenate((balanced_array, data_right), axis=0)
    return balanced_array

#
# Calculate velocity
#
def addVelocityToTrajectoryData(trajectory_data, upper_limit):
    separation = 10

    velocity_data = []
    for i in range(0, separation):
        velocity_data.append([0])

    for idx in range(separation, len(trajectory_data)):
        dx = trajectory_data[idx][0] - trajectory_data[idx-separation][0]
        dt = trajectory_data[idx][4] - trajectory_data[idx-separation][4]
        v = 0

        if dt > 0:
            v = dx/dt

        velocity_data.append([v])

    neo_data = np.concatenate((trajectory_data, velocity_data), axis=1)

    # throw out the outliers
    remove_idxs = []
    for idx in range(0, len(neo_data)):
        if neo_data[idx][5] > upper_limit:
            remove_idxs.append(idx)

    final_data = np.delete(neo_data, remove_idxs, axis=0)

    return final_data
#
# Format trap data as a dictionary
# Get the data and put it into a dictionary where the key is the name of the trap
# and the value is a list of tuples, where a tuple contains trap info and a trajectory segment
#
def createTrajectoryDataDict(data_paths, base_path):
    trap_data_dict = {}
    print "Extracting trap data and trajectory segments"
    for data_path in data_paths:
        # first get the trap info
        data_full_path = base_path + "/" + data_path
        precat_trap_data = wt.precategorizeTrapData(data_full_path + "/track_layout.csv")
        trap_classes = wt.rawTrapToClass(precat_trap_data)

        # Get the trajectory file
        trajectory_data_np = np.genfromtxt(data_full_path + "/husky_trajectory.csv", delimiter=',', skip_header=1)
        trajectory_data_np = addVelocityToTrajectoryData(trajectory_data_np, 2.5)

        # Organize the data into "trap_data_dict"
        for trap_class in trap_classes:

            # Prepare the trap data + trajectory tuple
            trajectory_segment = getTrajectorySegment(trajectory_data_np, 20, trap_class.mean_pos_x)
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

    return trap_data_dict
