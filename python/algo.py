import sys

import cv2
import numpy as np


class ContourKeys:
    Contour = "Contour"
    ColorNum = "ColorNum"
    AreaFinal = "AreaFinal"
    AreaFilled = "AreaFilled"
    IsHole = "Is Hole"


class ParamsConfig:
    NumContours = 8
    ColorRanges = (0, 85, 170, 255)
    ColorSpace = cv2.COLOR_BGR2LAB
    ChannelNum = 0


def get_region_image_from_image(current_image):

    # scale = 4
    # current_image = cv2.resize(current_image, (int(current_image.shape[1]/scale), int(current_image.shape[0]/scale)))

    image_smaller_dim = min(current_image.shape[:2])
    blur_size = int(image_smaller_dim / 30) * 2 + 1
    kernel_size = int(image_smaller_dim / 600) * 2 + 1
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Convert the BGR image to the given color spaces and extract the selected channel
    channel_image = cv2.cvtColor(current_image, ParamsConfig.ColorSpace)[:, :, ParamsConfig.ChannelNum]

    # Get the contours from the channel image
    sorted_contours = get_contours_dict(channel_image, blur_size)

    # Create an image from the contours on a new image
    contours_image = get_contours_image(channel_image, sorted_contours)

    final_contours = get_final_contours(contours_image, kernel)

    return final_contours


def get_final_contours(contours_image, kernel):
    final_contours = {}
    for color_num in range(len(ParamsConfig.ColorRanges) - 1):
        channel_min_value = ParamsConfig.ColorRanges[color_num]
        channel_max_value = ParamsConfig.ColorRanges[color_num + 1]

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
        image_mask = cv2.inRange(contours_image, channel_min_value, channel_max_value)

        image_mask = cv2.dilate(image_mask, kernel=kernel, iterations=1)
        image_mask = cv2.erode(image_mask, kernel=kernel, iterations=2)

        # # find contours in thresholded image, then keep only the largest
        (contours, hierarchies) = cv2.findContours(image_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if hierarchies is not None:
            final_contours[color_num] = contours
    return final_contours


def get_contours_image(channel_image, sorted_contours):
    # Create the image from the overlapping shapes
    contours_image = np.ones_like(channel_image) * 127
    # contours_image_debug = np.zeros_like(channel_image)
    # contours_image_debug[:, :, 1] = 255
    previous_area_filled = np.product(contours_image.shape)
    contours_counter = 0
    for idx, obj in enumerate(sorted_contours):
        if contours_counter >= ParamsConfig.NumContours:
            break

        contour = obj[ContourKeys.Contour]
        color_num = obj[ContourKeys.ColorNum]
        area_filled = obj[ContourKeys.AreaFilled]

        # Skip areas where the filling is too large
        if area_filled > previous_area_filled:
            continue

        contours_counter += 1
        previous_area_filled = area_filled

        color = int(color_num * 255 / (len(ParamsConfig.ColorRanges) - 2))
        # pts = [np.array(contour)]

        hull = cv2.convexHull(contour)
        pts = [np.array(hull)]

        # cv2.floodFill(contours_image, mask, (0, 0), 255)

        cv2.fillPoly(contours_image, pts=pts, color=color)

        # cv2.fillPoly(contours_image_debug, pts=pts, color=(color, 255, 0))
        # area_final = obj[ContourKeys.AreaFinal]
        # image_title = f"{color_num}.{idx}({contours_counter}), Area={int(area_final):,}({int(area_filled):,})"
        # cv2.imshow(image_title, contours_image_debug)  # Show the results
        # k = cv2.waitKey(1) & 0xFF
        # # while True:
        # if k == ord("b"):
        #     break
        # cv2.fillPoly(contours_image_debug, pts=pts, color=(color, color, color))
    # cv2.imshow("contours_image", contours_image_debug)  # Show the results
    # k = cv2.waitKey(1) & 0xFF
    return contours_image


def get_contours_dict(channel_image, blur_size):

    # Blur the image to make the ranges smoother
    smoothed_image = cv2.GaussianBlur(channel_image, ksize=(blur_size, blur_size), sigmaX=0)

    # Find contours on the smoothed image
    contours_list = []
    # contours_image_debug = np.zeros(current_image.shape, dtype=np.uint8)
    # contours_image_debug[:, :, 1] = 255
    for color_num in range(len(ParamsConfig.ColorRanges) - 1):
        channel_min_value = ParamsConfig.ColorRanges[color_num]
        channel_max_value = ParamsConfig.ColorRanges[color_num + 1]

        # Create the mask using the min and max values obtained from trackbar and apply bitwise and operation to get the results
        image_mask = cv2.inRange(smoothed_image, channel_min_value, channel_max_value)

        # # find contours in thresholded image, then keep only the largest
        # hierarchy=[Next, Previous, First_Child, Parent]
        contours, hierarchies = cv2.findContours(image_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cnts = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)
        # a = sorted(zip(contour_list, hierarchies), key=_get_contour_area_in_tuple, reverse=True)
        # cnts = cnts[:num_contours]

        if len(contours) > 0:
            _contours_dict = {}
            for idx, (contour, hierarchy) in enumerate(zip(contours, hierarchies[0])):
                contour_area = cv2.contourArea(contour)

                is_hole = False
                _hierarchy = hierarchy
                while _hierarchy[3] != -1:
                    is_hole = not is_hole
                    parent_idx = _hierarchy[3]
                    _hierarchy = hierarchies[0][parent_idx]

                # In case this contour is a hole, subtract its area from the parents area
                if is_hole:
                    parent_idx = hierarchy[3]
                    if parent_idx != -1:
                        _contours_dict[parent_idx][ContourKeys.AreaFinal] -= contour_area

                _contours_dict[idx] = {
                    ContourKeys.Contour: contour,
                    ContourKeys.ColorNum: color_num,
                    ContourKeys.AreaFinal: contour_area,
                    ContourKeys.AreaFilled: contour_area,
                    ContourKeys.IsHole: is_hole,
                }
                # contours_dict.append((color_num, contour))

                # hull = cv2.convexHull(cnt)
                # all_contours.append((color_num, hull))

                # epsilon = 0.001 * cv2.arcLength(cnt, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)
                # all_contours.append((color_num, approx))

                # cv2.fillPoly(contours_image_debug, pts=pts, color=(color, color, color))
            for idx, obj in _contours_dict.items():
                is_hole = obj[ContourKeys.IsHole]

                if is_hole is False:
                    contours_list.append(obj)

                    # contour = obj[ContourKeys.Contour]
                    # area_final = obj[ContourKeys.AreaFinal]
                    # area_filled = obj[ContourKeys.AreaFilled]
                    # pts = [np.array(contour)]
                    # if is_hole:
                    #     cv2.fillPoly(contours_image_debug, pts=pts, color=(0, 0, 0))
                    # else:
                    #     cv2.fillPoly(contours_image_debug, pts=pts, color=(255, 255, 255))
                    # image_title = f"{color_num}.{idx}.{is_hole}, Area={int(area_final):,}({int(area_filled):,})"
                    # cv2.imshow(image_title, contours_image_debug)  # Show the results
                    # k = cv2.waitKey(1) & 0xFF
                    # # while True:
                    # if k == ord("b"):
                    #     break
    sorted_contours = sorted(contours_list, key=lambda x: x[ContourKeys.AreaFinal], reverse=True)
    # sorted_contours = sorted_contours[:num_contours]
    return sorted_contours


if __name__ == "__main__":
    get_region_image_from_image(sys.argv[1])
