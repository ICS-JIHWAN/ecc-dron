import cv2
import numpy as np

config = {
    'image_path': 'C:/jhchoi/ecc_dron/video/frame_image/snapshot_7.jpg',
    'weight_path': 'C:/jhchoi/ecc_dron/YOLO_net_parameters/yolov2-tiny.weights',
    'cfg_path': 'C:\jhchoi\ecc_dron\YOLO_net_parameters\yolov2-tiny.cfg'
}

net = cv2.dnn.readNet(config['weight_path'], config['cfg_path'])

classes = []
with open('../YOLO_net_parameters/yolo.names', 'r') as f:
    classes = [line.strip for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0, 255, size=(len(classes), 3))

img = cv2.imread(config['image_path'])

h, w, c = img.shape

blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)

outs = net.forward(output_layers)

class_ids = []
confidences = []
boxes = []

for out in outs:

    for detection in out:

        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # 검출 신뢰도
        if confidence > 0.5:
            # Object detected
           # 검출기의 경계상자 좌표는 0 ~ 1로 정규화되어있으므로 다시 전처리
            center_x = int(detection[0] * w)
            center_y = int(detection[1] * h)
            dw = int(detection[2] * w)
            dh = int(detection[3] * h)
            # Rectangle coordinate
            x = int(center_x - dw / 2)
            y = int(center_y - dh / 2)
            boxes.append([x, y, dw, dh])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

