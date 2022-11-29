import utils
from . import Counter, CounterIn, CounterOut
from shapely.geometry import Point, LineString


class LineCrossingCounter(Counter):
    def __init__(self, lines_per_stream = None) -> None:
        super().__init__()
        self.default_lines = [(0.2, 0.95, 0.8, 0.95, 0.05), (0.95, 0.2, 0.95, 0.8, 0.05)]
        self.lines_per_stream = {}
        if lines_per_stream:
            self.lines_per_stream = lines_per_stream  # lines should be normalized (0->1)

    def count(self, detections, stream_id):
        if stream_id not in self.lines_per_stream:
            lines = self.default_lines
        def to_line_string(line):
            # leeway is how far can the object center be from the line
            # to successfully count it
            if len(line) == 5:
                x1, y1, x2, y2, leeway = line
            else:
                x1, y1, x2, y2 = line
                leeway = 0.05  # 5% of normalized image size
            line = LineString([(x1, y1), (x2, y2)])
            return line, leeway
        lines = list(map(to_line_string, lines))

        self.counts_last_frame[stream_id] = {}
        for det in detections:
            cls, conf, bbox = det
            cx, cy, w, h = bbox
            # treats objects as points represented by their bbox centers
            # see how far is the object center from the line
            point = Point(cx, cy)
            for line_crossing in lines:
                line, leeway = line_crossing
                dist = point.distance(line)
                # check if the distance between object center and line
                # is less than leeway
                # TODO (omkar): CHECK is over counting prevented? 
                # (this is resolved by point_line_sub..) 
                # counts point both when above or below line
                value = utils.point_line_substitution((point.x, point.y), \
                    list(line.coords))
                if dist <= leeway and value:
                    if cls not in self.total_counts[stream_id]:
                        self.total_counts[stream_id][cls] = 0
                    # increment counter
                    self.total_counts[stream_id][cls] += 1
                    # last frame counts
                    if cls not in self.counts_last_frame[stream_id]:
                        self.counts_last_frame[stream_id][cls] = 0
                    self.counts_last_frame[stream_id][cls] += 0
                    # break to avoid over counting across lines
                    break

    def execute(self, counter_in):
        # clear last frame for stream_id
        self.count(counter_in.detections, counter_in.stream_id)
        counter_out = CounterOut(self.total_counts, self.counts_last_frame)
        return counter_out


BLOCK = LineCrossingCounter
BLOCK_IN = CounterIn
BLOCK_OUT = CounterOut
