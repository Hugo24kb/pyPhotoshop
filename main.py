### Current Usage --> clone the repo and add an image named 'test.jpg' to the repo
###               --> Run main.py
### The index.html will soon be hosted, as some pyscript functions are still testing

import cv2
import numpy as np

def cartoonify_image(image):
    grayScaleImage= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)
    colorImage = cv2.bilateralFilter(image, 9, 300, 300)
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    return cartoonImage

def blur_image(image):
    blurred_image = cv2.blur(image,(20,20))
    return blurred_image

def brighten_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype = np.float64)
    hsv[:,:,1] = hsv[:,:,1]*1.25
    hsv[:,:,1][hsv[:,:,1]>255]  = 255
    hsv[:,:,2] = hsv[:,:,2]*1.25
    hsv[:,:,2][hsv[:,:,2]>255]  = 255
    hsv = np.array(hsv, dtype = np.uint8)
    brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return brightened_image

def count_faces(img):
    img2 = img.copy()
    scale = 150
    width = int(img2.shape[1] * scale / 100)
    height = int(img2.shape[0] * scale / 100)
    dim = (width, height)
    img2 = cv2.resize(img2, dim)
    sharpen_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img3 = cv2.filter2D(img2, -1, sharpen_filter)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img2, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite('img5.jpg', img2)
    return len(faces)

def main():
    img = cv2.imread('test.jpg')
    print(count_faces(img))
    img2 = cartoonify_image(img)
    img3 = blur_image(img)
    img4 = brighten_image(img)
    cv2.imwrite('img2.jpg', img2)
    cv2.imwrite('img3.jpg', img3)
    cv2.imwrite('img4.jpg', img4)
    return None

if __name__ == "__main__":
    main()
    
