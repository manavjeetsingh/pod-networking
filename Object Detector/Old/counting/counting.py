from . import Counter, CounterIn, CounterOut


class DefaultCounter(Counter):
    def execute(self, counter_in):
        # detections = CounterIn.from_data(data)
        # clear last frame for stream_id
        self.counts_last_frame[counter_in.stream_id] = {}
        for d in counter_in.detections:
            if d[0] not in self.total_counts[counter_in.stream_id]:
                self.total_counts[counter_in.stream_id][d[0]] = 0
            self.total_counts[counter_in.stream_id][d[0]] += 1
            if d[0] not in self.counts_last_frame[counter_in.stream_id]:
                self.counts_last_frame[counter_in.stream_id][d[0]] = 0
            self.counts_last_frame[counter_in.stream_id][d[0]] += 1
        counter_out = CounterOut(self.total_counts, self.counts_last_frame)
        return counter_out


BLOCK = DefaultCounter
BLOCK_IN = CounterIn
BLOCK_OUT = CounterOut
