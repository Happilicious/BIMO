import cv2

#camera = cv2.VideoCapture('http://192.168.43.242:8080/?action=stream')
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    cv2.imshow('Camera Feed', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break;

height, width = frame.shape[:2]
print(height)
print(width)

camera.release()
cv2.destroyAllWindows()
