# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/ArkwoodAR)

import numpy as np
import cv2
from OpenGL.GL import *
from markers import Markers
from constants import *
from cubeviews import *

class MediaCube:

    # constants
    FILE_PATH = 'scripts/features/mediacube/'

    INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])

    def __init__(self):
        # initialise markers
        self.markers = Markers()

        # initialise textures
        self.marker_one_textures, self.marker_two_textures = self._load_textures()

        # initialise video
        self.video_capture = cv2.VideoCapture()

    def detect(self, image):

        markers = None

        # detect markers
        try:
            markers = self.markers.detect(image)
        except Exception as ex:
            print(ex)

        if not markers:
            return None

        return markers

    def render(self, markers):

        for marker in markers:
            
            rvecs, tvecs, marker_rotation, marker_name = marker

            # build view matrix
            rmtx = cv2.Rodrigues(rvecs)[0]

            view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0]],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1]],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2]],
                                    [0.0       ,0.0       ,0.0       ,1.0    ]])

            view_matrix = view_matrix * self.INVERSE_MATRIX

            view_matrix = np.transpose(view_matrix)

            # load view matrix and draw cube
            glPushMatrix()
            glLoadMatrixd(view_matrix)

            if marker_name == MARKER_ONE:
                self.marker_one_textures[TEXTURE_FRONT] = cv2.flip(self._get_video_frame(), 0)
                self._draw_cube(marker_rotation, self.marker_one_textures)
            elif marker_name == MARKER_TWO:
                self._draw_cube(marker_rotation, self.marker_two_textures)

            glColor3f(1.0, 1.0, 1.0)
            glPopMatrix()

    def _load_textures(self):
        marker_one_textures = {}
        marker_two_textures = {}

        # load images
        image_green = cv2.imread('{}green.png'.format(self.FILE_PATH))
        image_yellow = cv2.imread('{}yellow.png'.format(self.FILE_PATH))
        image_blue = cv2.imread('{}blue.png'.format(self.FILE_PATH))
        image_pink = cv2.imread('{}pink.png'.format(self.FILE_PATH))
        image_saltwash = np.rot90(cv2.imread('{}saltwash.jpg'.format(self.FILE_PATH)), 2)
        image_halo = np.rot90(cv2.imread('{}halo.jpg'.format(self.FILE_PATH)), 2)

        # load textures for marker one
        marker_one_textures[TEXTURE_FRONT] = None
        marker_one_textures[TEXTURE_RIGHT] = image_green
        marker_one_textures[TEXTURE_BACK] = image_yellow
        marker_one_textures[TEXTURE_LEFT] = image_blue
        marker_one_textures[TEXTURE_TOP] = image_pink

        # load textures for marker two
        marker_two_textures[TEXTURE_FRONT] = image_saltwash
        marker_two_textures[TEXTURE_RIGHT] = image_green
        marker_two_textures[TEXTURE_BACK] = image_halo
        marker_two_textures[TEXTURE_LEFT] = image_blue
        marker_two_textures[TEXTURE_TOP] = image_pink

        return (marker_one_textures, marker_two_textures)

    def _get_video_frame(self):

        # get latest frame from video
        success, frame = self.video_capture.read()
        if success: return frame

        if not self.video_capture.isOpened():
            self.video_capture.open('{}channel_one.mp4'.format(self.FILE_PATH))
        else:
            self.video_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)      

        return self.video_capture.read()[1]

    def _draw_cube(self, marker_rotation, marker_textures):

        # draw cube
        if marker_rotation == 0:
            cube_degrees_0(marker_textures)
        elif marker_rotation == 1:
            cube_degrees_90(marker_textures)
        elif marker_rotation == 2:
            cube_degrees_180(marker_textures)
        elif marker_rotation == 3:
            cube_degrees_270(marker_textures)