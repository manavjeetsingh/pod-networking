import os
import logging

from blocks.detector import utils
from entities import BlockIn, BlockOut
import integrations.darknet.darknet as darknet
from . import BaseDetector, DetectIn, DetectOut


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DARKNET_PATH = "./integrations/darknet/"

network, class_names, colors = darknet.load_network(
	os.path.join(DARKNET_PATH, "cfg/yolov4-tiny.cfg"),
	os.path.join(DARKNET_PATH, "cfg/coco.data"),
	os.path.join(DARKNET_PATH, "weights/yolov4-tiny.weights"),
	batch_size=1
)

def obj_detect_block(image, network, class_names, thresh=0.25):	
	height, width, _ = image.shape
	darknet_image = darknet.make_image(width, height, 3)
	darknet.copy_image_from_bytes(darknet_image, image.tobytes())
	detections = darknet.detect_image(network, class_names, darknet_image, 
	thresh=thresh)
	darknet.free_image(darknet_image)
	return detections

class DarknetDetector(BaseDetector):
	def execute(self, detect_in: DetectIn):
		# detect_in = DetectIn.from_data(data_in)
		resized_image = utils.resize(detect_in.image, network)
		# if i == 0:
		logger.debug(f'Starting darknet object detection...')
		detections = obj_detect_block(resized_image, network, class_names)	
		# print('detections', detections)
		logger.debug(f'Detections are {detections}')
		vis_img = darknet.draw_boxes(detections, resized_image, colors)
		logger.debug(f'Normalizing the detections...')
		normed_detections = utils.rescale_and_normalize(detections, network)
		detect_out = DetectOut(detections=normed_detections, image=vis_img[...,::-1])
		return detect_out


BLOCK = DarknetDetector
BLOCK_IN: BlockIn = DetectIn
BLOCK_OUT: BlockOut = DetectOut
