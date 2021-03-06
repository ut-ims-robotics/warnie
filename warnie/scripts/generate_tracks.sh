#!/bin/bash

RED="\e[31m"
YELLOW="\e[33m"
GREEN="\e[32m"
BOLD="\e[1m"
NL="\n"
RESET="\e[39m\e[0m"

# 
check_success() {
  if [[ $? != 0 ]]; then
    echo -e $RED$BOLD$1". Exiting"$RESET
    exit
  fi
}

TRAP_LISTS_DIR="/trap_lists"
NR_OF_TRACKS=3
NR_OF_PARTITIONS=3

# Generate 9 continuous tracks
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p1.txt track_continuous_p1 true 5 11
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p2.txt track_continuous_p2 true 5 11
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p3.txt track_continuous_p3 true 5 11

# Check if the process was successful or not
check_success "Failed to generate continuous tracks"

# Generate 9 discrete tracks
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p1.txt track_discrete_p1 false 0 15
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p2.txt track_discrete_p2 false 0 15
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p3.txt track_discrete_p3 false 0 15

# Check if the process was successful or not
check_success "Failed to generate discrete tracks"

# Generate 9 biased tracks
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_biased_p1.txt track_biased_p1 true 13 20
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_biased_p2.txt track_biased_p2 true 13 20
rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_biased_p3.txt track_biased_p3 true 13 20

# Check if the process was successful or not
check_success "Failed to generate biased tracks"

# Combine the tracks to a track list
TRACK_LIST_DIR="track_list_tmp"
mkdir $TRACK_LIST_DIR
WORLD_OUTPUT_DIR=/home/robert/robosemiotics_study/

for (( p=0; p < $NR_OF_PARTITIONS; p++ )); do
  for (( i=0; i < $NR_OF_TRACKS; i++ )); do
    p_i1=$(((($p+0) % 3) +1))
    p_i2=$(((($p+1) % 3) +1))
    p_i3=$(((($p+2) % 3) +1))
    idx=$(($p*3 + $i + 1))

    TRACK_LIST_NAME=$TRACK_LIST_DIR/"track_list_p${p}_${i}_tmp.txt"

    echo "track_continuous_p${p_i1}_${i}, 5" >> $TRACK_LIST_NAME
    echo "track_discrete_p${p_i2}_${i}, 140" >> $TRACK_LIST_NAME
    echo "track_biased_p${p_i3}_${i}, 250" >> $TRACK_LIST_NAME
    
    rosrun warnie gazebo_world_generator study_track_${idx} /$TRACK_LIST_NAME $WORLD_OUTPUT_DIR
  done
done

rm -rf $TRACK_LIST_DIR
