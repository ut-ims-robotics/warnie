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


typedef std::vector<std::pair<std::string, float>> pairvec;

pairvec continuous_trap_data;
uint8_t nr_of_cont_tracks = 5;
const float track_start_dist = 10;
const float gate_trap_dist = 3;
const float gate_gate_dist = 10;
std::string trap_list_file = "";
std::string track_name_prefix = "track";
std::string gates_enabled = "false";

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
    if (argc == 4)
    {
      nr_of_cont_tracks = std::stoi(argv[1]);
      trap_list_file = argv[2];
      track_name_prefix = argv[3];
      gates_enabled = argv[4];
    }
    else
    {
      std::cout << "Invalid number of input arguments. "
                << "Usage: <nr_of_gen_tracks> <trap_list_path> <track_name> <gates_enabled>\n";
      return 1;
    }

    /*
     * Get the base path
     */
    std::string base_path = ros::package::getPath(ROS_PACKAGE_NAME);
    std::string models_folder = "/gazebo_models/";

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
        continuous_trap_data.push_back( {parameters.at(0), std::atof(parameters.at(1).c_str())} );
      }
      myfile.close();
    }

    std::cout << "Imported " << continuous_trap_data.size() << " traps\n";

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

    std::cout << "Generating " << (int)nr_of_cont_tracks << " continuous tracks ... " << std::flush;

    for (uint8_t i=0; i<nr_of_cont_tracks; i++)
    {
      std::string traps;
      std::string track_name = track_name_prefix + "_" + std::to_string(i);
      pairvec c_trap_data_cpy = continuous_trap_data;
      std::shuffle(std::begin(c_trap_data_cpy), std::end(c_trap_data_cpy), rng);

      // Insert the traps to the continuous track
      for(uint8_t k=0; k<c_trap_data_cpy.size(); k++)
      {
        // Add the gate model
        float gate_x = track_start_dist + gate_gate_dist*k;
        std::stringstream gate_x_stream;
        gate_x_stream << std::fixed << std::setprecision(1) << gate_x;

        if (gates_enabled == "true")
        {
          t_import_model.setArgument("model_name", "study_track_gate_block");
          t_import_model.setArgument("x", gate_x_stream.str());
          t_import_model.setArgument("z", "0");
          traps += t_import_model.processTemplate();
        }

        // Add trap model
        float trap_x = gate_x + gate_trap_dist;
        std::stringstream trap_x_stream;
        trap_x_stream << std::fixed << std::setprecision(1) << trap_x;

        t_import_model.setArgument("model_name", c_trap_data_cpy.at(k).first);
        t_import_model.setArgument("x", trap_x_stream.str());
        t_import_model.setArgument("z", std::to_string(c_trap_data_cpy.at(k).second));
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
