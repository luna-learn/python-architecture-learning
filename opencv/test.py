import opencv as cv2

# 创建Haar级联器
facer = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
# 导入人脸图片并灰度化
img = cv2.imread('p3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 调用接口
faces = facer.detectMultiScale(gray, 1.1, 5)

for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)

cv2.imshow('img', img)
cv2.waitKey()