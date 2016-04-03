# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/ArkwoodAR)

import cv2
import numpy as np

class TemplateMatching:

    THRESHOLD = 0.8

    def __init__(self):
        # load template
        self.template = cv2.imread('images/skull.jpg', 0)
        self.template_width, self.template_height = self.template.shape[::-1]

    def update_image(self, image):

        # convert image to grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # apply template matching
        result = cv2.matchTemplate(image_gray, self.template, cv2.TM_CCOEFF_NORMED)

        # show matches on image, where threshold met
        locations = np.where(result >= self.THRESHOLD)

        for pt in zip(*locations[::-1]):
            cv2.rectangle(image, pt, (pt[0]+self.template_width, pt[1]+self.template_height), (0,255,0), 2)

        # return image
        return image