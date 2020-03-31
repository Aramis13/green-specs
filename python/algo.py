import cv2
import numpy as np


def get_region_image_from_image(image_path, vals=(0, 85, 170, 255), channel_num=0, color_space=cv2.COLOR_BGR2LAB, iterations=1, kernel_size=5):
    original = cv2.imread(image_path)

    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image_mask_colored_all = np.zeros(original.shape[:2], dtype=np.uint8)
    # Get values from the trackbar
    for color_num in range(len(vals) - 1):
        channel_min_value = vals[color_num]
        channel_max_value = vals[color_num + 1]

        # Convert the BGR image to other color spaces
        image_converted = cv2.cvtColor(original, color_space)

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results

        image_mask = cv2.inRange(image_converted[:, :, channel_num], channel_min_value, channel_max_value)
        image_mask_colored = image_mask // (len(vals) - 2) * color_num

        # image_mask_colored = cv2.dilate(image_mask_colored, kernel, iterations=iterations)
        # image_mask_colored = cv2.erode(image_mask_colored, kernel, iterations=iterations)

        image_mask_colored_all = cv2.bitwise_or(image_mask_colored_all, image_mask_colored)

    image_mask_colored_all = cv2.dilate(image_mask_colored_all, kernel, iterations=iterations)
    image_mask_colored_all = cv2.erode(image_mask_colored_all, kernel, iterations=iterations)

    return image_mask_colored_all
