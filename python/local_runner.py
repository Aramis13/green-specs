# https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/

import cv2
import glob
import numpy as np
import algo

# global variable to keep track of
show = True


def _onTrackbarActivity(x):
    global show
    show = True
    pass


def _reload(i):
    global show
    show = True
    original = cv2.imread(files[i % len(files)])
    original = cv2.resize(original, (rsize, rsize))
    return original.copy()


def main():
    assert num_ranges > 0

    global show

    orig_window_name = 'P-> Previous, N-> Next'

    # creating windows to display images
    cv2.namedWindow(orig_window_name, cv2.WINDOW_NORMAL)  # Make the image resizable
    # cv2.namedWindow('Select', cv2.WINDOW_AUTOSIZE) # Fix the image size

    # creating trackbars to get values
    cv2.createTrackbar(f'Alpha', orig_window_name, 70, 100, _onTrackbarActivity)
    cv2.createTrackbar(f'Kernel', orig_window_name, 5, 50, _onTrackbarActivity)
    cv2.createTrackbar(f'Iterations', orig_window_name, 2, 10, _onTrackbarActivity)

    for color_num in range(num_ranges - 1):
        color_num += 1
        val = 255 * color_num // num_ranges
        cv2.createTrackbar(f'Color {color_num}', orig_window_name, val, 255, _onTrackbarActivity)

    # Show all images
    i = 0
    original = _reload(i)
    while (1):

        if show:  # If there is any event on the trackbar
            show = False

            params["kernel_size"] = cv2.getTrackbarPos(f'Kernel', orig_window_name)
            params["iterations"] = cv2.getTrackbarPos(f'Iterations', orig_window_name)

            vals = [0]
            for color_num in range(num_ranges - 1):
                color_num += 1
                vals.append(cv2.getTrackbarPos(f'Color {color_num}', orig_window_name))
            vals.append(255)
            image_mask_colored_all = algo.convert_image(original, vals)

            # apply the overlay
            a = cv2.getTrackbarPos(f'Alpha', orig_window_name)
            alpha = a / 100
            output = cv2.addWeighted(cv2.cvtColor(image_mask_colored_all, cv2.COLOR_GRAY2RGB), alpha, original, 1 - alpha, 0)

        cv2.imshow(orig_window_name, output)  # Show the results
        k = cv2.waitKey(1) & 0xFF
        # check next image in folder
        if k == ord('n'):
            i += 1
            original = _reload(i)
        # check previous image in folder
        elif k == ord('p'):
            i -= 1
            original = _reload(i)
        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Get the filename from the command line
    files = glob.glob('../../data/raw/*.jpeg')
    files.sort()

    # Resize the image
    rsize = 950

    # Number of different color ranges
    num_ranges = 3

    # cv2.COLOR_BGR2LAB,
    # L – Lightness ( Intensity ).
    # a – color component ranging from Green to Magenta.
    # b – color component ranging from Blue to Yellow.
    # cv2.COLOR_BGR2YCrCb,
    # Y – Luminance or Luma component obtained from RGB after gamma correction.
    # Cr = R – Y ( how far is the red component from Luma ).
    # Cb = B – Y ( how far is the blue component from Luma ).
    # cv2.COLOR_BGR2HSV
    # H – Hue ( Dominant Wavelength ).
    # S – Saturation ( Purity / shades of the color ).
    # V – Value ( Intensity ).

    # params = (cv2.COLOR_BGR2LAB, 0)  # 0 for L in LAB
    # params = (cv2.COLOR_BGR2YCrCb, 0)  # 0 for Y in YCrCb
    params = {"channel_num": 0, "color_space": cv2.COLOR_BGR2LAB, }  # 0 for L in LAB
    params = {"channel_num": 0, "color_space": cv2.COLOR_BGR2YCrCb, }  # 0 for Y in YCrCb
    params = {"channel_num": 2, "color_space": cv2.COLOR_BGR2HSV, }  # 2 for V in HSV

    main()
