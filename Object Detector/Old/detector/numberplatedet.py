
import logging

import jetson.inference
import jetson.utils

import argparse
import sys
import cv2
import time
import os

from . import BaseDetector
from . import DetectIn, DetectOut
from entities import BlockIn, BlockOut

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def normalize(bbox, image):
        im_h, im_w, _ = image.shape
        x, y, w, h = bbox
        return x/im_w, y/im_h, w/im_w, h/im_h

# parse the command line
#parser = argparse.ArgumentParser(description="Locate objects in a $
#                                 formatter_class=argparse.RawTextH$
#                                 jetson.utils.videoSource.Usage() $

#parser.add_argument("input_URI", type=str, default="", nargs='?', $
#parser.add_argument("output_URI", type=str, default="", nargs='?',$
#parser.add_argument("--network", type=str, default="ssd-mobilenet-$
#parser.add_argument("--overlay", type=str, default="box,labels,con$
#parser.add_argument("--threshold", type=float, default=0.5, help="$
#parser.add_argument("--image", type=str, help="image path")
#is_headless = ["--headless"] if sys.argv[0].find('console.py') != $

#try:
#        opt = parser.parse_known_args()[0]
#except:
#        print("")
#        parser.print_help()
#        sys.exit(0)

#print(sys.argv)
# load the object detection network
class NPDetector(BaseDetector):
	def __init__(self, mbversion="ssd-mobilenet-v2",threshold=0.5):
		self.argv = [ '--model=./integrations/az_plate/az_plate_ssdmobilenetv1.onnx', '--class_labels=./networks/az_plate/labels.txt', '--input_blob=input_0', '--input-codec=h264', '--output_cvg=scores', '--output_bbox=boxes', '--width=640', '--height=480', '--image=Numbertest.png']
		self.net = jetson.inference.detectNet(mbversion, self.argv,threshold)

		# creat  video sources & outputs
		#input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
		#output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+i$

		# process frames until the user exits
		#while True:
		# capture the next image

	def blocktest(self):
		images = os.listdir("Images/Carparking/")
		s_time = time.time()
		for img_path in images:
			img = cv2.imread("Images/Carparking/"+img_path )
			height,width,_ = img.shape
			image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			print("Processing the Image is done: ")
			detection = self.execute(DetectIn(image = image),save = False)
			print("Detection is Done")
		e_time = time.time()
		print("Time taken to do detection on these images : ", (e_time - s_time)/len(images))

	def execute(self, detect_in: DetectIn, save = True):
		logger.info(f'Starting TensorRT Number plate detection...')
		#img = cv2.imread(opt.image)
		#image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		start_time = time.time()

		imgCuda = jetson.utils.cudaFromNumpy(detect_in.image)
		# detect objects in the image (with overlay)
		detections = self.net.Detect(imgCuda, overlay="box,labels,conf")

		# print the detections
		print("detected {:d} objects in image".format(len(detections)))
		normalized_detections = []
		for det in detections:
                        bbox = normalize((det.Left,det.Top,det.Width,det.Height), detect_in.image)
                        #bbox = convert2xywh(bbox)
                        normalized_detections.append((det.ClassID, det.Confidence, bbox))
		
        	# render the image
		img = jetson.utils.cudaToNumpy(imgCuda)
		image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		if save:
			cv2.imwrite("./Numberplate_Detection.png",image)

		# update the title bar
		#output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, $

		# print out performance info
		#net.PrintProfilerTimes()

		# exit on input/output EOS
		#if not input.IsStreaming() or not output.IsStreaming():
		#break
		return DetectOut(detections=normalized_detections)


BLOCK = NPDetector
BLOCK_IN: BlockIn = DetectIn
BLOCK_OUT: BlockOut = DetectOut

