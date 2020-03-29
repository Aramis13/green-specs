# https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/

import cv2, time, argparse, glob
import numpy as np

# global variable to keep track of
show = True

color_spaces = [
    cv2.COLOR_BGR2LAB,
    # L – Lightness ( Intensity ).
    # a – color component ranging from Green to Magenta.
    # b – color component ranging from Blue to Yellow.
    cv2.COLOR_BGR2YCrCb,
    # Y – Luminance or Luma component obtained from RGB after gamma correction.
    # Cr = R – Y ( how far is the red component from Luma ).
    # Cb = B – Y ( how far is the blue component from Luma ).
    cv2.COLOR_BGR2HSV
    # H – Hue ( Dominant Wavelength ).
    # S – Saturation ( Purity / shades of the color ).
    # V – Value ( Intensity ).
]


def onTrackbarActivity(x):
    global show
    show = True
    pass


def reload():
    global show
    show = True
    original = cv2.imread(files[i % len(files)])
    original = cv2.resize(original, (rsize, rsize))
    return original.copy()


if __name__ == '__main__':
    show_orig = False
    orig_window_name = 'P-> Previous, N-> Next'
    color_space = cv2.COLOR_BGR2LAB
    channel_num = 0  # L in LAB
    num_ranges = 3

    # Resize the image
    rsize = 950

    # position on the screen where the windows start
    initialX = 50
    initialY = 100

    # Get the filename from the command line
    files = glob.glob('../data/raw/*.jpeg')
    files.sort()

    # creating windows to display images
    cv2.namedWindow(orig_window_name, cv2.WINDOW_NORMAL)  # Make the image resizable
    # cv2.namedWindow('Select', cv2.WINDOW_AUTOSIZE) # Fix the image size

    # moving the windows to stack them horizontally
    cv2.moveWindow(orig_window_name, initialX, initialY)

    # creating trackbars to get values
    cv2.createTrackbar(f'Alpha', orig_window_name, 70, 100, onTrackbarActivity)
    cv2.createTrackbar(f'Kernel', orig_window_name, 5, 50, onTrackbarActivity)
    cv2.createTrackbar(f'Iterations', orig_window_name, 2, 10, onTrackbarActivity)

    for color_num in range(num_ranges - 1):
        color_num += 1
        val = 255 * color_num // num_ranges
        cv2.createTrackbar(f'Color {color_num}', orig_window_name, val, 255, onTrackbarActivity)

    # show all images initially
    i = 0
    original = reload()
    while (1):

        if show:  # If there is any event on the trackbar
            show = False

            kernel_size = cv2.getTrackbarPos(f'Kernel', orig_window_name)
            kernel = np.ones((kernel_size, kernel_size), np.uint8)

            iterations = cv2.getTrackbarPos(f'Iterations', orig_window_name)

            image_mask_colored_all = np.zeros(original.shape[:2], dtype=np.uint8)

            # Get values from the trackbar
            for color_num in range(num_ranges):
                if color_num == 0:
                    channel_min_value = 0
                else:
                    channel_min_value = cv2.getTrackbarPos(f'Color {color_num}', orig_window_name)

                if color_num == num_ranges - 1:
                    channel_max_value = 255
                else:
                    channel_max_value = cv2.getTrackbarPos(f'Color {color_num + 1}', orig_window_name)

                # Convert the BGR image to other color spaces
                image_converted = cv2.cvtColor(original, color_space)

                # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results

                image_mask = cv2.inRange(image_converted[:, :, channel_num], channel_min_value, channel_max_value)
                image_mask_colored = image_mask // (num_ranges - 1) * color_num

                # image_mask_colored = cv2.dilate(image_mask_colored, kernel, iterations=iterations)
                # image_mask_colored = cv2.erode(image_mask_colored, kernel, iterations=iterations)

                image_mask_colored_all = cv2.bitwise_or(image_mask_colored_all, image_mask_colored)

            image_mask_colored_all = cv2.dilate(image_mask_colored_all, kernel, iterations=iterations)
            image_mask_colored_all = cv2.erode(image_mask_colored_all, kernel, iterations=iterations)

            # apply the overlay
            a = cv2.getTrackbarPos(f'Alpha', orig_window_name)
            alpha = a / 100
            output = cv2.addWeighted(cv2.cvtColor(image_mask_colored_all, cv2.COLOR_GRAY2RGB), alpha, original, 1 - alpha, 0)

        cv2.imshow(orig_window_name, output)  # Show the results
        k = cv2.waitKey(1) & 0xFF
        # check next image in folder
        if k == ord('n'):
            i += 1
            original = reload()
        # check previous image in folder
        elif k == ord('p'):
            i -= 1
            original = reload()
        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

    cv2.destroyAllWindows()
