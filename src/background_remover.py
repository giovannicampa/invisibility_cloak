import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import cv2


analyse_selected_area = False


# -----------------------------------------------------------------------------------------
# Functions

x_coords = []
y_coords = []

def area_selection_callback(clk, rls):

    global x_coords
    global y_coords

    x_coords.append(int(clk.xdata))
    y_coords.append(int(clk.ydata))

    x_coords.append(int(rls.xdata))
    y_coords.append(int(rls.ydata))


def onkeypress(event):
    if event.key == 'escape':
        plt.close()


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


# -----------------------------------------------------------------------------------------
# Image capture

cap = cv2.VideoCapture(0) # Get webcam stream

# Webcam stream. Interrupts when pressing esc
while True:
    _, frame = cap.read()

    cv2.imshow("frame", frame)

    k = cv2.waitKey(5) &0xFF
    if k == 27: break

cv2.destroyAllWindows()
cap.release()

# Last picture of the webcam stream is shown in a separate window to select the area of interest
image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots(1)
plt.imshow(image)
ax.set_axis_off()

toggle_selector.RS = RectangleSelector(
            ax, area_selection_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True
        )

bbox = plt.connect('key_press_event', toggle_selector)
key = plt.connect('key_press_event', onkeypress)
print(key)
plt.connect("button_press_event", area_selection_callback)
plt.show()

print("y {}, x {}".format(y_coords, x_coords))

area_of_interest = image[y_coords[0]:y_coords[1], x_coords[0]: x_coords[1],:]


# Plotting the selected are and the distribution of the HSV values
if analyse_selected_area:
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(area_of_interest)
    ax[0].set_title("Selected area")
    ax[0].set_axis_off()

    ax[1].hist(area_of_interest[:,:,0].ravel(), label = "Hue", color = 'tab:red', alpha = 0.5, bins = 15)
    ax[1].hist(area_of_interest[:,:,1].ravel(), label = "Saturation", color = 'tab:green', alpha = 0.5, bins = 15)
    ax[1].hist(area_of_interest[:,:,2].ravel(), label = "Value", color = 'tab:blue', alpha = 0.5, bins = 15)
    ax[1].set_title("HSV distribution")

    plt.legend()
    plt.show()
    print("done")


# -----------------------------------------------------------------------------------------
# Color range selection
# Plot the image at the selection time

area_of_interes_hsv = cv2.cvtColor(area_of_interest, cv2.COLOR_RGB2HSV)
image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

def range_limits(input_value, n_sigmas = 1):
    """Returns the HSV range that we want to remove from the image
    """
    std = np.std(input_value)
    mean = np.mean(input_value)

    value_lower = mean - std*n_sigmas
    value_upper = mean + std*n_sigmas

    return value_lower, value_upper


hue_lower, hue_upper = range_limits(area_of_interes_hsv[:,:,0], n_sigmas = 3)
value_lower, value_upper = range_limits(area_of_interes_hsv[:,:,1], n_sigmas = 3)
saturation_lower, saturation_upper = range_limits(area_of_interes_hsv[:,:,2], n_sigmas = 3)


lower_bound = np.array([hue_lower, value_lower, saturation_lower])
upper_bound = np.array([hue_upper, value_upper, saturation_upper])

# Webcam stream. Interrupts when pressing esc
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_color = cv2.inRange(frame_hsv, lower_bound, upper_bound)

    image_filtered = cv2.bitwise_not(frame, frame, mask = mask_color)
    image_filtered = cv2.cvtColor(image_filtered, cv2.COLOR_HSV2RGB)

    cv2.imshow("Image filtered", image_filtered)
    cv2.imshow("Image original", frame)
    k = cv2.waitKey(5) &0xFF
    if k == 27: break


cv2.destroyAllWindows()
cap.release()