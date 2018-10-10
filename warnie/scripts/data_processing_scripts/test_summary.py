import csv
import sys
import math
from numpy import genfromtxt

in_trajectory_file = str(sys.argv[1])
out_summary_file = str(sys.argv[2])

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

