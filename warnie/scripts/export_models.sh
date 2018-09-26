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

WARNIE_MODELS_DIR=$(pwd)"/gazebo_models/."
GAZEBO_MODELS_DIR=$(eval echo ~$USER)"/.gazebo/models"

# Copy the models from warnie models dir to gazebo models dir
cp -r $WARNIE_MODELS_DIR $GAZEBO_MODELS_DIR

# Check if the process was successful or not
check_success "Failed to copy files"




