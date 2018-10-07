#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

#include "ros/package.h"

#include <fstream>

namespace gazebo
{
  class ModelLogger : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      std::cout << "TERE MAAILM!!!!!\n";
      std::cout << "TERE MAAILM!!!!!\n";
      std::cout << "TERE MAAILM!!!!!\n";
      std::cout << "TERE MAAILM!!!!!\n";

      // Store the pointer to the model
      this->model = _parent;

      base_path_ = ros::package::getPath(ROS_PACKAGE_NAME) +  "/test/";

      std::cout << base_path_ << std::endl;

      // Open the data logging output stream
      log_stream_output_.open("~/catkin_ws/src/warnie/warnie/test/test.txt", std::ofstream::out);

      // Listen to the update event. This event is broadcast every simulation iteration.
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&ModelLogger::OnUpdate, this));
    }

    // Called by the world update start event
    public: void OnUpdate()
    {
      // Get the pose of the model
      gazebo::math::Pose model_pose;
      model_pose = this->model->GetWorldPose();

      log_stream_ << std::to_string(model_pose.pos.x) << " ";
      log_stream_ << std::to_string(model_pose.pos.y) << " ";
      log_stream_ << std::to_string(model_pose.pos.z) << "\n";

      if (sim_event_counter_ > log_buf_size_)
      {
            std::cout << "update\n";
        // Write the log stream
        log_stream_output_ << log_stream_.str().c_str();

        // Clear the log stream
        log_stream_.flush();
        //log_stream_output_.flush();

        // Reset the counter
        sim_event_counter_ = 0;
      }
      else
      {
        sim_event_counter_++;
      }
    }


    private: ~ModelLogger()
    {
      std::cout << "Hyvasti MAAILM!!!!!\n";
      std::cout << "Hyvasti MAAILM!!!!!\n";
      log_stream_output_.close();
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    private: std::ofstream log_stream_output_;
    private: std::stringstream log_stream_;
    private: unsigned int sim_event_counter_ = 0;
    private: unsigned int log_buf_size_ = 100;
    private: std::string base_path_;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(ModelLogger)
}
