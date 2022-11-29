
import logging

import jetson.inference
import jetson.utils
import os

import argparse
import sys
import cv2
import time

from . import BaseDetector
from . import DetectIn, DetectOut
from entities import BlockIn, BlockOut

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def normalize(bbox, image):
        im_h, im_w, _ = image.shape
        x, y, w, h = bbox
        return x/im_w, y/im_h, w/im_w, h/im_h

class OCRDetector():
	def __init__(self, network = "ssd-mobilenet-v2", threshold = 0.5):
		self.argv = [ '--model=./networks/az_ocr/az_ocr_ssdmobilenetv1_2.onnx', '--class_labels=./networks/az_ocr/labels.txt', '--input_blob=input_0', '--input-codec=h264', '--output_cvg=scores', '--output_bbox=boxes', '--width=640', '--height=480', '--image=Numbertest.png']
		self.net = jetson.inference.detectNet(network, self.argv, threshold)

	def blocktest(self):
		images = os.listdir("Images/Numberplates/")
		s_time = time.time()
		for img_path in images:
                	img = cv2.imread("Images/Numberplates/Cropped_NumberCarLongPlate980.jpg" )
                	height,width,_ = img.shape
                	image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                	print("Processing the Image is done: ")
                	detection = self.execute(DetectIn(image = image))
                	print("Detection is Done")
		e_time = time.time()
		print("Time taken to do the detection on these images : ", (e_time - s_time)/len(images))

	def execute(self, detect_in: DetectIn):
		logger.info(f'Starting TensorRT Number plate detection...')
		start_time = time.time()

		imgCuda = jetson.utils.cudaFromNumpy(detect_in.image)
		detections = self.net.Detect(imgCuda, overlay="box,labels,conf")

		print("detected {:d} objects in image".format(len(detections)))
		normalized_detections = []
		for det in detections:
			bbox = normalize((det.Left,det.Top,det.Width,det.Height), detect_in.image)
			normalized_detections.append((det.ClassID, det.Confidence, bbox))

		img = jetson.utils.cudaToNumpy(imgCuda)
		image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

		cv2.imwrite("./OCR_Detection.png",image)

		return DetectOut(detections=normalized_detections)

BLOCK = OCRDetector
BLOCK_IN: BlockIn = DetectIn
BLOCK_OUT: BlockOut = DetectOut
