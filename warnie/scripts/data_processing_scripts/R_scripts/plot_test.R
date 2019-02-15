"
sources:
  - png plotting: http://rfunction.com/archives/2539
  - plot aspect ratio: r.789695.n4.nabble.com/scatter-plot-with-axes-drawn-on-the-same-scale-td804863.html
  - Resetting plot: https://stackoverflow.com/a/31909011/8068769
  - Saving to pdf: https://stackoverflow.com/a/7144203/8068769
"

# install.packages("png")
# install.packages("collections")
# install.packages("rjson")

library(png);
library(collections);
library(rjson);

base_path <- "~/robosemiotics_data/data_cropped";

#
# Adds box images to the plot
#
addBoxImages <- function(trap_json, images_dict, box_size)
{
  for(box in trap_json$visual_cue_boxes)
  {
    if (grepl("wall", box$cue_type) == FALSE)
    {
      box_x = box$x - trap_json$mean_pos_x
      box_y = box$y
      extent_x_min = box_x - box_size
      extent_x_max = box_x + box_size
      extent_y_min = box_y - box_size
      extent_y_max = box_y + box_size

      rasterImage(images_dict$get(box$cue_type), extent_x_min, extent_y_min, extent_x_max, extent_y_max);
    }
  }
}

#
# Adds track edges to the plot
#
addTrackEdges <- function(width, x_low, x_high)
{
  left_xs = c(x_low, x_high)
  left_ys = c(width/2, width/2)
  right_xs = c(x_low, x_high)
  right_ys = c(-width/2, -width/2)
  
  lines(left_xs, left_ys, type="l", col=color, lwd=7);
  lines(right_xs, right_ys, type="l", col=color, lwd=7);
}

#
# Retrieves gate data
#
getGateData <- function(trap_json, track_width, track_width_total)
{
  # Initialize the dictionary
  gate_data <- Dict$new();
  
  gate_data$set("start_x", 0)
  gate_data$set("start_l_y", 0)
  gate_data$set("start_r_y", 0)
  
  gate_data$set("end_x", 0)
  gate_data$set("end_l_y", 0)
  gate_data$set("end_r_y", 0)
  
  if (grepl("continuous", trap_json$trap_type) == TRUE)
  {
    gate_data$set("start_x", -5)
    gate_data$set("start_l_y", 4.95)
    gate_data$set("start_r_y", -4.95)
    
    gate_data$set("end_x", 6)
    gate_data$set("end_l_y", 4.95)
    gate_data$set("end_r_y", -4.95)
  }
  
  else
  {
    for(box in trap_json$visual_cue_boxes)
    {
      if (grepl("wall", box$cue_type) != TRUE)
      {
        next
      }
      
      gate_x_pos <- box$x - trap_json$mean_pos_x
      
      if (box$y>0 && gate_x_pos<0)
      {
        gate_data$set("start_x", gate_x_pos)
        gate_data$set("start_l_y", box$y)
      }
      else
      if (box$y<0 && gate_x_pos<0)
      {
        gate_data$set("start_r_y", box$y)
      }
      else
      if (box$y>0 && gate_x_pos>0)
      {
        gate_data$set("end_x", gate_x_pos)
        gate_data$set("end_l_y", box$y)
      }
      else
      if (box$y<0 && gate_x_pos>0)
      {
        gate_data$set("end_r_y", box$y)
      }
    }
    
    # If the end gate was not included, then add the entries "manually"
    if (gate_data$get("end_x") == 0)
    {
      gate_data$set("end_x", 7)
      gate_data$set("end_l_y", 4.95)
      gate_data$set("end_r_y", -4.95)
    }
  }
  
  return(gate_data)
}

#
# Adds entry and exit gates to the trap plot
#
addTrapGates <- function(gate_data, track_width, track_width_total)
{
  start_x = gate_data$get("start_x")
  start_y_l_out = track_width/2
  start_y_l_in = 2*gate_data$get("start_l_y") - track_width_total/2
  start_y_r_out = -track_width/2
  start_y_r_in = 2*gate_data$get("start_r_y") + track_width_total/2
  
  end_x = gate_data$get("end_x")
  end_y_l_out = track_width/2
  end_y_l_in = 2*gate_data$get("end_l_y") - track_width_total/2
  end_y_r_out = -track_width/2
  end_y_r_in = 2*gate_data$get("end_r_y") + track_width_total/2
  
  start_l_xs = c(start_x, start_x)
  start_l_ys = c(start_y_l_out, start_y_l_in)
  start_r_xs = c(start_x, start_x)
  start_r_ys = c(start_y_r_out, start_y_r_in)
  
  end_l_xs = c(end_x, end_x)
  end_l_ys = c(end_y_l_out, end_y_l_in)
  end_r_xs = c(end_x, end_x)
  end_r_ys = c(end_y_r_out, end_y_r_in)
  
  lines(start_l_xs, start_l_ys, type="l", col=color, lwd=9);
  lines(start_r_xs, start_r_ys, type="l", col=color, lwd=9);
  lines(end_l_xs, end_l_ys, type="l", col=color, lwd=9);
  lines(end_r_xs, end_r_ys, type="l", col=color, lwd=9);
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#
# Create images dictionary
#
box_images <- Dict$new();
box_images$set("neutral", readPNG("~/robosemiotics_data/images/neutral_box_2.png"));
box_images$set("push", readPNG("~/robosemiotics_data/images/push_box_2.png"));
box_images$set("pull", readPNG("~/robosemiotics_data/images/pull_box_2.png"));

#
# Setup the track parameters
#
color <- rgb(0,0,0, alpha=0.1);
line_wd <- 3;
track_width <- 5.35
track_width_total <- 18

#
# Get trap names
#
trap_names <- list.dirs(base_path, full.names = FALSE)

for (trap_name_no_slsh in trap_names)
{
  if (trap_name_no_slsh == "")
  {
    next
  }
  
  #
  # Read the JSON file
  #
  trap_name <- paste("/", trap_name_no_slsh, sep="");
  # trap_name <- paste("/", "trap_b_1_1", sep="");
  json_path <- paste(base_path, trap_name, trap_name, ".json", sep="");
  json_file <- fromJSON(file = json_path);
  
  #
  # Read the CSV file
  #
  cols_per_sub <- 6
  csv_path <- paste(base_path, trap_name, trap_name, ".csv", sep="");
  csv_file <- read.csv(csv_path)
  csv_nr_of_rows <- dim(csv_file)[1]
  csv_nr_of_cols <- dim(csv_file)[2]
  
  #
  # Reset the plot
  #
  if (!is.null(dev.list()))
  {
    dev.off(); 
  }
  
  #
  # Set up the plot parameters based on JSON file
  #
  gate_data <- getGateData(json_file, track_width, track_width_total)
  
  plot_y_in <- 3;
  plot_y_low <- -3;
  plot_y_high <- 3;
  plot_y_range <- plot_y_high - plot_y_low;
  
  plot_x_low <- gate_data$get("start_x")
  plot_x_high <- gate_data$get("end_x")
  plot_x_range = plot_x_high - plot_x_low
  
  pt_to_in <- plot_y_in/plot_y_range;
  plot_x_in <- plot_x_range*pt_to_in;
  
  #
  # Initialize the plot
  #
  par(pin=c(plot_x_in, plot_y_in));
  plot(NULL, 
       xlim=c(plot_x_low, plot_x_high),
       ylim=c(plot_y_low,plot_y_high),
       ylab="y (m)",
       xlab="x (m)",
       frame.plot = FALSE,
       axes = FALSE);
  
  axis(1, at=seq(plot_x_low, plot_x_high, 1));
  axis(2, at=seq(plot_y_low, plot_y_high, 1), cex.axis=1);
  
  #
  # Fill the graph with data
  #
  for(idx in 0:(csv_nr_of_cols/cols_per_sub - 1))
  {
    data_x_elem <- csv_file[idx*6 + 1]$x
    data_y_elem <- csv_file[idx*6 + 2]$y
    lines(data_x_elem, data_y_elem, type="l", col=color, lwd=line_wd);
  }
  
  #
  # Add the box images and track edges
  #
  addBoxImages(json_file, box_images, 0.45)
  addTrackEdges(track_width, gate_data$get("start_x"), gate_data$get("end_x"))
  addTrapGates(gate_data, track_width, track_width_total)
  
  #
  # Export the plot to PDF
  #
  trap_pdf_path <- paste("~/temporary_junk/trap_pdfs", trap_name, ".pdf", sep="")
  dev.print(pdf, trap_pdf_path)
}

