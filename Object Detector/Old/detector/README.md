# Obect Detection Block #

Object detection blocks take image as input and return normalized shape invariant coordiantes.

```
image.shape => (640, 480, 3)
image -> detector.execute -> detections
detections => List[(class_label, confidence, (cx, cy, w, h))]
(cx, cy, w, h) => (cx, cy is bbox center, w and h is bbox height and width)
range(cx or cy or w or h) => [0, 1.0]
```
