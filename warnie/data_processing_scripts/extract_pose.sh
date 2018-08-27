#!/bin/bash

#
# Usage: 
#   bash extract_pose.sh <log_file_path>(required) <name_of_the_object>(opitional)
#

RED="\e[31m"
YELLOW="\e[33m"
GREEN="\e[32m"
BOLD="\e[1m"
NL="\n"
RESET="\e[39m\e[0m"

LOG_FILE_PATH=$1
GAZEBO_OBJECT="husky_warnie"

# Check if the input path was given or not
if [[ $LOG_FILE_PATH == "" ]]; then
  echo -e $RED$BOLD"Gazebo logfile path not specified. Exiting"$RESET
  exit
fi

# Check if the object was specified or not
if [[ $2 != "" ]]; then
  GAZEBO_OBJECT=$2
fi

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Extract only pose related information from the log file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

echo -e $RESET $GREEN $NL"Extracting pose information of" $BOLD$GAZEBO_OBJECT $RESET$GREEN"..."$RESET
gz log -e -f $LOG_FILE_PATH --filter $GAZEBO_OBJECT.pose >> log_pose_tmp.xml

# Check if the process was successful or not
if [[ $? != 0 ]]; then
  echo -e $RED $BOLD"Failed to extract pose information from" $LOG_FILE_PATH". Exiting"$RESET
  exit
fi

# # # # # # # # #
# Format to CSV
# # # # # # # # #

echo -e $RESET $GREEN $NL"Formating pose information to CSV format ..."$RESET
python2.7 format_pose.py log_pose_tmp.xml $GAZEBO_OBJECT.csv

# Check if the process was successful or not
if [[ $? != 0 ]]; then
  echo -e $RED $BOLD"Failed to extract pose information from" $LOG_FILE_PATH". Exiting"$RESET
  exit
fi

# # # # # # # # # # # # # # # # # # # # #
# Extract initial states of the objects
# # # # # # # # # # # # # # # # # # # # #

echo -e $RESET $GREEN $NL"Extracting initial states of the world objects ..."$RESET
python2.7 format_objects.py log_pose_tmp.xml object_initial_states.csv

# Check if the process was successful or not
if [[ $? != 0 ]]; then
  echo -e $RED $BOLD"Failed to extract initial state information from" $LOG_FILE_PATH". Exiting"$RESET
  exit
fi

# # # # # # # # # # # # # # # # # # # # #
# Run the data analysis
# # # # # # # # # # # # # # # # # # # # #

echo -e $RESET $GREEN $NL"Analyzing the data ..."$RESET
python2.7 analyze_data.py object_initial_states.csv $GAZEBO_OBJECT.csv analyzed_data.csv

# Check if the process was successful or not
if [[ $? != 0 ]]; then
  echo -e $RED $BOLD"Failed to analyze the data" $LOG_FILE_PATH". Exiting"$RESET
  exit
fi

# Remove the temporary file
rm log_pose_tmp.xml

echo -e $RESET $GREEN $NL"Done"$RESET
