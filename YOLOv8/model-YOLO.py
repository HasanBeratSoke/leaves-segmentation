from ultralytics import YOLO
from PIL import Image
import cv2
import torchvision
print(torchvision.__version__)

model = YOLO("./YOLOv8/best (2).pt")
"""
# from PIL
img = cv2.imread("IMG_0161.JPG")
results = model.predict(source=img, save=False)  # save plotted images
res_plotted = results[0].plot(conf = False, labels = True, masks = True, boxes = False, save = True)
#results = model.predict(source="0")
"""

img = cv2.imread("IMG_0161.JPG")
# img resize

res = model(img)
res_plotted = res[0].plot(labels = True, masks = True)
cv2.imshow("result", res_plotted)
cv2.waitKey(0)
cv2.destroyAllWindows()