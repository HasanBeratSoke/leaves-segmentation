from tkinter.tix import Tree
import cv2 as cv
import numpy as np
from random import randint  # for random values
import copy  # for deepcopy on images

IMG_PATH = r"C:\Users\hasan\Desktop\leaves-segmentation\watershed-method\test2.png"
img = cv.imread(IMG_PATH)
cv.imshow("org", img)

# Backgraund subtraction > 1- MOG  2- KNN 



#blur image
blur = cv.GaussianBlur(src= img, ksize=(7,7), borderType=cv.BORDER_DEFAULT,  sigmaX= 1.5, sigmaY=1.5)
#cv.imshow("5-blur", blur)

""" #smooth image
kernel = np.ones((5,5), dtype=np.float32) / 25
smooth = cv.filter2D(blur, -1, kernel )
 """
#convert hsv
hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# hsv filtering
high_value = (30,110,125)
low_value = (179, 255, 255)
image_threshold = cv.inRange(hsv_img, high_value, low_value )
cv.imshow("image_threshold-hsv",image_threshold)

#opening and dilate image
kernel  = np.ones((3,3), np.uint8)
opening = cv.morphologyEx(image_threshold, cv.MORPH_OPEN, kernel ,iterations= 4)
sure_bg = cv.dilate(opening, kernel, iterations=5)
cv.imshow("backgraund", sure_bg)

# Finding sure foreground area
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
_, sure_fg = cv.threshold(dist_transform, 0.02*dist_transform.max(), 255, 0)
cv.imshow("foregraund", sure_fg)

sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)
cv.imshow("unknown", unknown)

_, markers = cv.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0
markers = cv.watershed(img, markers)

img[markers == -1] = [255, 0, 0]

leaf_count = 0
total_leaf_area = 0
for i in range(2, markers.max() + 1):
    img[markers == i] = [randint(0, 255), randint(0, 255), randint(0, 255)] 
    leaf_count+=1
mask = copy.deepcopy(img)
mask[markers < 2] = [0, 0, 0]


cv.putText(img = mask, text= ("leaf count : " + str(leaf_count)), fontFace= cv.FONT_HERSHEY_SIMPLEX,
color= (255, 255, 255), thickness= 2, lineType= cv.LINE_AA, bottomLeftOrigin= False, org= (50,50),
fontScale= 0.8)

cv.imshow("result", img)
cv.imshow("mask", mask)
cv.waitKey()
cv.destroyAllWindows()