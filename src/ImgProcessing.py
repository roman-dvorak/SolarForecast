#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import numpy
import ConfigParser
import pygtk
import gtk
import cv2
import cv
import numpy as np
import scipy
import Image
import matplotlib.pyplot as plt
import threading
import time
import random

print "ARTAO AOGDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"



		
def array_from_source(source):
	if isinstance( source, int ):
		cam = cv2.VideoCapture(int(source))
		s, img = cam.read()
		return numpy.asarray(img)

	elif isinstance( source, str ):
		img = cv2.LoadImage(filename, iscolor=CV_LOAD_IMAGE_COLOR)
		return numpy.asarray( img )

	else:
		print "ERROR: source is not string or int"
		return -1
