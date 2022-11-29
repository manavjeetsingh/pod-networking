import logging

import jetson.inference
import jetson.utils
import cv2
import sys
import time
import os
from . import BaseDetector
from . import DetectIn, DetectOut
from entities import BlockIn, BlockOut

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def convert2xywh(bbox):
        x1, y1, w, h = bbox
        x, y = x1 + w/2, y1 + h/2
        return x, y, w, h

def normalize(bbox, image):
	im_h, im_w, _ = image.shape
	x, y, w, h = bbox
	return x/im_w, y/im_h, w/im_w, h/im_h

class MBNDetector(BaseDetector):
	def __init__(self, mbversion="ssd-mobilenet-v2", threshold=0.5):
		self.threshold = threshold
		self.mbversion = mbversion
		self.net = jetson.inference.detectNet(self.mbversion ,threshold = self.threshold)
 		#print("Time taken to setup the object detection pipeline is :", en$

	def blocktest(self):
		images = os.listdir("Images/Carparking/")
		s_time = time.time()
                print(images)

		for img_path in images:
			img = cv2.imread("Images/Carparking/CarLongPlate534.jpg" )
			height,width,_ = img.shape
			image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			print("Processing the Image is done: ")
			detection = self.execute(DetectIn(image = image))
			print("Detection is Done")
		e_time = time.time()
		print("Time taken to do the detection on these images : ", (e_time - s_time) / len(images))

	def execute(self, detect_in: DetectIn):
		logger.info(f'Starting TensorRT Yolo Detection...')
		start_time = time.time()
		#print(sys.argv[1])
		imgCuda = jetson.utils.cudaFromNumpy(detect_in.image)
		detections = self.net.Detect(imgCuda)
		end = time.time()
		img = jetson.utils.cudaToNumpy(imgCuda)
		#for attr in dir(detections[0]):
     			#print(attr)
		normalized_detections = []
		for det in detections:
			#bbox = normalize((det.Left,det.Top,det.Width,det.Height), img)
                        bbox = (det.Left, det.Top, det.Width, det.Height)
			#bbox = convert2xywh(bbox)
                        normalized_detections.append((det.ClassID, det.Confidence, bbox))
		#variables = detections[0].__dict__.keys()
		#print(variables)
		print("Time taken to detect is : ", end - start_time)

		#img = jetson.utils.cudaToNumpy(imgCuda)
		#print(sys.argv[1].split('/')[-1])
		print('Saving output at "./vis_out.png"')
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		cv2.imwrite("./mobilenet.png", img)
		
		#print(detections)
		return DetectOut(detections=normalized_detections)


BLOCK = MBNDetector
BLOCK_IN: BlockIn = DetectIn
BLOCK_OUT: BlockOut = DetectOut
