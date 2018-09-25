cmake_minimum_required(VERSION 2.8.3)
project(warnie)

add_compile_options(-std=c++1y)

find_package(catkin REQUIRED 
  roscpp
  file_template_parser
)

catkin_package(
  LIBRARIES ft_parser
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(continuous_track_gen src/continuous_track_gen.cpp)
add_dependencies(continuous_track_gen ${catkin_EXPORTED_TARGETS} ${${PROJECT_NAME}_EXPORTED_TARGETS})
target_link_libraries(continuous_track_gen ${catkin_LIBRARIES} ft_parser)
