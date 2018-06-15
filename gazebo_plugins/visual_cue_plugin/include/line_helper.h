#ifndef GAZEBO_LINE_HELPER_H
#define GAZEBO_LINE_HELPER_H

#include <gazebo/gazebo.hh>

namespace gazebo
{

class LineHelper
{
public:

  /**
   * @brief Constructor
   * @param p0 Starting point of the line
   * @param p1 Ending point of the line
   * @param parent_visual Visual of the parent object
   * @param z_offset Z axis offset of the line
   */
  LineHelper(math::Vector3 p0, math::Vector3 p1, msgs::Visual parent_visual, double z_offset = 0);

  /**
   * @brief Initializes the visual aspects of the line
   */
  void initVisual();

  /**
   * @brief Sets the visual of the line parallel to the direction given by the two points
   */
  void setOrientationAlongDirection();

  /**
   * @brief Formats the line into a gazebo visual message
   * @return Visual message
   */
  msgs::Visual toVisualMsg();

  /**
   * @brief setOffsetZ
   * @param z_offset
   */
  void setOffsetZ( double z_offset );

  msgs::Visual visual_msg_;
  msgs::Material material_;
  msgs::Geometry geometry_;
  msgs::Vector3d scale_;
  msgs::Pose pose_;
  msgs::Vector3d pos_;
  msgs::Quaternion ori_;
  int32_t id_;
  std::string name_;
  math::Vector3 direction_;
  double length_;
  double z_offset_ = 0;

};

} // gazebo namespace
#endif
