import csv
import sys
import math
import numpy as np

def csvRowToNumpy(csv_row):
    pose = [float(csv_row['x']), float(csv_row['y']), float(csv_row['z'])]
    return np.array(pose)

# Get the input file path and output file path
input_file_1 = str(sys.argv[1])
input_file_2 = str(sys.argv[2])
output_file = str(sys.argv[3])

# Header for the output CSV file
output_data_header = ["object_name", "cue_type", "closest_distance", "avg_speed"]

proximity_radius = 5

# Open the CSV files
initial_states_csv = open(input_file_1)
initial_states_reader = csv.DictReader(initial_states_csv)
robot_poses_csv = open(input_file_2)
robot_poses_reader = csv.DictReader(robot_poses_csv)

# Convert the robot poses into numpy array
robot_poses = []
robot_pose_timestamps = []
for robot_state in robot_poses_reader:
    robot_pose = csvRowToNumpy(robot_state)
    robot_poses.append(robot_pose)
    robot_pose_timestamps.append(float(robot_state['time(s)']))

robot_poses_np = np.array(robot_poses)
output_data = []
print output_data_header

# Calculate the minimal distance from the robot
for object_state in initial_states_reader:
    min_distance = 999999999
    avg_speed = 0
    proximity_count = 0
    object_pose = csvRowToNumpy(object_state)

    # Iterate through the robot poses
    for index, robot_pose in enumerate(robot_poses_np):
        distance = np.linalg.norm(robot_pose - object_pose)

        # Calculate the velocity in objects proximity
        if distance < proximity_radius:
            distance_prev = np.linalg.norm(robot_poses_np[index-1] - object_pose)
            speed = (distance - distance_prev)/(robot_pose_timestamps[index] - robot_pose_timestamps[index-1])
            avg_speed += speed
            proximity_count += 1

        # Check how close the robot got to the object
        if distance < min_distance:
            min_distance = distance

    # Calculate the average velocity in the objects proximity
    # NOTE: the speed may be negative, hence this value kind of estimates
    # what was the speed given that the robot drove smoothly across the proximity radius
    if proximity_count > 0:
        avg_speed /= proximity_count

    output_data_inst = [object_state['object_name'], 'ToDo', min_distance, avg_speed]
    output_data.append(output_data_inst)
    print (output_data_inst)

# Write the data to CSV file
with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(output_data_header)
    writer.writerows(output_data)

print "Finished writing analysis output to", output_file

# Close the CSV files
initial_states_csv.close()
robot_poses_csv.close()