#include <ignition/math/Pose3.hh>
#include "gazebo/physics/physics.hh"
#include "gazebo/common/common.hh"
#include "gazebo/gazebo.hh"

namespace gazebo
{
class SaveWorld : public WorldPlugin
{
  public: void Load(physics::WorldPtr _parent, sdf::ElementPtr _sdf)
  {
    // Get the base path
    if (_sdf->HasElement("data_path"))
    {
      base_path_ = _sdf->GetElement("data_path")->GetValue()->GetAsString();
    }

    // Get the name of the gazebo world
    if (_sdf->HasElement("world_name"))
    {
      world_name_ = _sdf->GetElement("world_name")->GetValue()->GetAsString();
    }

    // Save the gazebo world
    _parent->Save(base_path_ + world_name_ + ".world");

    std::cout << "Gazebo world is saved in: " << base_path_ + world_name_ << std::endl;
  }

  private: std::string base_path_ = "/home/robert/robosemiotics_study/";
  private: std::string world_name_;
};

// Register this plugin with the simulator
GZ_REGISTER_WORLD_PLUGIN(SaveWorld)
}
