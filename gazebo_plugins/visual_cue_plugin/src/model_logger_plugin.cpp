#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

#include "ros/package.h"
#include "ros/ros.h"

#include <fstream>

namespace gazebo
{
  class ModelLogger : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      // Store the pointer to the model
      this->model = _parent;

      // Get the base path
      if (_sdf->HasElement("data_path"))
      {
        base_path_ = _sdf->GetElement("data_path")->GetValue()->GetAsString();
      }

      // Get the subsampling nr
      if (_sdf->HasElement("subsamples"))
      {
        sub_samples_ = std::stoi(_sdf->GetElement("subsamples")->GetValue()->GetAsString());
      }

      // Open the data logging output stream
      log_stream_output_.open(base_path_ + "husky_trajectory.csv", std::ofstream::out);

      // Create a header for the log
      log_stream_ << "x(m),y(m),z(m),yaw(rad),time(s)\n";

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

      // Record every n'th data point
      if ((sim_event_counter_ % sub_samples_) == 0)
      {
        log_stream_ << std::to_string(model_pose.pos.x) << ",";
        log_stream_ << std::to_string(model_pose.pos.y) << ",";
        log_stream_ << std::to_string(model_pose.pos.z) << ",";
        log_stream_ << std::to_string(model_pose.rot.GetYaw()) << ",";
        log_stream_ << std::to_string(ros::Time::now().toSec()) << "\n";
      }

      if (sim_event_counter_ > log_buf_size_)
      {
        // Write the log stream
        log_stream_output_ << log_stream_.str().c_str() << std::flush;

        // Clear the log stream
        log_stream_.str( std::string() );
        log_stream_.clear();

        // Reset the counter
        sim_event_counter_ = 0;
      }
      else
      {
        sim_event_counter_++;
      }
    }


//    private: ~ModelLogger()
//    {
//      std::cout << "Hyvasti MAAILM!!!!!\n";
//      std::cout << "Hyvasti MAAILM!!!!!\n";
//      log_stream_output_.close();
//    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    private: std::ofstream log_stream_output_;
    private: std::stringstream log_stream_;
    private: unsigned int sim_event_counter_ = 0;
    private: unsigned int log_buf_size_ = 200;
    private: unsigned int sub_samples_ = 50;
    private: std::string base_path_ = "/home/robert/robosemiotics_study/";
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(ModelLogger)
}
