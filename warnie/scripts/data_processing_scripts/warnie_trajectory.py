import random
import numpy as np

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