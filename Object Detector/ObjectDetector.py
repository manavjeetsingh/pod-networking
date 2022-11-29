
import jetson_inference
import jetson_utils
import cv2
import sys
import time
import os
import logging




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

# class TRTDetector():
# 	def __init__(self) -> None:
# 		super().__init__()
# 		self.cuda_ctx = cuda.Device(0).make_context()
# 		self.trt_yolo = TrtYOLO("yolov4-tiny-288", cuda_ctx=self.cuda_ctx)
# 		logger.info('Initialized TensorRT - yolov4-tiny-288')

# 	def execute(self, image):
# 		logger.info(f'Starting TensorRT Yolo Detection...')
# 		start_time = time.time()
        
# 		self.cuda_ctx.push()
# 		boxes, confs, classes = self.trt_yolo.detect(image, 0.25)
# 		self.cuda_ctx.pop()

# 		logger.info(f'Finished TensorRT Yolo Detection in {time.time() - start_time}')
# 		labels = list(map(lambda idx: COCO_CLASSES_LIST[int(idx)], classes))
# 		# logger.debug(f'Classes to labels {classes[0]} -> {labels[0]}')
# 		detections = list(zip(labels, confs, boxes))
# 		# logger.debug(f'Detections {detections}')
        
# 		logger.debug(f'Normalizing detections...')
# 		normed_detections = []
# 		for label, conf, bbox in detections:
# 			# convert to xywh from x1y1x2y2
# 			# normalize
# 			bbox = normalize(convert2xywh(bbox), detect_in.image)
# 			normed_detections.append((label, conf, bbox))
# 		# logger.debug(f'Displaying first detection {normed_detections[0]}')
# 		return normed_detections

class MBNDetector():
    def __init__(self, mbversion="ssd-mobilenet-v2", threshold=0.5):
        self.threshold = threshold
        self.mbversion = mbversion
        self.net = jetson_inference.detectNet(self.mbversion ,threshold = self.threshold)
        self.correct_ratio1=0
        self.correct_ratio2=0
        self.correct_ratio3=0
        self.total_images=0
        #print("Time taken to setup the object detection pipeline is :", en$

    def blocktest(self):
        images = os.listdir("Frames/")
        s_time = time.time()
        # print(images)

        for img_path in images:
            img = cv2.imread("Frames/"+img_path )
            height,width,_ = img.shape
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image1 = cv2.resize(image,(50,50))
            image2 = cv2.resize(image,(100,100))
            image3 = cv2.resize(image,(150,150))
            image4 = cv2.resize(image,(200,200))
            # print("Processing the Image is done: ")
            detection1 = self.execute(image = image1)
            # print("--------------------------------")
            # print(len(detection))
            detection2 = self.execute(image = image2)
            # print("--------------------------------")
            # print(len(detection))
            detection3 = self.execute(image = image3)
            # print("--------------------------------")
            # print(len(detection))
            detection4 = self.execute(image = image4)
            # print("--------------------------------")
            # print(len(detection))
            # print("Detection is Done")

            if (len(detection1)>=len(detection4)):
                self.correct_ratio1+=1

            if (len(detection2)>=len(detection4)):
                self.correct_ratio2+=1

            if (len(detection3)>=len(detection4)):
                self.correct_ratio3+=1

            self.total_images+=1
            print(self.total_images)
        e_time = time.time()
        print("Time taken to do the detection on these images : ", (e_time - s_time) / len(images))

    def execute(self, image):
        logging.info(f'Starting TensorRT Yolo Detection...')
        start_time = time.time()
        #print(sys.argv[1])
        imgCuda = jetson_utils.cudaFromNumpy(image)
        detections = self.net.Detect(imgCuda)
        end = time.time()
        img = jetson_utils.cudaToNumpy(imgCuda)
        #for attr in dir(detections[0]):
                #print(attr)
        normalized_detections = []
        factor=4
        for det in detections:
            bbox = normalize((det.Left,det.Top,det.Width,det.Height), img)
            bbox = (det.Left*factor, det.Top*factor, det.Width*factor, det.Height*factor)
            # bbox = convert2xywh(bbox)
            # print(bbox)
            # normalized_detections.append((det.ClassID, det.Confidence, bbox))
            normalized_detections.append(bbox)
        #variables = detections[0].__dict__.keys()
        #print(variables)
        # print("Time taken to detect is : ", end - start_time)

        #img = jetson.utils.cudaToNumpy(imgCuda)
        #print(sys.argv[1].split('/')[-1])
        # print('Saving output at "./vis_out.png"')
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imwrite("./mobilenet.png", img)
        
        #print(detections)
        return normalized_detections
    


def main():
    d=MBNDetector()
    d.blocktest()
    print("Accuracy 50*50:", d.correct_ratio1/d.total_images)
    print("Accuracy 100*100:", d.correct_ratio2/d.total_images)
    print("Accuracy 150*150:", d.correct_ratio3/d.total_images)

if __name__=='__main__':
    main()