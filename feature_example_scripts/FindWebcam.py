import cv2
import pathlib

currentpath = pathlib.Path(__file__).parent.resolve()
def take_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    filePath = currentpath/'testWebcamPhoto.jpg'
    cv2.imwrite( filePath, frame)
    cap.release()

take_photo()