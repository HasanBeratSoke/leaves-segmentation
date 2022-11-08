import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.feature import peak_local_max


IMG_PATH = r'Contour-Region-Detection\test2.png'
img  = cv.imread(IMG_PATH)
cv.imshow("1-org", img)

""" -- A -- """
# Preserve Edges
preserve_edges = cv.bilateralFilter(img, 9, 75  , 75 )
cv.imshow("2-pre-edges", preserve_edges )

# Stylization Filter
dst = cv.edgePreservingFilter(preserve_edges, flags=1, sigma_s= 60, sigma_r=0.07)
cv.imshow("3-dst", dst )

#3 to 1 chennel
gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
cv.imshow("4-gray", gray)

#apply Gaussian filter for blurring image background
blur = cv.GaussianBlur(src= gray, ksize=(7,7), borderType=cv.BORDER_DEFAULT,  sigmaX= 1.5, sigmaY=1.5)
cv.imshow("5-blur", blur)

#expand
dila = cv.dilate(blur, kernel= (3,3), iterations= 1)
cv.imshow("6-dila", dila)

""" -- B -- """
#smooth edges
kernel = np.ones((5,5), dtype=np.float32) / 25
smooth = cv.filter2D(dila, -1, kernel )
cv.imshow("7B-smooth" , smooth)

#adative threhold
thresh = cv.adaptiveThreshold(src= smooth, maxValue=255, adaptiveMethod= cv.ADAPTIVE_THRESH_GAUSSIAN_C, blockSize= 11, thresholdType= cv.THRESH_BINARY , C= 2)
cv.imshow("8B-adaptiveThresh" , thresh)


""" -- C -- """
#binary otsu threshold
thresh_otsu = cv.threshold(dila,200,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)[1]
cv.imshow("7C-otsu" , thresh_otsu)

#erosyon and dila and border
kernel  = np.ones((3,3), np.uint8)
dila = cv.dilate(thresh_otsu, kernel, iterations=6)
cv.imshow("8C-dilate", dila)

erosion = cv.erode(dila, kernel, iterations=4)
cv.imshow("9C-erosion", erosion)

#siyah noktalı kapatma
closing = cv.morphologyEx(erosion.astype(np.float32),cv.MORPH_CLOSE,kernel, iterations= 3)
cv.imshow("10C-Closing",closing)

#detect counter
img_copy1 = img.copy()
contours_C, hierarchy = cv.findContours(image=erosion, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
cv.drawContours(image=img_copy1, contours=contours_C, contourIdx=-1, color=(0, 0, 0), thickness=2, lineType=cv.LINE_AA)
cv.imshow("11C-contoure", img_copy1)

img_copy2 = img.copy()
contours_B, hierarchy = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)
cv.drawContours(image=img_copy2, contours=contours_B, contourIdx=-1, color=(0, 0, 0), thickness=2, lineType=cv.LINE_AA) 
cv.imshow("11B-contoure", img_copy2)

#compare and draw best contoure
img_copy3 = img.copy()
contours_C = sorted(contours_C, key=lambda x: cv.contourArea(x),reverse=True)
contours_B = sorted(contours_B, key=lambda x: cv.contourArea(x),reverse=True)

total_leaf_area = 0
total_leaf_area_cm2 = 0
for i, j in zip(contours_C, contours_B):
    r = cv.matchShapes(i, j, 1, 0.0)
    print(r)
    if ((r < 850) and (cv.contourArea(i) < 90000 )):
       cv.drawContours(img_copy3, i, -1, (0, 0, 255), 4) 
       total_leaf_area += cv.contourArea(i)


RATIO_PIXEL_TO_CM  = 78
RATIO_PIXEL_TO_SQURE_CM = 78*78

total_leaf_area_cm2 = round(total_leaf_area / RATIO_PIXEL_TO_SQURE_CM,2)
cv.putText(img_copy3, "total leaf area : {} cm2 ".format(total_leaf_area_cm2), fontFace= cv.FONT_HERSHEY_SIMPLEX,
color= (255, 255, 255), thickness= 2, lineType= cv.LINE_AA, bottomLeftOrigin= False, org= (50,50),
fontScale= 0.8)

cv.imshow("result",img_copy3)
                   

cv.waitKey()
cv.destroyAllWindows()