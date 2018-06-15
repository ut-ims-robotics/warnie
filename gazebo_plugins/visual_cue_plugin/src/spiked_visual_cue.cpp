#include "spiked_visual_cue.h"

namespace gazebo
{

/*
 * Constructor
 */
SpikedVisualCue::SpikedVisualCue(msgs::Visual parent_visual, math::Box parent_bb, bool offset_visual)
: parent_visual_(parent_visual),
  base_spike_(parent_visual),
  parent_bb_(parent_bb)
{
  /* TODO: Thats yet another hack for getting the actual bounding
   * box of the model. If the object is rotated (its axes do not align
   * with world axes) then the bounding box is bigger than the actual
   * object. Due to this stupid reason, I came up with the following hack
   */
  if (parent_visual_.geometry().type() == msgs::Geometry_Type_BOX)
  {
    msgs::Vector3d parent_size = parent_visual_.geometry().box().size();
    parent_bb_vec_.x = parent_size.x();
    parent_bb_vec_.y = parent_size.y();
    parent_bb_vec_.z = parent_size.z();
  }
  else if (parent_visual_.geometry().type() == msgs::Geometry_Type_MESH)
  {
    // TODO: Hopeless case, no idea how to get the actual bounding box of a mesh
    parent_bb_vec_ = parent_bb.GetSize();
  }
  else
  {
    // Calculate the size of the parent based on its bounding box
    parent_bb_vec_ = parent_bb.GetSize();
  }

  // Calculate the diagonal size of the parents bounding box
  parent_size_ = parent_bb_vec_.GetLength();

  // Offset the visual
  if (offset_visual)
  {
    z_offset_ = parent_bb_.GetZLength()/2;
    base_spike_.setOffsetZ(z_offset_);
  }

  // Initialize the visuals
  initVisuals();
}

/*
 * getSpikes
 */
std::vector<SpikeHelper>& SpikedVisualCue::getSpikes()
{
  return spikes_;
}

/*
 * getLines
 */
std::vector<LineHelper>& SpikedVisualCue::getLines()
{
  return lines_;
}

/*
 * initVisuals
 */
void SpikedVisualCue::initVisuals()
{
  // Initialize base visual
  initBaseSpike();

  // Create the spikes
  for (int i=0; i<nr_of_spikes_; i++)
  {
    // Initialize the visual
    SpikeHelper spike = base_spike_;

    // Assign a unique id and name
    /* TODO: If ids are created incrementally (and we have at least 8 ids to create)
     * then ids will overlap with other object ids. Hence a random number is used
     * but there is still a probability, that an overlap will occur. I have no clue
     * what is Gazebo's id assignment convention, but currently it seems that Gazebo
     * will allocate a small window of ids (~7) for an object to use and this window
     * is allocated incremetally (obj_0 has ids from 0-7, obj_2 has id from 8-15).
     * Gazebo does not care if the object type is different, or names are unique,
     * it just looks at the ids ...
     * the trouble maker: visual.id_ = ++base_spike_.id_;
     */
    spike.id_ = std::rand();
    spike.name_ = spike.name_ + "_cue_" + std::to_string(spike.id_);
    //std::cout << "cis: " << visual.visual_msg_.visible() << std::endl;

    // Add the visual to the vec of visuals
    spikes_.push_back(spike);
  }

  /*
   * Set the relative position of the visual cues
   * TODO: Dunno how to do this in a loop
   */
  double x_dir = parent_bb_vec_.x/parent_size_;
  double y_dir = parent_bb_vec_.y/parent_size_;
  double z_dir = parent_bb_vec_.z/parent_size_;

  double pos_x = 1 * parent_bb_vec_.x/2 ;
  double pos_y = 1 * parent_bb_vec_.y/2;
  double pos_z = 1 * parent_bb_vec_.z/2;

  spikes_.at(0).direction_.x = x_dir;
  spikes_.at(0).direction_.y = y_dir;
  spikes_.at(0).direction_.z = z_dir;

  spikes_.at(1).direction_.x = x_dir;
  spikes_.at(1).direction_.y = -y_dir;
  spikes_.at(1).direction_.z = z_dir;

  spikes_.at(2).direction_.x = -x_dir;
  spikes_.at(2).direction_.y = -y_dir;
  spikes_.at(2).direction_.z = z_dir;

  spikes_.at(3).direction_.x = -x_dir;
  spikes_.at(3).direction_.y = y_dir;
  spikes_.at(3).direction_.z = z_dir;

  spikes_.at(4).direction_.x = x_dir;
  spikes_.at(4).direction_.y = y_dir;
  spikes_.at(4).direction_.z = -z_dir;

  spikes_.at(5).direction_.x = x_dir;
  spikes_.at(5).direction_.y = -y_dir;
  spikes_.at(5).direction_.z = -z_dir;

  spikes_.at(6).direction_.x = -x_dir;
  spikes_.at(6).direction_.y = -y_dir;
  spikes_.at(6).direction_.z = -z_dir;

  spikes_.at(7).direction_.x = -x_dir;
  spikes_.at(7).direction_.y = y_dir;
  spikes_.at(7).direction_.z = -z_dir;


  // Top
  LineHelper line_0(math::Vector3(pos_x, pos_y, pos_z + z_offset_),
                    math::Vector3(pos_x, -pos_y, pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_0);

  LineHelper line_1(math::Vector3(pos_x, -pos_y, pos_z + z_offset_),
                    math::Vector3(-pos_x, -pos_y, pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_1);

  LineHelper line_2(math::Vector3(-pos_x, -pos_y, pos_z + z_offset_),
                    math::Vector3(-pos_x, pos_y, pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_2);

  LineHelper line_3(math::Vector3(-pos_x, pos_y, pos_z + z_offset_),
                    math::Vector3(pos_x, pos_y, pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_3);

  // Bottom
  LineHelper line_4(math::Vector3(pos_x, pos_y, -pos_z + z_offset_),
                    math::Vector3(pos_x, -pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_4);

  LineHelper line_5(math::Vector3(pos_x, -pos_y, -pos_z + z_offset_),
                    math::Vector3(-pos_x, -pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_5);

  LineHelper line_6(math::Vector3(-pos_x, -pos_y, -pos_z + z_offset_),
                    math::Vector3(-pos_x, pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_6);

  LineHelper line_7(math::Vector3(-pos_x, pos_y, -pos_z + z_offset_),
                    math::Vector3(pos_x, pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_7);

  // Sides
  LineHelper line_8(math::Vector3(pos_x, pos_y, pos_z + z_offset_),
                    math::Vector3(pos_x, pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_8);

  LineHelper line_9(math::Vector3(pos_x, -pos_y, pos_z + z_offset_),
                    math::Vector3(pos_x, -pos_y, -pos_z + z_offset_),
                    base_spike_.visual_msg_);
  lines_.push_back(line_9);

  LineHelper line_10(math::Vector3(-pos_x, -pos_y, pos_z + z_offset_),
                     math::Vector3(-pos_x, -pos_y, -pos_z + z_offset_),
                     base_spike_.visual_msg_);
  lines_.push_back(line_10);

  LineHelper line_11(math::Vector3(-pos_x, pos_y, pos_z + z_offset_),
                     math::Vector3(-pos_x, pos_y, -pos_z + z_offset_),
                     base_spike_.visual_msg_);
  lines_.push_back(line_11);


  // Set the orientation and position of the cue along bounding box edge direction
  for (SpikeHelper& spike : spikes_)
  {
    spike.setOrientationAlongDirection();
    spike.setPositionAlongDirection();
  }
}

/*
 * initBaseSpike
 */
void SpikedVisualCue::initBaseSpike()
{
  // Set the size of the base spike
  msgs::Vector3d* size = new msgs::Vector3d();

  size->set_x( parent_size_ * scaling_factor_ * 1);
  size->set_y( parent_size_ * scaling_factor_ * 1);
  size->set_z( parent_size_ * scaling_factor_ * 1.4);

  msgs::MeshGeom* mesh_geom = new msgs::MeshGeom();
  mesh_geom->set_filename("/home/robert/catkin_ws/src/warnie/gazebo_plugins/visual_cue_plugin/models/blade.dae");
  mesh_geom->set_allocated_scale(size);

  base_spike_.geometry_.set_type(msgs::Geometry_Type_MESH);
  base_spike_.geometry_.set_allocated_mesh(mesh_geom);
  base_spike_.distance_ = 1 * parent_size_/2;

  // Set the color of the visual
  msgs::Color* color = new msgs::Color();

  color->set_r(1);
  color->set_g(0.4);
  color->set_b(0);
  color->set_a(0.6);

  base_spike_.material_.set_allocated_diffuse(color);
  base_spike_.material_.set_allocated_specular(new msgs::Color(*color));

  // Cast no shadows and set visible
  base_spike_.visual_msg_.set_cast_shadows(false);
  base_spike_.visual_msg_.set_visible(true);
}

}// gazebo namespace
