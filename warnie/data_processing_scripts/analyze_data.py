import csv
import math
import numpy as np

def csvRowToNumpy(csv_row):
    pose = [float(csv_row['x']), float(csv_row['y']), float(csv_row['z'])]
    return np.array(pose)

csv_header = ["object_name", "cue_type", "closest_distance", "avg_speed"]

# Open the CSV files
initial_states_csv = open('object_initial_states.csv')
initial_states_reader = csv.DictReader(initial_states_csv)

robot_poses_csv = open('husky_warnie.csv')
robot_poses_reader = csv.DictReader(robot_poses_csv)
robot_poses = []

for robot_state in robot_poses_reader:
    robot_pose = csvRowToNumpy(robot_state)
    robot_poses.append(robot_pose)

robot_poses_np = np.array(robot_poses)

# Calculate the minimal distance from the robot
for object_state in initial_states_reader:
    min_distance = 999999999
    object_pose = csvRowToNumpy(object_state)

    # Iterate through the robot poses
    for robot_pose in robot_poses_np:
        distance = np.linalg.norm(robot_pose - object_pose)

        if distance < min_distance:
            min_distance = distance

    print (object_state['object_name'], min_distance)

initial_states_csv.close()
robot_poses_csv.close()