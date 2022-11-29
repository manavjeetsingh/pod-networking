from typing import Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np

from entities.entities import BlockOut, DataIn, DataOut
from utils import from_b64_to_nparr, from_np_to_b64


class BaseDetector(ABC):
	def __init__(self) -> None:
		super().__init__()

	@abstractmethod
	def execute(self, inp: 'DetectIn') -> 'DetectOut':
		raise NotImplementedError()

@dataclass
class DetectIn:
	image: np.ndarray
	# detections: Dict


	@staticmethod
	def from_data(data: DataIn):
		# image = from_b64_to_nparr(data.image)
		# image = data['image']
		# detections = data["kv"]["detections"]
		# return DetectIn(image, detections)
		image = data["image"]
		return DetectIn(image)

@dataclass
class DetectOut(BlockOut):
	detections: Dict
	image: np.ndarray = None

	@staticmethod
	def to_data(detect_out):
		image = None
		if detect_out.image:
			#image = from_np_to_b64(detect_out.image)
                        image = detect_out.image
		# convert float to str
		tfmed_detections = []
		for detection in detect_out.detections:
			class_label, conf, bbox = detection
			conf = str(conf)
			bbox = list(map(int, bbox))
			tfmed_detections.append([class_label, conf, bbox])
		return DataOut(image=image, kv={'detections' : tfmed_detections})


# TODO: Get the default detector to select from here
# A better idea might be to have the defaults in a config file
# DefaultDetector = DarknetDetector
