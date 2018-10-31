import csv
import json
import sys
import math

#
# Class for maintaining visual cue box data
#
class VisualCueBox:
    def __init__(self, cue_type, x, y, z):
        self.cue_type = cue_type
        self.x = x
        self.y = y
        self.z = z

    def toJsonStr(self):
        # Return Json string
        return "1"


#
# Class for maintaining trap data
#
class Trap:
    def __init__(self, name):
        self.name = name

    def addVisualCueBox(self, visual_cue_box):
        self.visual_cue_boxes.append(visual_cue_box)

    def toJsonStr(self):
        # Return JSON string
        return "2"

#
# Convert raw trap data to Trap class
#
def rawTrapToClass(raw_trap_data):
    return raw_trap_data

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
                precat_trap_data[trap_name].append(full_name)
            else:
                precat_trap_data[trap_name] = []
                precat_trap_data[trap_name].append(full_name)

    return precat_trap_data

in_file_trajectory_file = str(sys.argv[1])
in_file_track_layout = str(sys.argv[2])
# out_file_yaml = str(sys.argv[3])

precat_trap_data = precategorizeTrapData(in_file_track_layout)

for key, value in precat_trap_data.iteritems():
    print key

    for val in value:
        print "   " + val

# with open('data.json', 'w') as outfile:
#     json.dump(data, outfile)

# data_dictionary = {}
# data_json = json.dumps(data_dictionary)
# print data_json

