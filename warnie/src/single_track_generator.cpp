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
#include <fstream>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/classification.hpp> // Include boost::for is_any_of
#include <boost/algorithm/string/split.hpp> // Include for boost::split

struct TrapData
{
  TrapData( std::string name, float height = 0, float lenght = 0 )
  : name_(name), height_(height), lenght_(lenght)
  {}

  std::string name_ = "";
  float height_ = 0;
  float lenght_ = 0;
};

std::vector<TrapData> trap_data;
uint8_t nr_of_cont_tracks = 5;
const float track_start_dist = 10;
float gate_trap_dist = 3;
float gate_gate_dist = 10;
std::string trap_list_file = "";
std::string track_name_prefix = "track";
std::string gates_enabled = "false";
std::string randomize = "true";

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
    if (argc == 8)
    {
      nr_of_cont_tracks = std::stoi(argv[1]);
      randomize = argv[2];
      trap_list_file = argv[3];
      track_name_prefix = argv[4];
      gates_enabled = argv[5];
      gate_trap_dist = std::atof(argv[6]);
      gate_gate_dist = std::atof(argv[7]);
    }
    else
    {
      std::cout << "Invalid number of input arguments. "
                << "Usage: <nr_of_gen_tracks> <randomize> <trap_list_path> <track_name> <gates_enabled> <g_t_dist> <g_g_dist>\n";
      return 1;
    }

    /*
     * Get the base path
     */
    std::string base_path = ros::package::getPath(ROS_PACKAGE_NAME);
    std::string models_folder = "/test_models/";

    /*
     * Read the track file
     */
    std::string line;
    std::ifstream myfile (base_path + trap_list_file);
    if (myfile.is_open())
    {
      while ( getline (myfile, line) )
      {
        std::vector<std::string> parameters;
        boost::split(parameters, line, boost::is_any_of(", "), boost::token_compress_on);

        if (parameters.size() == 2)
        {
          trap_data.emplace_back( parameters.at(0)
                                , std::atof(parameters.at(1).c_str()) );
        }

        if (parameters.size() == 3)
        {
          trap_data.emplace_back( parameters.at(0)
                                , std::atof(parameters.at(1).c_str())
                                , std::atof(parameters.at(2).c_str()) );
        }

      }
      myfile.close();
    }

    std::cout << "Imported " << trap_data.size() << " traps\n";

    /*
     * Import the templates
     */
    tp::TemplateContainer t_track_sdf(base_path + "/track_templates/track_sdf.xml");
    tp::TemplateContainer t_track_cfg(base_path + "/track_templates/track_config.xml");
    tp::TemplateContainer t_import_model(base_path + "/track_templates/import_model.xml");

    /*
     * Generate the tracks
     */
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine rng(seed);

    std::cout << "Generating " << (int)nr_of_cont_tracks << " tracks based on "
              << trap_list_file << " ... " << std::flush;

    for (uint8_t i=0; i<nr_of_cont_tracks; i++)
    {
      std::string traps;
      std::string track_name = track_name_prefix + "_" + std::to_string(i);
      std::vector<TrapData> trap_data_cpy = trap_data;
      float gate_x = track_start_dist;
      float trap_x = 0;
      float previous_trap_len = 0;
      float trap_starting_dist = 0;

      if (randomize == "true")
      {
        std::shuffle(std::begin(trap_data_cpy), std::end(trap_data_cpy), rng);
      }

      // Insert the traps to the continuous track
      for (const TrapData& trap : trap_data_cpy)
      {
        trap_x = gate_x;

        // Add the gate model
        if (gates_enabled == "true")
        {
          trap_x += gate_trap_dist;
          std::stringstream gate_x_stream;
          gate_x_stream << std::fixed << std::setprecision(1) << gate_x;

          t_import_model.setArgument("model_name", "study_track_gate_block");
          t_import_model.setArgument("x", gate_x_stream.str());
          t_import_model.setArgument("z", "0");
          traps += t_import_model.processTemplate();
        }
        else
        {
          gate_x += gate_trap_dist;
          trap_x = gate_x;
        }

        // Add trap model
        std::stringstream trap_x_stream;
        trap_x_stream << std::fixed << std::setprecision(1) << trap_x;

        t_import_model.setArgument("model_name", trap.name_);
        t_import_model.setArgument("x", trap_x_stream.str());
        t_import_model.setArgument("z", std::to_string(trap.height_));
        traps += t_import_model.processTemplate();

        // Offset the gate distance
        if (trap.lenght_ == 0)
        {
          previous_trap_len = gate_gate_dist;
        }
        else
        {
          previous_trap_len = trap.lenght_;
        }

        gate_x += previous_trap_len;
      }

      // Create a gazebo model folder structure
      boost::filesystem::create_directories(base_path + models_folder + track_name);

      // Generate the continuous track SDF file
      t_track_sdf.setArgument("track_name", track_name);
      t_track_sdf.setArgument("traps", traps);
      t_track_sdf.processAndSaveTemplate(base_path + models_folder + track_name, "model");

      // Generate the continuous track config file
      t_track_cfg.setArgument("track_name", track_name);
      t_track_cfg.processAndSaveTemplate(base_path + models_folder + track_name, "model");
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
