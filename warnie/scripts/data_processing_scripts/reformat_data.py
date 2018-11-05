import csv
import json
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

#
# Class for maintaining visual cue box data
#
class VisualCueBox:
    def __init__(self, cue_type, cue_functionality, x, y, z):
        self.cue_type = cue_type
        self.cue_functionality = cue_functionality
        self.x = x
        self.y = y
        self.z = z

    def toStr(self):
        return (self.cue_type + " "
                + self.cue_functionality + " "
                + str(self.x) + " "
                + str(self.y) + " "
                + str(self.z))

    def reprJSON(self):
        return self.__dict__

#
# Class for maintaining trap data
#
class Trap:
    def __init__(self, name, trap_type):
        self.name = name
        self.trap_type = trap_type
        self.visual_cue_boxes = []
        self.mean_pos_x = 0.0
        self.trajectory_data_path = "/todo/"

    def addVisualCueBox(self, visual_cue_box):
        self.visual_cue_boxes.append(visual_cue_box)

    def calculateMeanPos(self):
        mean_pos_x = 0.0

        for box in self.visual_cue_boxes:
            mean_pos_x += box.x

        mean_pos_x /= len(self.visual_cue_boxes)
        self.mean_pos_x = mean_pos_x
        return mean_pos_x

    def reprJSON(self):
        return self.__dict__

    def toStr(self):
        trap_str = "trap_name: " + self.name + \
                   "\ntrap_type: " + self.trap_type + \
                   "\ntrap_mean_pos_x: " + str(self.mean_pos_x) + \
                   "\ncue_boxes: \n"

        for box in self.visual_cue_boxes:
            trap_str += "    " + box.toStr() + '\n'

        return trap_str

#
# JSON encoder
#
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

#
# Return trap category
#
def getTrapType(trap_name):
    if "b" in trap_name:
        return "biased"
    elif "c" in trap_name:
        return "continuous"
    elif "d" in trap_name:
        return "discrete"

#
# Return box category
#
def getBoxType(box_name):
    box_name_last = box_name.split("::")[-1]

    if "attract" in box_name_last:
        return "pull"
    elif "repel" in box_name_last:
        return "push"
    elif "normal" in box_name_last:
        return "neutral"
    elif "wall_l" in box_name_last:
        return "wall_left"
    elif "wall_r" in box_name_last:
        return "wall_right"
    else:
        return "undefined"

#
# Convert raw trap data to Trap class
#
def rawTrapToClass(raw_trap_data):
    trap_classes = []

    for trap_name, trap_boxes in raw_trap_data.iteritems():
        trap = Trap(trap_name, getTrapType(trap_name))

        for box_raw in trap_boxes:
            box_type = getBoxType(box_raw['object_name'])
            box_functionality = box_raw['object_name'].split("::")[-2]
            box_x = float(box_raw['x'])
            box_y = float(box_raw['y'])
            box_z = float(box_raw['z'])

            box_processed = VisualCueBox(box_type, box_functionality, box_x, box_y, box_z)
            trap.addVisualCueBox(box_processed)

        trap.calculateMeanPos()
        trap_classes.append(trap)

    return trap_classes

#
# Precategorize the raw trap layout data
#
def precategorizeTrapData(track_layout_file):
    precat_trap_data = {}

    # Open the CSV files
    track_layout_csv = open(track_layout_file)
    track_layout_reader = csv.DictReader(track_layout_csv)

    for idx, track_element in enumerate(track_layout_reader):
        full_name = track_element['object_name']
        trap_name = full_name.split('::')[1]

        if ("trap" in trap_name) or ("vis_cue" in trap_name):
            if trap_name in precat_trap_data:
                precat_trap_data[trap_name].append(track_element)
            else:
                precat_trap_data[trap_name] = []
                precat_trap_data[trap_name].append(track_element)

    return precat_trap_data

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

#
# Creates a dictionary of the box images
#
def createImagesDictionary(base_path):
    images_dict = {}

    images_dict['neutral'] = plt.imread(base_path + "neutral_box.png", format="png")
    images_dict['pull'] = plt.imread(base_path + "pull_box.png", format="png")
    images_dict['push'] = plt.imread(base_path + "push_box.png", format="png")

    return images_dict

#
# Adds box images to the plot
#
def addBoxImages(trap_data, plot, images_dict, box_size):
    for box in trap_data.visual_cue_boxes:
        if "wall" not in box.cue_type:
            box_x = box.x - trap_data.mean_pos_x
            box_y = box.y
            extent_x_min = box_x - box_size
            extent_x_max = box_x + box_size
            extent_y_min = box_y - box_size
            extent_y_max = box_y + box_size

            plot.imshow(images_dict[box.cue_type], extent=[extent_x_min, extent_x_max, extent_y_min, extent_y_max])

#
# Adds track edges to the plot
#
def addTrackEdges(plot, distance, width):
    left = [[-distance/2, distance/2], [width/2, width/2]]
    right = [[-distance/2, distance/2], [-width/2, -width/2]]

    plot.plot(left[0], left[1], "b-")
    plot.plot(right[0], right[1], "b-")

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



'''
fig, plot = plt.subplots()
plt.axis('equal')
plt.axis([-10, 10, -3, 3])

images_dictionary = createImagesDictionary("../images/")

test_trap = trap_classes[5]
trajectory_data_np = np.genfromtxt(in_file_trajectory_file, delimiter=',', skip_header=1)
trajectory_segment = getTrajectorySegment(trajectory_data_np, 20, test_trap.mean_pos_x)

plot.plot(trajectory_segment[:, 0] - test_trap.mean_pos_x, trajectory_segment[:, 1], "k-", alpha=0.2)
addTrackEdges(plot, 20, 5.45)

addBoxImages(test_trap, plot, images_dictionary, 0.35)

plt.show()
#plt.savefig("test.png", dpi=500)
'''


# Get the data directories
in_base_path = str(sys.argv[1])
data_paths_raw = os.listdir(in_base_path)
data_paths = []

# Prepare the plotting things
# fig, plot = plt.subplots()
plt.axis('equal')
plt.axis([-10, 10, -3, 3])
images_dictionary = createImagesDictionary(in_base_path + "/images/")

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
    precat_trap_data = precategorizeTrapData(data_full_path + "/track_layout.csv")
    trap_classes = rawTrapToClass(precat_trap_data)

    # Get the trajectory file
    trajectory_data_np = np.genfromtxt(data_full_path + "/husky_trajectory.csv", delimiter=',', skip_header=1)

    # Organize the data into "trap_data_dict"
    for trap_class in trap_classes:

        # Prepare the trap data + trajectory tuple
        trajectory_segment = getTrajectorySegment(trajectory_data_np, 20, trap_class.mean_pos_x)
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
    addTrackEdges(plt, 20, 5.45)
    addBoxImages(trap_tuples[0][0], plt, images_dictionary, 0.35)

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