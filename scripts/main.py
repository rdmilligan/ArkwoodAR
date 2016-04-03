# Copyright (C) 2016 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/ArkwoodAR)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cv2
from PIL import Image
from webcam import Webcam
from templatematching import TemplateMatching

class ArkwoodAR:

    def __init__(self):

        # initialise webcams
        self.webcam_one = Webcam(0)
        self.webcam_two = Webcam(1)

        # initialise template matching
        self.template_matching = TemplateMatching()

        # initialise texture
        self.texture_background = None

    def _init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # start webcam threads
        self.webcam_one.start()
        self.webcam_two.start()

        # assign texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)

    def _draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # get image from webcams
        image_one = self.webcam_one.get_current_frame()
        image_two = self.webcam_two.get_current_frame()

        # create stereoscopic image
        stereo_image = np.concatenate((image_one, image_two), axis=1)

        # update image with template matching
        stereo_image = self.template_matching.update_image(stereo_image)

        # handle background
        self._handle_background(stereo_image)

        glutSwapBuffers()

    def _handle_background(self, image):

        # convert image to OpenGL texture format
        bg_image = cv2.flip(image, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes('raw', 'BGRX', 0, -1)
 
        # create background texture
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        
        # draw background
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        glPopMatrix()

    def main(self):
        # setup and run OpenGL
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 360)
        glutInitWindowPosition(100, 100)
        self.window_id = glutCreateWindow('ArkwoodAR')
        glutDisplayFunc(self._draw_scene)
        glutIdleFunc(self._draw_scene)
        self._init_gl()
        glutMainLoop()
 
# run an instance of ArkwoodAR
arkwoodAR = ArkwoodAR()
arkwoodAR.main()
