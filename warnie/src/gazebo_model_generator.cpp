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

struct ModelData
{
  ModelData( std::string name, float x = 0 )
  : name_(name), x_(x)
  {}

  std::string name_ = "";
  float x_ = 0;
};

std::vector<ModelData> model_data;
std::string model_list_file = "";
std::string combined_model_name_prefix = "track";
std::string combined_model_name;

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
    if (argc == 3)
    {
      combined_model_name = argv[1];
      model_list_file = argv[2];
    }
    else
    {
      std::cout << "Invalid number of input arguments. " << "Usage: <combined_model_name> <model_list>\n";
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
    std::ifstream myfile (base_path + model_list_file);
    if (myfile.is_open())
    {
      while ( getline (myfile, line) )
      {
        std::vector<std::string> parameters;
        boost::split(parameters, line, boost::is_any_of(", "), boost::token_compress_on);

        if (parameters.size() == 2)
        {
          model_data.emplace_back( parameters.at(0)
                                , std::atof(parameters.at(1).c_str()) );
        }
      }
      myfile.close();
    }

    std::cout << "Imported " << model_data.size() << " models\n";

    /*
     * Import the templates
     */
    tp::TemplateContainer t_track_sdf(base_path + "/track_templates/track_sdf.xml");
    tp::TemplateContainer t_track_cfg(base_path + "/track_templates/track_config.xml");
    tp::TemplateContainer t_import_model(base_path + "/track_templates/import_model.xml");

    /*
     * Combine the models
     */
    std::cout << "Combining the models" << std::endl;
    std::string models;

    for (const ModelData& model : model_data)
    {
      t_import_model.setArgument("model_name", model.name_);
      t_import_model.setArgument("x", std::to_string(model.x_));
      // t_import_model.setArgument("z", std::to_string(trap.x_));
      models += t_import_model.processTemplate();
    }

    // Create a gazebo model folder structure
    boost::filesystem::create_directories(base_path + models_folder + combined_model_name);

    // Generate the continuous track SDF file
    t_track_sdf.setArgument("track_name", combined_model_name);
    t_track_sdf.setArgument("traps", models);
    t_track_sdf.processAndSaveTemplate(base_path + models_folder + combined_model_name, "model");

    // Generate the continuous track config file
    t_track_cfg.setArgument("track_name", combined_model_name);
    t_track_cfg.processAndSaveTemplate(base_path + models_folder + combined_model_name, "model");

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
