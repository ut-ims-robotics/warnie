import xml.etree.ElementTree as ET
import csv
import sys

def formatTime(time_unform):
    time_components = time_unform.split(" ")
    return float(time_components[0]) + float(time_components[1])/1000000000

def formatPose(pose_unform):
    pose_f = []
    for pose_uf in pose_unform.split(" "):
        pose_f.append(float(pose_uf))
    return pose_f

# Get the input file path and output file path
input_file = str(sys.argv[1])
output_file = str(sys.argv[2])

# Open the xml file
print "Opening", input_file
tree = ET.parse(input_file)
root = tree.getroot()
print "Amount of chunks in this file is", len(root.findall("chunk"))

# Prepare the CSV data structures
chunk_csv_header = ["x", "y", "z", "roll", "pitch", "yaw", "time(s)"]
chunk_csv_list = []

# Extract pose related information
for chunk_idx, chunk_elem in enumerate(root.findall("chunk")[2:]):

    chunk_root = ET.fromstring(str(chunk_elem.text)).find("state")
    chunk_model = chunk_root.find("model")
    chunk_time = chunk_root.find("real_time")
    chunk_pose = chunk_model.find("pose")

    chunk_time_f = formatTime(chunk_time.text)
    chunk_pose_f = formatPose(chunk_pose.text)

    chunk_pose_f.append(chunk_time_f)
    chunk_csv_list.append(chunk_pose_f)

# Write pose information to CSV file
with open(output_file, 'w') as csvfile:

    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(chunk_csv_header)
    writer.writerows(chunk_csv_list)

print "Finished writing pose information to", output_file
