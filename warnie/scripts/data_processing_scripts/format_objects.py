import xml.etree.ElementTree as ET
import csv
import sys

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
chunk = tree.getroot().findall("chunk")[0]
chunk_world = ET.fromstring(str(chunk.text)).find("world").find("state")

# Prepare the CSV data structures
chunk_csv_header = ["object_name", "x", "y", "z", "roll", "pitch", "yaw"]
chunk_csv_list = []

for chunk_model in chunk_world.findall("model"):
    name = chunk_model.get("name")
    chunk_pose = chunk_model.find("pose")
    chunk_pose_f = formatPose(chunk_pose.text)
    chunk_pose_f.insert(0, name)
    chunk_csv_list.append(chunk_pose_f)

# Write pose information to CSV file
with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(chunk_csv_header)
    writer.writerows(chunk_csv_list)

print "Finished writing initial object states to", output_file