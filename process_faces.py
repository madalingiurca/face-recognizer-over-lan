import os
from PIL import Image, ImageDraw
import numpy as np
import cv2

faceCascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")
base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'Faces')
train_faces = []
train_labels = []
print(images_dir)

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path))
            print(label, "@", path)
            image = Image.open(path).convert("L") # "L" pentru grayscale
            image_mat = np.array(image, "uint8")
            face = faceCascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)
            
