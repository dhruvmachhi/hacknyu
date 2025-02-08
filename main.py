import cv2
import numpy as np
import csv

# Load Haar cascades for face and eyes detection.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

KNOWN_DISTANCE_MM = 63  # Known interpupillary distance in mm.
FRAME_COUNT = 20        # Number of valid frames to average per run.
TOTAL_RUNS = 5          # Number of complete measurement runs.
all_measurements = []

def is_face_centered(face_x, face_y, face_w, face_h, frame_width, frame_height):
    """Checks if the detected face is centered and large enough."""
    center_x = face_x + face_w // 2
    center_y = face_y + face_h // 2
    tolerance_x = frame_width * 0.2  
    tolerance_y = frame_height * 0.2  
    min_face_height = frame_height * 0.3  # Face must occupy at least 30% of the frame height.
    
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
    gray_eye = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
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
        # Convert circle parameters to integers to avoid unsigned arithmetic issues.
        circles = np.around(circles[0, :]).astype(int)
        x, y, r = circles[0]  # Use the first detected circle (assumed to be the iris/pupil).
        return int(x - r), int(x + r)
    return None, None

def detect_pupil_center(eye_roi):
    """
    Detects the pupil center using HoughCircles.
    Returns the (x, y) coordinates relative to the eye ROI.
    """
    gray_eye = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
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

# Countdown before starting measurement.
for i in range(3, 0, -1):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, f"Starting in {i}...", (frame.shape[1] // 3, frame.shape[0] // 2), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    cv2.imshow("Face Alignment & Measurement", frame)
    cv2.waitKey(1000)

# Define how many consecutive frames we allow to lose the face before resetting.
lost_frame_threshold = 10

for run in range(TOTAL_RUNS):
    print(f"Starting measurement run {run + 1}/{TOTAL_RUNS}...")
    measurements = []
    lost_frame_count = 0

    while len(measurements) < FRAME_COUNT:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            continue

        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

        if len(faces) == 0:
            lost_frame_count += 1
            if lost_frame_count >= lost_frame_threshold:
                # Too many consecutive frames without a detected face; reset this run.
                measurements = []
                print("Face lost for several frames. Resetting current measurement run.")
            cv2.putText(frame, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            lost_frame_count = 0  # Reset counter once a face is detected.
            for (x, y, w, h) in faces:
                if not is_face_centered(x, y, w, h, frame_width, frame_height):
                    cv2.putText(frame, "Align Face in Oval", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    continue

                # Draw face bounding box.
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
                eye_boxes = []
                for (ex, ey, ew, eh) in eyes:
                    eye_boxes.append((ex, ey, ew, eh))
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

                if len(eye_boxes) >= 2:
                    # Sort the detected eyes left-to-right.
                    eye_boxes.sort(key=lambda box: box[0])
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
                        # Convert the local (eye ROI) coordinates to the face ROI coordinates.
                        left_iris_global = left_eye[0] + left_boundaries[0]
                        right_iris_global = right_eye[0] + right_boundaries[1]
                        eye_total_width_pixels = right_iris_global - left_iris_global

                        left_pupil_global = left_eye[0] + left_pupil[0]
                        right_pupil_global = right_eye[0] + right_pupil[0]
                        interpupil_distance_pixels = right_pupil_global - left_pupil_global

                        if interpupil_distance_pixels > 0:
                            pixel_to_mm_ratio = KNOWN_DISTANCE_MM / interpupil_distance_pixels
                        else:
                            pixel_to_mm_ratio = 1  # Fallback

                        eye_width_mm = round(eye_total_width_pixels * pixel_to_mm_ratio, 2)
                    else:
                        # Fallback if iris/pupil detection fails:
                        avg_eye_width = (left_eye[2] + right_eye[2]) / 2
                        left_center = left_eye[0] + left_eye[2] / 2
                        right_center = right_eye[0] + right_eye[2] / 2
                        interpupil_distance_pixels = right_center - left_center
                        if interpupil_distance_pixels > 0:
                            pixel_to_mm_ratio = KNOWN_DISTANCE_MM / interpupil_distance_pixels
                        else:
                            pixel_to_mm_ratio = 1
                        eye_width_mm = round(avg_eye_width * pixel_to_mm_ratio, 2)

                    # Calculate the bridge width (distance between the eyes).
                    bridge_distance_pixels = right_eye[0] - (left_eye[0] + left_eye[2])
                    bridge_width_mm = round(bridge_distance_pixels * pixel_to_mm_ratio, 2)

                    # Estimate vertical dimension ("b_size") using a fraction of the eye height.
                    left_eye_height = min(left_eye[3], int(left_eye[2] * 0.6))
                    right_eye_height = min(right_eye[3], int(right_eye[2] * 0.6))
                    b_size_pixels = max(left_eye_height, right_eye_height)
                    b_size_mm = round(b_size_pixels * pixel_to_mm_ratio, 2)

                    measurement = {
                        'eye_width_mm': eye_width_mm,
                        'bridge_width_mm': bridge_width_mm,
                        'b_size_mm': b_size_mm
                    }
                    measurements.append(measurement)
                    # Once a valid measurement is taken from one face, break out of the face loop.
                    break

        # Draw an alignment ellipse to guide the user.
        cv2.ellipse(frame, (frame_width // 2, frame_height // 2), 
                    (frame_width // 5, frame_height // 4), 0, 0, 360, (255, 255, 255), 2)
        cv2.imshow("Face Alignment & Measurement", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if len(measurements) == FRAME_COUNT:
        all_measurements.append(measurements)
    else:
        print("Measurement run did not complete successfully, retrying...")

cap.release()
cv2.destroyAllWindows()

# After collecting measurements from all runs, average them and save to CSV.
if len(all_measurements) == TOTAL_RUNS:
    total_measurements = FRAME_COUNT * TOTAL_RUNS
    final_measurements = {
        'eye_width_mm': round(sum(m['eye_width_mm'] for run in all_measurements for m in run) / total_measurements, 2),
        'bridge_width_mm': round(sum(m['bridge_width_mm'] for run in all_measurements for m in run) / total_measurements, 2),
        'b_size_mm': round(sum(m['b_size_mm'] for run in all_measurements for m in run) / total_measurements, 2)
    }

    csv_filename = "glasses_final_dimensions.csv"
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Measurement", "Value (mm)"])
        writer.writerow(["Eye Width", final_measurements['eye_width_mm']])
        writer.writerow(["Bridge Size", final_measurements['bridge_width_mm']])
        writer.writerow(["B Size (Vertical Height)", final_measurements['b_size_mm']])

    print(f"✅ Final Measurements saved to {csv_filename}")
    print("✅ Program automatically closed after completing multiple runs.")