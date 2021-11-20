import cv2
from time import sleep
import numpy as np

# Abrir archivo de video
cap = cv2.VideoCapture(0)

# Ancho y alto del video
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Code para archivo de video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Archivo de salida
# 30 --> fps
out = cv2.VideoWriter('new_video.mp4', fourcc, 30, (w,h))

# Rango de deteccion de colores hsv
hsv_blue_min = (190/2,50*2.55,80*2.55)
hsv_blue_max = (250/2,100*2.55,100*2.55)

# Mostrar todo el video
for i in range(150): # revisar que el video esté abierto
    ret, img = cap.read()
    # Revisar que haya más frames
    if ret == False:
        break
    
    # Segmentacion del color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, hsv_blue_min, hsv_blue_max)

    # Deteccion de contornos
    img_blur = cv2.GaussianBlur(mask_blue, (3,3), 0)
    edges = cv2.Canny(image=img_blur, threshold1=10, threshold2=200)
    
    # Relleno pixeles objetos segmentados
    mask = cv2.bitwise_not(edges)
    mask_inv = cv2.bitwise_not(mask)

    img_fl = mask_inv.copy()
    h, w = mask_inv.shape

    mask_hw = np.zeros((h+2, w+2),np.uint8)
    cv2.floodFill(img_fl, mask_hw, (1, 1), 255)
    img_fl_inv = cv2.bitwise_not(img_fl)

    # Deteccion de contornos
    fill_img = cv2.bitwise_or(mask_inv, img_fl_inv)
    cnts, h = cv2.findContours(fill_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # dibujar recuadros
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
    
    cv2.putText(img, 'Andres Sanchez Avalos :)', (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)

    # mostrar fotogramas
    cv2.imshow('Video figuras deliminadas - Sanchez Avalos Andres', img)

    # grabacion del video
    out.write(img)
    
    # Salida con tecla ESC
    if cv2.waitKey(1) == 27:
        break
    
    sleep(0.03)