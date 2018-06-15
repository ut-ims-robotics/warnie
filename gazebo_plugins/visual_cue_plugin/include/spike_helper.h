#ifndef GAZEBO_SPIKE_HELPER_H
#define GAZEBO_SPIKE_HELPER_H

#include <gazebo/gazebo.hh>

namespace gazebo
{

/**
 * @brief Class that helps to manage spike objects
 */
class SpikeHelper
{
public:

  /**
   * @brief Default constructor
   */
  SpikeHelper();

  /**
   * @brief Constructor
   * @param visual_msg
   */
  SpikeHelper(msgs::Visual visual_msg);

  /**
   * @brief Formats the spike into a gazebo visual message
   * @return Visual message
   */
  msgs::Visual toVisualMsg();

  /**
   * @brief Sets the position of the spike to the direction
   * it poits to
   */
  void setPositionAlongDirection();

  /**
   * @brief Sets the orientation along the @direction_
   */
  void setOrientationAlongDirection();

  /**
   * @brief Sets the offset along z axis of the parent object
   * @param z_offset
   */
  void setOffsetZ( double z_offset );

  msgs::Visual visual_msg_;
  msgs::Material material_;
  msgs::Geometry geometry_;
  msgs::Vector3d scale_;
  math::Vector3 direction_;
  double distance_;
  msgs::Pose pose_;
  msgs::Vector3d pos_;
  msgs::Quaternion ori_;
  int32_t id_;
  std::string name_;
  const float pi_ = 3.1416;
  double z_offset_ = 0;

};

}// gazebo namespace

#endif
