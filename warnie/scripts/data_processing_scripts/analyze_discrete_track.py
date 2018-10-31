import csv
import yaml
import sys
import math
import numpy as np

#
# Class for maintaining visual cue box data
#
class VisualCueBox:
    def __init__(self, cue_type, x, y)
        self.cue_type = cue_type
        self.x = x
        self.y = y

#
# Class for maintaining trap data
#
class Trap:
    def __init__(self, name)
        self.name = name
  
    def addVisualCueBox(self, visual_cue_box)
        self.visual_cue_boxes.append(visual_cue_box)

#
# Function that evaluates which opening was passed
#
def evaluateOpeningBinary():
    #stuff

#
# Function that BLA
#
def extractTraps(trap_data):
    #stuff


in_file_trajectory_file = str(sys.argv[1])
in_file_track_layout = str(sys.argv[2])
out_file_results = str(sys.argv[3])

# Open the CSV files
#trajectory_data_csv = open(in_trajectory_file)
#trajectory_data_reader = csv.DictReader(trajectory_data_csv)

##for trajectory_point in trajectory_data_reader:
#   
#first_point = trajectory_data_reader[1]

#print first_point

trajectory_data = genfromtxt(in_trajectory_file, delimiter=',')

# Calculate duration
test_duration_sec = trajectory_data[-1][4] - trajectory_data[1][4]
test_duration_m = int(math.floor(test_duration_sec/60))
test_duration_s = test_duration_sec % 60

# Write the data to the summary file
summary = open(out_summary_file, "w")
summary.write("Duration: " + str(test_duration_m) + " min " + str(test_duration_s) + " s")
summary.close()

