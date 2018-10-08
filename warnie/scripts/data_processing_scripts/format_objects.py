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
track_model = tree.getroot().find("world").find("state").findall("model")[1]

# Prepare the CSV data structures
csv_header = ["object_name", "x", "y", "z", "roll", "pitch", "yaw"]
csv_list = []

for link in track_model.findall("link"):
    name = link.get("name")
    pose = link.find("pose")
    pose_f = formatPose(pose.text)
    pose_f.insert(0, name)
    csv_list.append(pose_f)

# Write pose information to CSV file
with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(csv_header)
    writer.writerows(csv_list)

print "Finished writing initial object states to", output_file
