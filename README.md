# Invisibility cloak
This script shows a webcam stream in which all the pixels matching a user defined color are substituted with a reference image.
At first the user selects an image that will be used as a reference background. Then, from a second picture, an area containing the color range to be removed can be selected.

## Processing steps

### 1. Image selection

Select an image that will be used as a reference background can be selected by interrupting the webcam stream with the key **esc**.

<p align="left">
  <img src="https://github.com/giovannicampa/invisibility_cloak/blob/master/images/background.png" width="480">
</p>


### 2. Color selection
A second frame captured with the **esc** key is then used to select the area that contains the color that the user wants to be removed.
This is done with a rectangle selection on the frane as shown below. For the selected area the median values for each of the hue, saturation and value ranges are calculated.
A range around the median values is created by adding and subtracting n times the standard deviation of the value distibution.

By setting the *analyse_selected_area* flag to true, a plot showing the distribution of the hue, saturation, value distributions of the selected area is generated. Here the HSV ranges that will be substituted can be seen. They are defined as the area between the vertical lines of the same color of the distribution.

<p align="left">
  <img src="https://github.com/giovannicampa/invisibility_cloak/blob/master/images/color_to_filter.png" width="450">
  <img src="https://github.com/giovannicampa/invisibility_cloak/blob/master/images/hsv_distribution.png" width="450">
</p>

### 3. Pixel substitution
The current frame is processed by creating a 2d array of logic values, that indicates the pixels that fall in the Hue-Saturation-Value ranges defined.
Logical indexing is used to fill a blank image with the pixels of the current frame and the original image.

The image below shows a frame of the webcam stream with the removed colors. The pixels belonging to the yoga mat, whose color was selected, are substituted with corresponding ones of the original background image.

<p align="left">
  <img src="https://github.com/giovannicampa/invisibility_cloak/blob/master/images/invisible_yoga_mat.png" width="480">
</p>
