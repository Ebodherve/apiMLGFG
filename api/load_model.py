import cv2
import os
import numpy as np

path_file = os.getcwd()+"/api/"


class ModelYolov:
    
    def __init__(self, pF = path_file):
        net = cv2.dnn.readNetFromDarknet(pF+'yolov4.cfg', pF+'yolov4.weights')
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

        DECO = 0.5
        TRH = 0.4
        
        with open(pF+'coco.names', 'r') as f:
            LABELS = f.read().splitlines()
        
        self.net = net
        self.ln = ln
        self.DECO = DECO
        self.TRH = TRH
        self.LABELS = LABELS
    
    def detection(self, path_fileD):
        img = cv2.imread(path_fileD)
        height, width, _ = img.shape
        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=True)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)
        
        boxes = []
        confidences = []
        classIDs = []
        boxes = []
        labsI = []
        
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
        
                if confidence > self.DECO:
                    box = detection[0:4]*np.array([width, height, width, height])
                    (centerX, centerY, W, H) = box.astype('int')

                    x = int(centerX - (W/2))
                    y = int(centerY - (H/2))
                    
                    boxes.append([x, y, int(W), int(H)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
                    labsI.append(self.LABELS[classID])
        
        return list(set(labsI))

