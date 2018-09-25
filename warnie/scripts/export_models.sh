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

# Copy function
copy_files() {
  SRC_DIR=$1
  DST_DIR=$2
  FILES=$(ls $SRC_DIR)

  for FILE in ${FILES[*]}
  do
    cp -r $SRC_DIR/$FILE $DST_DIR
  done
}

WARNIE_MODELS_DIR=$(pwd)"/gazebo_models"
GAZEBO_MODELS_DIR=$(eval echo ~$USER)"/.gazebo/models"

# Copy the models from warnie models dir to gazebo models dir
copy_files $WARNIE_MODELS_DIR $GAZEBO_MODELS_DIR

# Check if the process was successful or not
check_success "Failed to copy files"




