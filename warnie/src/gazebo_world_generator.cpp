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
std::string gazebo_world_name_prefix = "track";
std::string gazebo_world_name;
std::string world_output_path;

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
      gazebo_world_name = argv[1];
      model_list_file = argv[2];
      world_output_path = argv[3];
    }
    else
    {
      std::cout << "Invalid number of input arguments. " << "Usage: <gazebo_world_name> <model_list> <data_out_dir>\n";
      return 1;
    }

    /*
     * Get the base path
     */
    std::string base_path = ros::package::getPath(ROS_PACKAGE_NAME);
    std::string worlds_folder = "/generated_worlds/";

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

    std::cout << "Imported " << model_data.size() << " models from "
              << base_path + model_list_file << std::endl;

    /*
     * Import the templates
     */
    tp::TemplateContainer t_gazebo_world(base_path + "/track_templates/gazebo_world.xml");
    tp::TemplateContainer t_import_model(base_path + "/track_templates/import_model.xml");

    /*
     * Combine the models
     */
    std::cout << "Generating a gazebo world ..." << std::endl;
    std::string models;

    for (const ModelData& model : model_data)
    {   
      t_import_model.setArgument("model_name", model.name_);
      t_import_model.setArgument("static", "true");
      t_import_model.setArgument("x", std::to_string(model.x_));
      models += t_import_model.processTemplate();
    }

    // Generate the continuous track SDF file
    t_gazebo_world.setArgument("world_name", gazebo_world_name);
    t_gazebo_world.setArgument("models", models);
    t_gazebo_world.setArgument("data_path", world_output_path);
    t_gazebo_world.processAndSaveTemplate(base_path + worlds_folder, gazebo_world_name);

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
