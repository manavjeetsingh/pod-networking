import cv2
import integrations.darknet.darknet as darknet

def resize(image, network):
	width = darknet.network_width(network)
	height = darknet.network_height(network)
	image_resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
	return image_resized

def rescale_and_normalize(detections, network):
	# im_h, im_w, _ = image.shape
	width = darknet.network_width(network)
	height = darknet.network_height(network)
	# ratio_h = im_h / height
	# ratio_w = im_w / width
	normalized_detections = []
	for label, conf, bbox in detections:
		# x, y of center; w is width and h is height
		x, y, w, h = bbox
		x_normed, y_normed, w_normed, h_normed = x/width, y/height, w/width, h/height
		normalized_detections.append([label, conf, (x_normed, y_normed, w_normed, \
			h_normed)])
	return normalized_detections
