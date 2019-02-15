import matplotlib.pyplot as plt

#
# Creates a dictionary of the box images
#
def createImagesDictionary(base_path):
    images_dict = {}

    images_dict['neutral'] = plt.imread(base_path + "neutral_box.png", format="png")
    images_dict['pull'] = plt.imread(base_path + "pull_box.png", format="png")
    images_dict['push'] = plt.imread(base_path + "push_box.png", format="png")

    return images_dict

#
# Adds box images to the plot
#
def addBoxImages(trap_data, plot, images_dict, box_size):
    for box in trap_data.visual_cue_boxes:
        if "wall" not in box.cue_type:
            box_x = box.x - trap_data.mean_pos_x
            box_y = box.y
            extent_x_min = box_x - box_size
            extent_x_max = box_x + box_size
            extent_y_min = box_y - box_size
            extent_y_max = box_y + box_size

            plot.imshow(images_dict[box.cue_type], extent=[extent_x_min, extent_x_max, extent_y_min, extent_y_max]) 

#
# Adds track edges to the plot
#
def addTrackEdges(plot, distance, width):
    left = [[-distance/2, distance/2], [width/2, width/2]]
    right = [[-distance/2, distance/2], [-width/2, -width/2]]

    plot.plot(left[0], left[1], "b-")
    plot.plot(right[0], right[1], "b-")