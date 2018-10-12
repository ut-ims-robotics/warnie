#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>

#include "ros/package.h"
#include "ros/ros.h"
#include <sensor_msgs/Joy.h>
#include "std_msgs/Bool.h"
#include "std_msgs/Float32MultiArray.h"

#include <fstream>

namespace gazebo
{
  class ModelPoseReset : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      // Store the pointer to the model
      this->model = _parent;

      // Subscribe to joystick messages
      joy_subscriber_ = nh_.subscribe<sensor_msgs::Joy>("/husky_warnie/joy", 10, &ModelPoseReset::joyCallback, this);

      // Subscribe to remote reset messages
      remote_reset_subscriber_ = nh_.subscribe("reset_model", 1, &ModelPoseReset::remoteResetCallback, this);

      // Create the timer
      timer_ = nh_.createTimer(ros::Duration(0.1), &ModelPoseReset::timerCallback, this);

      ROS_INFO_STREAM("Model pose reset plugin ready");
    }

    private: void joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
    {
      if (can_reset_ &&
          joy->buttons[2] == 1 &&
          joy->buttons[4] == 1 &&
          joy->buttons[5] == 1)
      {
        resetModelPose();
        reset_start_time_ = ros::Time::now();
        can_reset_ = false;
      }
    }

    private: void remoteResetCallback(const std_msgs::Float32MultiArray& reset_msg)
    {
      if (reset_msg.data[0] != 1.0)
      {
        return;
      }

      if (reset_msg.data[1] == 1)
      {
        ROS_INFO_STREAM("Resetting the pose");

        math::Pose model_pose = model->GetWorldPose();

        if (reset_msg.data[2] == -101)
        {
          model_pose.pos.Set(model_pose.pos.x, reset_msg.data[3], reset_msg.data[4]);
        }
        else
        {
          model_pose.pos.Set(reset_msg.data[2], reset_msg.data[3], reset_msg.data[4]);
        }

        model_pose.rot.SetFromEuler(0, 0, 0);
        model->SetWorldPose(model_pose);
      }
      else
      {
        resetModelPose();
      }
    }

    private: void resetModelPose()
    {
      ROS_INFO_STREAM("Resetting the pose");

      math::Pose model_pose = model->GetWorldPose();
      model_pose.pos.Set(model_pose.pos.x, 0, model_pose.pos.z + 0.2);
      model_pose.rot.SetFromEuler(0, 0, 0);

      model->SetWorldPose(model_pose);
    }

    private: void timerCallback(const ros::TimerEvent&)
    {
      if (!can_reset_)
      {
        ros::Duration timediff = ros::Time::now() - reset_start_time_;
        if (timediff >= ros::Duration(2))
        {
          can_reset_ = true;
        }
      }
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    // ROS nodehandle
    private: ros::NodeHandle nh_;

    // reset timer
    ros::Timer timer_;

    // Joy subscriber
    private: ros::Subscriber joy_subscriber_;

    // Remote reset subscriber
    private: ros::Subscriber remote_reset_subscriber_;

    private: ros::Time reset_start_time_;

    private: bool can_reset_ = true;

  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(ModelPoseReset)
}
