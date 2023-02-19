import cv2
# 讀取圖片並縮放方便顯示
img = cv2.imread('55557.png')
height, width = img.shape[:2]
size = (int(width * 1.2), int(height * 1.2))
# 縮放
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

temp1 = []
# 鼠標點擊響應事件
def RGB_check(event, x, y, flags, param):
    global temp1
    if event==cv2.EVENT_LBUTTONDOWN:
        print("RGB is:", img[y, x])
        temp1 = img[y, x]
        
cv2.imshow('image', img)
cv2.setMouseCallback("image", RGB_check)
cv2.waitKey(0)
cv2.destroyAllWindows()