#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include "ros/ros.h"
#include "spiked_visual_cue.h"

namespace gazebo
{

  /**
   * @brief The SpikedVisualCuePlugin class
   */
  class SpikedVisualCuePlugin : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr _sdf)
    {
      // Store the pointer to the model
      this->model = _parent;

      // Get the offset request
      bool offset_visual = false;
      if (_sdf->HasElement("offset_visual"))
      {
        offset_visual = true;
      }

      // Initialize the visual cue helper class
      std::string link_full_name = model->GetName() + "::" + model->GetLink()->GetName();

      visual_cue_ = new SpikedVisualCue(
                    model->GetLink()->GetVisualMessage(link_full_name + "::visual"),
                    model->GetLink()->GetBoundingBox(),
                    offset_visual);

      // Create the node
      this->node = transport::NodePtr(new transport::Node());

      // Initialize the node
      this->node->Init(this->model->GetWorld()->GetName());

      // Set up the visual publisher
      this->visPub = this->node->Advertise<msgs::Visual>("~/visual", 20);

      /*
       * TODO: This loop publishes the spiked visuals 7000 times. First of all
       * it should be just 1 time but in that case gazebo server just ignores
       * the messages. Seconndly, 7000 is an arbitrary number that worked for
       * my machine.
       */
      for (iterations=0; iterations<7000; iterations++)
      {
        for (SpikeHelper& visual : visual_cue_->getSpikes())
        {
          msgs::Visual visual_msg = visual.toVisualMsg();
          this->visPub->Publish(visual_msg);
        }

        for (LineHelper& line : visual_cue_->getLines())
        {
          msgs::Visual visual_msg = line.toVisualMsg();
          this->visPub->Publish(visual_msg);
        }
      }

      iterations = 0;

      // Listen to the update event. This event is broadcast every
      // simulation iteration.
//      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
//          std::bind(&SpikedVisualCuePlugin::OnUpdate, this));

    }

    // Called by the world update start event
    public: void OnUpdate()
    {

    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    // Visual publisher
    private: transport::PublisherPtr visPub;

    // Node
    private: transport::NodePtr node;

    // Visual cue manager class
    private: SpikedVisualCue* visual_cue_;

    private: int iterations = 0;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(SpikedVisualCuePlugin)
}

