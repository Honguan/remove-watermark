import cv2
import numpy
import os

src = cv2.imread('1111.png')
mask = cv2.imread('2222.png')
# 创建一张空图像用于保存

canvas = numpy.zeros(src.shape, numpy.uint8) 

for row in range(src.shape[0]):
    for col in range(src.shape[1]):
        for channel in range(src.shape[2]):
            if mask[row, col, channel] == 0:
                val = 0
            else:
                reverse_val = 255 - src[row, col, channel]
                val = 255 - reverse_val * 256 / mask[row, col, channel]
                if val < 0: 
                    val = 0
            canvas[row, col, channel] = val
#把去除水印的圖片背景透明化
tmp = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
b, g, r = cv2.split(canvas)
rgba = [b, g, r, alpha]
dst = cv2.merge(rgba, 4) 
#暫存在資料夾
cv2.imwrite('temp.png', dst)    
temp = cv2.imread('temp.png')
os.remove('temp.png')
#先刪除含有浮水印的區塊
src_subtract = cv2.subtract(src, mask)   
#去除水印圖和原圖合成
result = cv2.addWeighted(src_subtract, 1, temp, 1, 0)
cv2.imshow('src', src)
#cv2.imshow('mask', mask)
cv2.imshow('neutralization_result', result)
#cv2.imwrite('neutralization_result.png', result)
cv2.waitKey(0)
cv2.destroyAllWindows()