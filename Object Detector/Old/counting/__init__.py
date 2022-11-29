from typing import Dict
from dataclasses import dataclass
from collections import defaultdict

from blocks import Block
from entities import BlockIn, BlockOut, DataIn, DataOut


class Counter(Block):    
	def __init__(self) -> None:
		super().__init__()
		self.total_counts = defaultdict(dict)
		self.counts_last_frame = defaultdict(dict)


@dataclass
class CounterIn(BlockIn):
	detections: Dict
	stream_id: int

	@staticmethod
	def from_data(data: DataIn):
		tfmed_detections = []
		for detection in data['kv']['detections']:
			class_label, conf, bbox = detection
			conf = float(conf)
			bbox = list(map(float, bbox))
			tfmed_detections.append([class_label, conf, bbox])
		return CounterIn(detections=tfmed_detections, stream_id=data['kv']['streamID'])


@dataclass
class CounterOut(BlockOut):
	total_counts: Dict[str, object]
	counts_last_frame: Dict[str, object]

	@staticmethod
	def to_data(counter_out):
		d = {
			'count_per_stream': dict(counter_out.total_counts),
			'counts_last_frame': dict(counter_out.counts_last_frame)
		}
		return DataOut(kv=d)


from .basic import PerFrameCounter
from .linecrossing import LineCrossingCounter
