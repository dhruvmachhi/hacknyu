from flask import Flask, jsonify, request
from flask_cors import CORS  # Enable cross-origin requests
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

KNOWN_DISTANCE_MM = 63  

# Load Haar cascade files
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def is_face_centered(face_x, face_y, face_w, face_h, frame_width, frame_height):
    """Checks if the detected face is centered and large enough."""
    center_x = face_x + face_w // 2
    center_y = face_y + face_h // 2
    tolerance_x = frame_width * 0.2  
    tolerance_y = frame_height * 0.2  
    min_face_height = frame_height * 0.3  
    return (
        (frame_width // 2 - tolerance_x < center_x < frame_width // 2 + tolerance_x) and
        (frame_height // 2 - tolerance_y < center_y < frame_height // 2 + tolerance_y) and
        (face_h > min_face_height)
    )

def detect_iris_boundaries(eye_roi):
    """
    Detects the iris boundaries using HoughCircles.
    Returns (left_boundary, right_boundary) relative to the eye ROI.
    """
    try:
        gray_eye = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
    except Exception:
        return None, None
    gray_eye = cv2.medianBlur(gray_eye, 5)
    circles = cv2.HoughCircles(
        gray_eye,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=gray_eye.shape[0] / 2,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=int(gray_eye.shape[0] / 2)
    )
    if circles is not None:
        circles = np.around(circles[0, :]).astype(int)
        x, y, r = circles[0]  
        return int(x - r), int(x + r)
    return None, None

def detect_pupil_center(eye_roi):
    """
    Detects the pupil center using HoughCircles.
    Returns the (x, y) coordinates relative to the eye ROI.
    """
    try:
        gray_eye = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
    except Exception:
        return None
    gray_eye = cv2.medianBlur(gray_eye, 5)
    circles = cv2.HoughCircles(
        gray_eye,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=gray_eye.shape[0] / 2,
        param1=50,
        param2=30,
        minRadius=3,
        maxRadius=20
    )
    if circles is not None:
        circles = np.around(circles[0, :]).astype(int)
        x, y, r = circles[0]
        return int(x), int(y)
    return None

def process_frame(frame):
    """
    Process a single frame (already decoded as a BGR image) to detect face/eyes
    and perform measurements. Returns a dictionary with measurements or an error.
    """
    if frame is None:
        return None, "Invalid image data."

    frame_height, frame_width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Adjusted parameters for better detection on webcam images
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50))

    if len(faces) == 0:
        return None, "No face detected. Please ensure your face is visible and well-lit."

    for (x, y, w, h) in faces:
        if not is_face_centered(x, y, w, h, frame_width, frame_height):
            continue 

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # Adjust eye detection parameters for better results
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))
        if len(eyes) < 2:
            return None, "Not enough eyes detected. Please center your face properly."

        # Sort eyes based on x-coordinate (left to right)
        eye_boxes = sorted(eyes, key=lambda b: b[0])
        left_eye = eye_boxes[0]
        right_eye = eye_boxes[1]

        left_eye_roi = roi_color[left_eye[1]:left_eye[1] + left_eye[3], left_eye[0]:left_eye[0] + left_eye[2]]
        right_eye_roi = roi_color[right_eye[1]:right_eye[1] + right_eye[3], right_eye[0]:right_eye[0] + right_eye[2]]

        left_boundaries = detect_iris_boundaries(left_eye_roi)
        right_boundaries = detect_iris_boundaries(right_eye_roi)
        left_pupil = detect_pupil_center(left_eye_roi)
        right_pupil = detect_pupil_center(right_eye_roi)

        if (left_boundaries[0] is not None and right_boundaries[1] is not None and 
            left_pupil is not None and right_pupil is not None):
            left_iris_global = left_eye[0] + left_boundaries[0]
            right_iris_global = right_eye[0] + right_boundaries[1]
            eye_total_width_pixels = right_iris_global - left_iris_global

            left_pupil_global = left_eye[0] + left_pupil[0]
            right_pupil_global = right_eye[0] + right_pupil[0]
            interpupil_distance_pixels = right_pupil_global - left_pupil_global

            if interpupil_distance_pixels > 0:
                pixel_to_mm_ratio = KNOWN_DISTANCE_MM / interpupil_distance_pixels
            else:
                pixel_to_mm_ratio = 1 
            eye_width_mm = round(eye_total_width_pixels * pixel_to_mm_ratio, 2)
        else:
            avg_eye_width = (left_eye[2] + right_eye[2]) / 2
            left_center = left_eye[0] + left_eye[2] / 2
            right_center = right_eye[0] + right_eye[2] / 2
            interpupil_distance_pixels = right_center - left_center
            if interpupil_distance_pixels > 0:
                pixel_to_mm_ratio = KNOWN_DISTANCE_MM / interpupil_distance_pixels
            else:
                pixel_to_mm_ratio = 1
            eye_width_mm = round(avg_eye_width * pixel_to_mm_ratio, 2)

        bridge_distance_pixels = right_eye[0] - (left_eye[0] + left_eye[2])
        bridge_width_mm = round(bridge_distance_pixels * pixel_to_mm_ratio, 2)

        left_eye_height = min(left_eye[3], int(left_eye[2] * 0.6))
        right_eye_height = min(right_eye[3], int(right_eye[2] * 0.6))
        b_size_pixels = max(left_eye_height, right_eye_height)
        b_size_mm = round(b_size_pixels * pixel_to_mm_ratio, 2)

        measurement = {
            'eye_width_mm': eye_width_mm,
            'bridge_width_mm': bridge_width_mm,
            'b_size_mm': b_size_mm
        }
        return measurement, None

    return None, "No centered face found. Please adjust your position."

@app.route('/api/measure', methods=['POST'])
def measure_api():
    """
    Expects a JSON payload with an "image" field containing a base64-encoded JPEG.
    Processes the image with OpenCV and returns the measurements.
    """
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided."}), 400

    img_data = data['image']
    if "," in img_data:
        # Remove data URL header if present
        img_data = img_data.split(",")[1]
    try:
        decoded = base64.b64decode(img_data)
        np_data = np.frombuffer(decoded, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Could not decode image."}), 400
    except Exception:
        return jsonify({"error": "Could not decode image."}), 400

    measurement, error_msg = process_frame(frame)
    if error_msg:
        return jsonify({"error": error_msg}), 400

    return jsonify(measurement)

if __name__ == '__main__':
    app.run(debug=True)
