import os as o
import numpy as np
import cv2 as cv


global image_map
image_map = {}


def get_image_size(image_path: str) -> int:
    image = cv.imread(image_path)
    height, width, color = image.shape
    

    return height


print(get_image_size("test-images/image-1.png"))