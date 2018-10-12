cmake_minimum_required(VERSION 2.8.3)
project(visual_cue_plugin)
add_compile_options(-std=c++11)

# Load catkin and all dependencies required for this package
find_package(catkin REQUIRED COMPONENTS 
  roscpp 
  gazebo_ros
)

# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

catkin_package(
  INCLUDE_DIRS include
  DEPENDS 
    roscpp 
    gazebo_ros 
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

#add_library(${PROJECT_NAME} src/visual_cue_plugin.cpp
#                            src/line_helper.cpp
#                            src/spike_helper.cpp
#                            src/spiked_visual_cue.cpp)
#target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

#add_library(${PROJECT_NAME}_vis src/model_cue_plugin_vis.cpp)
#target_link_libraries(${PROJECT_NAME}_vis ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

add_library(${PROJECT_NAME}_model src/model_logger_plugin.cpp)
target_link_libraries(${PROJECT_NAME}_model ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

add_library(${PROJECT_NAME}_model_reset src/model_pose_reset_plugin.cpp)
target_link_libraries(${PROJECT_NAME}_model ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})

add_library(${PROJECT_NAME}_world src/model_import_plugin.cpp)
target_link_libraries(${PROJECT_NAME}_world ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})
