#include "spike_helper.h"

namespace gazebo
{

/*
 * Default constructor
 */
SpikeHelper::SpikeHelper(){}

/*
 * Constructor
 */
SpikeHelper::SpikeHelper(msgs::Visual visual_msg)
: visual_msg_(visual_msg),
  material_(visual_msg.material()),
  geometry_(visual_msg.geometry()),
  scale_(visual_msg.scale()),
  pose_ (visual_msg.pose()),
  pos_  (pose_.position()),
  ori_ (pose_.orientation()),
  id_ (visual_msg.id()),
  name_ (visual_msg.name())
{}

/*
 * toVisualMsg
 */
msgs::Visual SpikeHelper::toVisualMsg()
{
  msgs::Pose* pose = new msgs::Pose();
  pose->set_allocated_position(new msgs::Vector3d(pos_));
  pose->set_allocated_orientation(new msgs::Quaternion(ori_));

  visual_msg_.set_allocated_pose(pose);
  visual_msg_.set_allocated_material(new msgs::Material(material_));
  visual_msg_.set_allocated_geometry(new msgs::Geometry(geometry_));
  visual_msg_.set_allocated_name(new std::string(name_));
  visual_msg_.set_id(id_);

  return visual_msg_;
}

/*
 * setPositionAlongDirection
 */
void SpikeHelper::setPositionAlongDirection()
{
  pos_.set_x( direction_.x * distance_ );
  pos_.set_y( direction_.y * distance_ );
  pos_.set_z( direction_.z * distance_ + z_offset_ );
}

/*
 * setOrientationAlongDirection
 */
void SpikeHelper::setOrientationAlongDirection()
{
  // Find the rotation axis, which is perpendicular to the direction_ vector
  math::Vector3 up_axis(0, 0, 1);
  math::Vector3 rotation_axis = up_axis.Cross(direction_);

  double angle = acos( direction_.Dot(up_axis) );

  // Rotate the quaternion in the direction of rotation_axis
  math::Quaternion quat;
  quat.SetFromAxis(rotation_axis, angle);
  quat.Normalize();

  ori_.set_x( quat.x );
  ori_.set_y( quat.y );
  ori_.set_z( quat.z );
  ori_.set_w( quat.w );
}

/*
 * setOffsetZ
 */
void SpikeHelper::setOffsetZ( double z_offset )
{
  z_offset_ = z_offset;
}

}// gazebo namespace
