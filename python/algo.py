import sys

import cv2

colors_types = {
    0: "Low",
    1: "Medium",
    2: "High"
}


def _get_contour_area_in_tuple(item):
    return cv2.contourArea(item[1])


def get_region_image_from_image(
        current_image,
        vals=(0, 85, 170, 255),
        channel_num=0,
        color_space=cv2.COLOR_BGR2LAB,
        blur_size=21,
        num_contours=8):
    # Load the image from the given path
    # current_image = cv2.imread(image_path)

    # Convert the BGR image to the given color spaces and extract the selected channel
    channel_image = cv2.cvtColor(current_image, color_space)[:, :, channel_num]

    # Blur the image to make the ranges smoother
    smoothed_image = cv2.GaussianBlur(channel_image, ksize=(blur_size * 2 + 1, blur_size * 2 + 1), sigmaX=0)

    # Find contours on the smoothed image
    all_contours = []
    for color_num in range(len(vals) - 1):
        layer_color_type = colors_types[color_num]

        channel_min_value = vals[color_num]
        channel_max_value = vals[color_num + 1]

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
        image_mask = cv2.inRange(smoothed_image, channel_min_value, channel_max_value)

        # # find contours in thresholded image, then keep only the largest
        cnts = cv2.findContours(image_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts[0]) > 0:
            layer_contours = sorted(cnts[0], key=cv2.contourArea, reverse=True)
            layer_contours = layer_contours[:num_contours]
            for cnt in layer_contours:
                # all_contours.append((layer_color_hexa, cnt))

                hull = cv2.convexHull(cnt)
                all_contours.append((layer_color_type, hull))

                # epsilon = 0.001 * cv2.arcLength(cnt, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)
                # all_contours.append((layer_color_hexa, approx))

    sorted_contours = sorted(all_contours, key=_get_contour_area_in_tuple, reverse=True)
    sorted_contours = sorted_contours[:num_contours]

    # Convert to list for easier sending via requests
    contours_to_return = []
    for (color, hull) in sorted_contours:
        contours_to_return.append([color, hull.tolist()])

    # print(contours_to_return)
    return contours_to_return


if __name__ == "__main__":
    get_region_image_from_image(sys.argv[1])
