#include "line_helper.h"

namespace gazebo
{

/*
 * Constructor
 */
LineHelper::LineHelper(math::Vector3 p0, math::Vector3 p1, msgs::Visual parent_visual, double z_offset)
: visual_msg_(parent_visual),
  z_offset_(z_offset)
{
  id_ = std::rand();
  name_ = "line_" + std::to_string(id_);

  direction_ = (p1 - p0).Normalize();
  length_ = (p1 - p0).GetLength();

  math::Vector3 pos = p0 + (p1 - p0)/2;
  pos_.set_x(pos.x);
  pos_.set_y(pos.y);
  pos_.set_z(pos.z + z_offset_);

  setOrientationAlongDirection();

  initVisual();
}

/*
 * initVisual
 */
void LineHelper::initVisual()
{
  visual_msg_.set_type(msgs::Visual_Type_VISUAL);

  msgs::CylinderGeom* cylinder = new msgs::CylinderGeom();
  cylinder->set_radius(0.02);
  cylinder->set_length(length_);

  geometry_.set_allocated_cylinder(cylinder);
  geometry_.set_type(msgs::Geometry_Type_CYLINDER);

  msgs::Color* color = new msgs::Color();
  color->set_r(1);
  color->set_g(0.4);
  color->set_b(0);
  color->set_a(0.6);

  material_.set_allocated_diffuse(color);
}

/*
 * setOrientationAlongDirection
 */
void LineHelper::setOrientationAlongDirection()
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
 * toVisualMsg
 */
msgs::Visual LineHelper::toVisualMsg()
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
 * setOffsetZ
 */
void LineHelper::setOffsetZ( double z_offset )
{
  z_offset_ = z_offset;
  pos_.set_z(pos_.z() + z_offset_);
}

} // gazebo namespace
