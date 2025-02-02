import cv2
import numpy as np
from typing import Optional, Tuple
import logging
import os

# Get the directory containing this file
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def process_image_for_face_recognition(image_path: str) -> Optional[np.ndarray]:
    """Process an image and return face encoding if a face is detected."""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            logging.error("Failed to load image")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            logging.warning("No face detected in the image")
            return None

        if len(faces) > 1:
            logging.warning("Multiple faces detected in the image")
            return None

        # Get the face ROI
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]

        # Resize to a standard size
        face_roi = cv2.resize(face_roi, (128, 128))

        # Flatten and normalize
        face_encoding = face_roi.flatten() / 255.0

        return face_encoding

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return None

def compare_faces(known_encoding: np.ndarray, unknown_encoding: np.ndarray, 
                 tolerance: float = 0.6) -> bool:
    """Compare two face encodings and return True if they match."""
    try:
        if known_encoding is None or unknown_encoding is None:
            return False

        # Calculate euclidean distance
        distance = np.linalg.norm(known_encoding - unknown_encoding)
        return distance < tolerance

    except Exception as e:
        logging.error(f"Error comparing faces: {str(e)}")
        return False

def detect_face_from_frame(frame: np.ndarray) -> Tuple[bool, Optional[np.ndarray]]:
    """Detect and encode face from a video frame."""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) == 0:
            return False, None

        # Get the face ROI
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]

        # Resize to a standard size
        face_roi = cv2.resize(face_roi, (128, 128))

        # Flatten and normalize
        face_encoding = face_roi.flatten() / 255.0

        return True, face_encoding

    except Exception as e:
        logging.error(f"Error processing frame: {str(e)}")
        return False, None