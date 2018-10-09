#!/bin/bash

RED="\e[31m"
YELLOW="\e[33m"
GREEN="\e[32m"
BOLD="\e[1m"
NL="\n"
RESET="\e[39m\e[0m"

# Success/failure control function
check_success() {
  if [[ $? != 0 ]]; then
    echo -e $RED$BOLD$1". Exiting"$RESET
    exit
  fi
}

ROBOSEMIOTICS_PTH=~/robosemiotics_study
WARNIE_PTH=/home/robert/catkin_ws/src/warnie/warnie
SUBJECT_COUNTER_PTH=$ROBOSEMIOTICS_PTH/subject_counter.txt
GAZEBO_WORLDS_PTH=worlds/
NR_OF_WORLDS=9

echo -e $GREEN$BOLD"Starting the robosemiotics user study" $SUBJECT_NR$RESET$NL

# Create robosemiotics folder
mkdir -p $ROBOSEMIOTICS_PTH/data
check_success "Failed to create data storage directories"

# Create the counter file
find $SUBJECT_COUNTER_PTH > /dev/null 2>&1
if [[ $? != 0 ]]; then
  echo -e $GREEN"* Creating a subject counter file "$RESET
  echo 0 > $SUBJECT_COUNTER_PTH
fi

# Get the subject nr
SUBJECT_NR=$(($(cat $SUBJECT_COUNTER_PTH)+1))
check_success "Failed to read the subject counter file"
echo -e $GREEN"* Running the user study on subject nr:" $SUBJECT_NR$RESET

# Load the simulation environment
GAZEBO_WORLD="study_track_$(((($SUBJECT_NR-1) % NR_OF_WORLDS) + 1)).world"
echo -e $GREEN"* Loading "$GAZEBO_WORLD$RESET
trap 'kill %1;' SIGINT
roslaunch warnie husky_in_world.launch joystick_enabled:=true gazebo_world:=$GAZEBO_WORLD load_rviz:=true & rosbag record -O $ROBOSEMIOTICS_PTH/husky_image_raw_compressed.bag /husky_warnie/image_raw/compressed
wait
check_success "Failed to load the simulation environment"

# Create subject specific data folder and move all the data into this folder
echo -e $GREEN"* Formating the data"$RESET
STUDY_DATA=$ROBOSEMIOTICS_PTH/data/subject_nr_$SUBJECT_NR
mkdir $STUDY_DATA
mv $ROBOSEMIOTICS_PTH/husky_trajectory.csv $STUDY_DATA/
mv $ROBOSEMIOTICS_PTH/husky_image_raw_compressed.bag $STUDY_DATA/
mv $ROBOSEMIOTICS_PTH/$GAZEBO_WORLD $STUDY_DATA/
python2.7 $WARNIE_PTH/scripts/data_processing_scripts/format_objects.py $STUDY_DATA/$GAZEBO_WORLD $STUDY_DATA/track_objects.csv
check_success "Failed to move the data"

# Increment the subject number
echo -e $GREEN"* Incrementing the subject counter "$RESET
echo "$SUBJECT_NR" > $SUBJECT_COUNTER_PTH
check_success "Failed to increment the subject counter"

echo -e $NL$GREEN$BOLD"Experiment finished successfully."$RESET$NL
