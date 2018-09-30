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

## Generate 9 continuous tracks
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p1.txt track_continuous_p1 true $NR_OF_TRACKS 10
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p2.txt track_continuous_p2 true $NR_OF_TRACKS 10
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_continuous_p3.txt track_continuous_p3 true $NR_OF_TRACKS 10

## Check if the process was successful or not
#check_success "Failed to generate continuous tracks"

## Generate 9 discrete tracks
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p1.txt track_discrete_p1 false 0 10
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p2.txt track_discrete_p2 false 0 10
#rosrun warnie single_track_generator $NR_OF_TRACKS true $TRAP_LISTS_DIR/trap_list_discrete_p3.txt track_discrete_p3 false 0 10

for (( p=1; p <= $NR_OF_PARTITIONS; p++ )); do
  for (( i=0; i < $NR_OF_TRACKS; i++ )); do
    echo "track_continuous_p${p}_${i}" >> track_list${p}_tmp.txt
    echo "track_discrete_p${p}_${i}" >> track_list${p}_tmp.txt
  done
done

# Check if the process was successful or not
check_success "Failed to generate discrete tracks"




