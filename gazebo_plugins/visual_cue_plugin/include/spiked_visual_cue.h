#ifndef GAZEBO_SPIKED_VISUAL_CUE_H
#define GAZEBO_SPIKED_VISUAL_CUE_H

#include <gazebo/gazebo.hh>
#include <ignition/math/Vector3.hh>
#include "line_helper.h"
#include "spike_helper.h"

namespace gazebo
{

/**
 * @brief Creates and manages the visual cues around the parent model
 */
class SpikedVisualCue
{

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Public members
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
public:

/**
 * @brief Constructs the visual cue based on the parent visual
 * @param Visual of the parent
 * @param Bounding box of the parent
 */
SpikedVisualCue(msgs::Visual parent_visual, math::Box parent_bb, bool offset_visual);

/**
 * @brief Returns the spike objects
 * @return
 */
std::vector<SpikeHelper>& getSpikes();

/**
 * @brief Returns the line objects
 * @return
 */
std::vector<LineHelper>& getLines();

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Private members
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
private:

/**
 * @brief Initialize the 8 spikes and 12 lines
 */
void initVisuals();

/**
 * @brief Initialize the base spike object. Used for
 * constructing the other spikes
 */
void initBaseSpike();

msgs::Visual parent_visual_;
SpikeHelper base_spike_;
std::vector<SpikeHelper> spikes_;
std::vector<LineHelper> lines_;
double scaling_factor_ = 0.1;
const uint16_t nr_of_spikes_ = 8;
const uint16_t nr_of_lines_ = 12;
double parent_size_;
math::Box parent_bb_;
math::Vector3 parent_bb_vec_;
double z_offset_;

};

}// gazebo namespace

#endif
