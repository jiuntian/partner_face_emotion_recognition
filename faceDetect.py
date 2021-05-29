import cv2
import numpy as np
from PIL import Image

scale = 0.2
haar_cascade = cv2.CascadeClassifier(r'resource/haarcascade_frontface_default.xml')


def detectFaceArea(img: np.ndarray) -> list:
    """
    Detect area of face

    Returns:
        list: a list of *scaled* 4-element tuples (x, y, width, height)
    """
    # resize image
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)), interpolation=cv2.INTER_AREA)
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect using haar cascade
    scaled_faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    faces_rect = []
    for (x, y, w, h) in scaled_faces_rect:
        faces_rect.append((x//scale, y//scale, w//scale, h//scale))
    
    return faces_rect

def cvt_cv2_to_PIL(img: np.ndarray) -> Image:
    """Convert from OpenCV Numpy image to PIL image"""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def cvt_PIL_to_cv2(img: Image) -> np.ndarray:
    """Convert from PIL image to OpenCV Numpy image"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def drawRect(img: np.ndarray, faces_rect: list):
    """Draw rectangle on image"""
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
