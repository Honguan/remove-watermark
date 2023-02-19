import cv2
import numpy as np

path = "5555.png"
org = cv2.imread(path)
dot1 = []                          # 記錄第一個座標
dot2 = []                          # 記錄第二個座標
# 選擇擷取區塊
def ROI(event,x,y,flags,param):
    global dot1, dot2, org         # 在函式內使用全域變數
    # 滑鼠拖曳發生時
    if flags == 1:
        if event == 1:
            dot1 = [x, y]          # 按下滑鼠時記錄第一個座標
        if event == 0:
            img2 = org.copy()      # 拖曳時不斷複製 org
            dot2 = [x, y]          # 拖曳時不斷更新第二個座標
            # 根據兩個座標繪製四邊形
            cv2.rectangle(img2, (dot1[0], dot1[1]), (dot2[0], dot2[1]), (0,0,255), 2)
            # 不斷顯示新圖片 ( 如果不這麼做，會出現一堆四邊形殘影 )
            cv2.imshow('image', img2)
            
            
cv2.imshow('image', org)            
cv2.setMouseCallback('image', ROI)
cv2.waitKey(0) 
cv2.destroyAllWindows()
img = org

#提取出水印區塊，以及要填入浮水印的顏色參數
thresh = cv2.inRange(img[dot1[1]:dot2[1],dot1[0]:dot2[0]],
                     np.array([170,170,170]),
                     np.array([200,200,200]))

#腐蝕水印區塊
kernel  = np.ones((5,5),np.uint8)
cor = cv2.dilate(thresh,kernel,iterations=1)

#還原圖片，修復算法(包括INPAINT_TELEA/INPAINT_NS， 前者算法效果較好)
specular = cv2.inpaint(img[dot1[1]:dot2[1],dot1[0]:dot2[0]],cor,5,flags=cv2.INPAINT_TELEA)

#區塊圖片替換
temp = img[dot1[1]:dot2[1],dot1[0]:dot2[0]]
img[dot1[1]:dot2[1],dot1[0]:dot2[0]] = np.ones(temp.shape, dtype="uint8")
img[dot1[1]:dot2[1],dot1[0]:dot2[0]] = specular

#輸出和顯示圖片
#cv2.imshow("image",org)
cv2.imshow("thresh",thresh)
cv2.imshow("inpaint_result",img)
#cv2.imwrite('inpaint_result.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
