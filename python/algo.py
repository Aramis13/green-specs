import sys

import cv2
import numpy as np


def _get_contour_area_in_tuple(item):
    return cv2.contourArea(item[1])


def get_region_image_from_image(
        current_image,
        vals=(0, 85, 170, 255),
        channel_num=0,
        color_space=cv2.COLOR_BGR2LAB,
        blur_size=21,
        num_contours=8,
        kernel=5):

    # Convert the BGR image to the given color spaces and extract the selected channel
    channel_image = cv2.cvtColor(current_image, color_space)[:, :, channel_num]

    # Blur the image to make the ranges smoother
    smoothed_image = cv2.GaussianBlur(channel_image, ksize=(blur_size * 2 + 1, blur_size * 2 + 1), sigmaX=0)

    # Find contours on the smoothed image
    all_contours = []
    for color_num in range(len(vals) - 1):
        channel_min_value = vals[color_num]
        channel_max_value = vals[color_num + 1]

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
        image_mask = cv2.inRange(smoothed_image, channel_min_value, channel_max_value)

        # # find contours in thresholded image, then keep only the largest
        cnts, _ = cv2.findContours(image_mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            for cnt in cnts:
                hull = cv2.convexHull(cnt)
                all_contours.append((color_num, hull))

                # epsilon = 0.001 * cv2.arcLength(cnt, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)
                # all_contours.append((color_num, approx))

    sorted_contours = sorted(all_contours, key=_get_contour_area_in_tuple, reverse=True)
    # sorted_contours = sorted_contours[:num_contours]

    # Create the image from the overlapping shapes
    contours_image = np.zeros(current_image.shape[:2], dtype=np.uint8)
    for color_num, contour in sorted_contours:
        color = int(color_num * 255 / (len(vals) - 2))
        cv2.fillPoly(contours_image, pts=[np.array(contour)], color=(color, color, color))

    final_contours = {}
    for color_num in range(len(vals) - 1):
        channel_min_value = vals[color_num]
        channel_max_value = vals[color_num + 1]

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
        image_mask = cv2.inRange(contours_image, channel_min_value, channel_max_value)

        image_mask = cv2.dilate(image_mask, np.ones((kernel, kernel), np.uint8), iterations=1)
        image_mask = cv2.erode(image_mask, np.ones((kernel, kernel), np.uint8), iterations=2)

        # # find contours in thresholded image, then keep only the largest
        (cnts, hierarchies) = cv2.findContours(image_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if hierarchies is not None:
            final_contours[color_num] = cnts

    return final_contours


if __name__ == "__main__":
    get_region_image_from_image(sys.argv[1])
