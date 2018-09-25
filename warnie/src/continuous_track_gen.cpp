#include "ros/ros.h"
#include "ros/package.h"
#include "file_template_parser/file_template_parser.h"
#include <stdexcept>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <sstream>
#include <iomanip>
#include <boost/filesystem.hpp>

const std::vector<std::string> continuous_trap_names = {
  "trap_c_4_a_1",
  "trap_c_4_a_1_m",
  "trap_c_4_a_2",
  "trap_c_4_a_2_m",
  "trap_c_4_r_1",
  "trap_c_4_r_1_m",
  "trap_c_4_r_2",
  "trap_c_4_r_2_m",
  "trap_c_4_n",
  "trap_c_4_n_m",
  "vis_cue_normal",
  "vis_cue_attract",
  "vis_cue_repel"
};

uint8_t nr_of_cont_tracks = 5;
const float track_start_dist = 10;
const float gate_trap_dist = 3;
const float gate_gate_dist = 7;

/*
 * MAIN
 */
int main(int argc, char **argv)
{
  try
  {
    /*
     * Get the commandline arguments
     */
    if (argc == 2)
    {
      nr_of_cont_tracks = std::stoi(argv[1]);
    }

    /*
     * Get the base path
     */
    std::string base_path = ros::package::getPath(ROS_PACKAGE_NAME);
    std::string models_folder = "/gazebo_models/";

    /*
     * Import the templates
     */
    tp::TemplateContainer t_track_c_sdf(base_path + "/track_templates/continuous_track_sdf.xml");
    tp::TemplateContainer t_track_c_cfg(base_path + "/track_templates/continuous_track_config.xml");
    tp::TemplateContainer t_import_model(base_path + "/track_templates/import_model.xml");

    /*
     * Generate the tracks
     */
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine rng(seed);

    std::cout << "Generating a continuous track ... " << std::flush;

    for (uint8_t i=0; i<nr_of_cont_tracks; i++)
    {
      std::string traps;
      std::string track_name = "continuous_track_" + std::to_string(i);
      std::vector<std::string> c_trap_names_cpy = continuous_trap_names;
      std::shuffle(std::begin(c_trap_names_cpy), std::end(c_trap_names_cpy), rng);

      // Insert the traps to the continuous track
      for(uint8_t k=0; k<c_trap_names_cpy.size(); k++)
      {
        // Add the gate model
        float gate_x = track_start_dist + gate_gate_dist*k;
        std::stringstream gate_x_stream;
        gate_x_stream << std::fixed << std::setprecision(1) << gate_x;

        t_import_model.setArgument("model_name", "study_track_gate_block");
        t_import_model.setArgument("x", gate_x_stream.str());
        t_import_model.setArgument("static", "true");
        traps += t_import_model.processTemplate();

        // Add trap model
        float trap_x = gate_x + gate_trap_dist;
        std::stringstream trap_x_stream;
        trap_x_stream << std::fixed << std::setprecision(1) << trap_x;

        t_import_model.setArgument("model_name", c_trap_names_cpy.at(k));
        t_import_model.setArgument("x", trap_x_stream.str());
        t_import_model.setArgument("static", "false");
        traps += t_import_model.processTemplate();
      }

      // Create a gazebo model folder structure
      boost::filesystem::create_directories(base_path + models_folder + track_name);

      // Generate the continuous track SDF file
      t_track_c_sdf.setArgument("track_name", track_name);
      t_track_c_sdf.setArgument("traps", traps);
      t_track_c_sdf.processAndSaveTemplate(base_path + models_folder + track_name, "model");

      // Generate the continuous track config file
      t_track_c_cfg.setArgument("track_name", track_name);
      t_track_c_cfg.processAndSaveTemplate(base_path + models_folder + track_name, "model");
    }

    std::cout << "done" << std::endl;
  }
  catch(std::runtime_error e)
  {
    ROS_ERROR_STREAM(e.what());
  }

  catch(std::exception e)
  {
    ROS_ERROR_STREAM(e.what());
  }

  return 0;
}
