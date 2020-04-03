# https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/

import cv2
import glob
import numpy as np
import algo


# global variable to keep track of
# show = True


class Controller(object):
    def __init__(self, paths):
        self.paths = paths
        self.image_index = 0
        self._show = True
        self.current_image = cv2.imread(self.get_current_path())

    def get_current_path(self):
        return self.paths[self.image_index]

    def set_paths(self, paths):
        self.paths = paths

    def change_image(self, i):
        self.image_index += i
        self.image_index = self.image_index % len(self.paths)
        self.current_image = cv2.imread(self.get_current_path())
        self._show = True

    def get_current_image(self):
        return self.current_image.copy()

    def on_change(self, x):
        self._show = True

    def is_showing(self):
        if self._show is True:
            self._show = False
            return True

        else:
            return False


def _get_contour_area_in_tuple(item):
    return cv2.contourArea(item[1])


def show_trackers(controller, params, num_ranges=3):
    orig_window_name = 'P-> Previous, N-> Next'

    # creating windows to display images
    cv2.namedWindow(orig_window_name, cv2.WINDOW_NORMAL)  # Make the image resizable
    # cv2.namedWindow('Select', cv2.WINDOW_AUTOSIZE) # Fix the image size

    # creating trackbars to get values
    cv2.createTrackbar(f'Alpha', orig_window_name, 70, 100, controller.on_change)
    cv2.createTrackbar(f'blur_size', orig_window_name, 5, 50, controller.on_change)

    for color_num in range(1, num_ranges):
        val = 255 * color_num // num_ranges
        cv2.createTrackbar(f'Color {color_num}', orig_window_name, val, 255, controller.on_change)

    for color_num in range(num_ranges):
        cv2.createTrackbar(f'Contour {color_num}', orig_window_name, 3, 10, controller.on_change)

    # Show all images
    while (1):

        if controller.is_showing():
            # If there is any event on the trackbar
            params["blur_size"] = cv2.getTrackbarPos(f'blur_size', orig_window_name)

            vals = [0]
            params["number_contours"] = [cv2.getTrackbarPos(f'Contour {0}', orig_window_name)]
            for color_num in range(num_ranges - 1):
                color_num += 1
                vals.append(cv2.getTrackbarPos(f'Color {color_num}', orig_window_name))
                params["number_contours"].append(cv2.getTrackbarPos(f'Contour {color_num}', orig_window_name))
            vals.append(255)
            params["vals"] = vals

            image_path = controller.get_current_path()
            all_contours = algo.get_region_image_from_image(image_path, **params)
            original = cv2.imread(image_path)

            contours_image = np.zeros(original.shape[:2], dtype=np.uint8)
            sorted_contours = sorted(all_contours, key=_get_contour_area_in_tuple, reverse=True)
            for color, contour in sorted_contours:
                cv2.fillPoly(contours_image, pts=[contour], color=(color, color, color))

            # apply the overlay
            a = cv2.getTrackbarPos(f'Alpha', orig_window_name)
            alpha = a / 100
            output = cv2.addWeighted(cv2.cvtColor(contours_image, cv2.COLOR_GRAY2RGB), alpha, controller.get_current_image(), 1 - alpha, 0)

        cv2.imshow(orig_window_name, output)  # Show the results
        k = cv2.waitKey(1) & 0xFF
        # check next image in folder
        if k == ord('n'):
            controller.change_image(1)
        # check previous image in folder
        elif k == ord('p'):
            controller.change_image(-1)
        # Close all windows when 'esc' key is pressed
        elif k == 27:
            break

    cv2.destroyAllWindows()


def main():
    # Get the filename from the command line
    files = glob.glob('../../data/raw/*.jpeg')
    files.sort()
    controller = Controller(files)

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

    show_trackers(controller, params)


if __name__ == '__main__':
    main()
