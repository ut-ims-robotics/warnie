#
# Segments the data based on the center point and the range around the center
#
def getTrajectorySegment(data, range, center_point):
    start_idx = 0
    end_idx = 0

    start_dist = center_point - range/2
    end_dist = center_point + range/2

    start_idx_found = False

    for idx, trajectory_point in enumerate(data):
        if start_idx_found != True and trajectory_point[0] >= start_dist:
            start_idx = idx
            start_idx_found = True

        if trajectory_point[0] >= end_dist:
            end_idx = idx
            break

    return data[start_idx:end_idx + 1]