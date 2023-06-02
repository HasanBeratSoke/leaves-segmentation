import cv2
import numpy as np

# resmi oku
img = cv2.imread("./IMG_0167.JPG")


scale_percent = 20 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 

# gri tonlamaya dönüştür
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# sınırları bulmak için Gaussian gürültüyü azalt
blur = cv2.GaussianBlur(gray, (5, 5), 0)

edges = cv2.Canny(blur, 50, 150)
cv2.imshow("edges",edges)
# binary threshhold kullanarak sınırları belirle
_, thresh = cv2.threshold(blur, 145, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("thresh", thresh)

#erosion
kernel = np.ones((5, 5), np.uint8)
threh = cv2.erode(thresh, kernel, iterations=1)
cv2.imshow("res", thresh)


# konturları bul
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for contour in contours:
    area = cv2.contourArea(contour)
    if area < 9000:
        # Boyut belirli bir eşikten küçükse, bölgeyi silelim
        cv2.drawContours(thresh, [contour], 0, (255,255,255), -1)

cv2.imshow("area", thresh)
# her bir konturu kutu içine al
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # kutu boyutunun belirli bir eşiğin altındaysa sil
    if (w < 100 or h < 100) or (w>300 or h>300):
        continue
        
    # kutuyu oluştur
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

# sonuç resmi görüntüle
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
