import csv
import json
import sys
import math

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
# Segment the raw trajectory data into parts that relate to a positon
# of the trap
#
def segmentTrajectoryData(traps, trajectory):
    return 3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   "MAIN"
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

in_file_trajectory_file = str(sys.argv[1])
in_file_track_layout = str(sys.argv[2])
out_file_json = str(sys.argv[3])

precat_trap_data = precategorizeTrapData(in_file_track_layout)
trap_classes = rawTrapToClass(precat_trap_data)
trap_classes_json = json.dumps(trap_classes, cls=ComplexEncoder, sort_keys=True, indent=2)

print trap_classes_json

with open(out_file_json, 'w') as out_file:
    out_file.write(trap_classes_json)


