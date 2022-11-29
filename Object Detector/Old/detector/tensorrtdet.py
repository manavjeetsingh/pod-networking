import time
import logging

import numpy as np
import pandas as pd
import pycuda.autoinit
import pycuda.driver as cuda

from entities import BlockIn, BlockOut

from . import DetectIn, DataIn
from . import BaseDetector, DetectOut
from integrations.trt.yolo_with_plugins import TrtYOLO
from integrations.trt.yolo_classes import COCO_CLASSES_LIST


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def convert2xywh(bbox):
	x1, y1, x2, y2 = bbox
	w = x2 - x1
	h = y2 - y1
	x, y = x1 + w/2, y1 + h/2
	return x, y, w, h

def normalize(bbox, image):
	im_h, im_w, _ = image.shape
	x, y, w, h = bbox
	return x/im_w, y/im_h, w/im_w, h/im_h


class TRTDetector(BaseDetector):
	def __init__(self) -> None:
		super().__init__()
		self.cuda_ctx = cuda.Device(0).make_context()
		self.trt_yolo = TrtYOLO("yolov4-tiny-288", cuda_ctx=self.cuda_ctx)
		logger.info('Initialized TensorRT - yolov4-tiny-288')

	def execute(self, detect_in: DataIn):
		logger.info(f'Starting TensorRT Yolo Detection...')
		start_time = time.time()
		
		self.cuda_ctx.push()
		boxes, confs, classes = self.trt_yolo.detect(detect_in.image, 0.25)
		self.cuda_ctx.pop()

		logger.info(f'Finished TensorRT Yolo Detection in {time.time() - start_time}')
		labels = list(map(lambda idx: COCO_CLASSES_LIST[int(idx)], classes))
		# logger.debug(f'Classes to labels {classes[0]} -> {labels[0]}')
		detections = list(zip(labels, confs, boxes))
		# logger.debug(f'Detections {detections}')
		
		logger.debug(f'Normalizing detections...')
		normed_detections = []
		for label, conf, bbox in detections:
			# convert to xywh from x1y1x2y2
			# normalize
			bbox = normalize(convert2xywh(bbox), detect_in.image)
			normed_detections.append((label, conf, bbox))
		# logger.debug(f'Displaying first detection {normed_detections[0]}')
		return DetectOut(detections=normed_detections)


BLOCK = TRTDetector
BLOCK_IN: BlockIn = DetectIn
BLOCK_OUT: BlockOut = DetectOut
