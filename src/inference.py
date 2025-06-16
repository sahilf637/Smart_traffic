import cv2
import os
import numpy as np
from model_loader import models

def detect_objects(input_path, model_type="traffic_violation", is_video=False):
    """
    Runs YOLOv8 detection on an image or video.

    Parameters:
    - input_path (str): Path to the input image or video.
    - model_type (str): 'traffic_violation' or 'pothole' to specify which model to use.
    - is_video (bool): Set to True if the input is a video.

    Returns:
    - If image: Processed image with detections.
    - If video: Path to the processed output video.
    - detections (list): List of detected objects.
    """

    # Ensure model_type is valid
    if model_type not in models:
        raise ValueError(f"Invalid model type. Choose from: {list(models.keys())}")

    # Load the model
    model = models[model_type]

    # Process an image
    if not is_video:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Error: Image file '{input_path}' not found.")

        image = cv2.imread(input_path)
        if image is None:
            raise ValueError("Could not load the image. Check the file path.")

        results = model(image)
        detections, output_img = process_results(results, image)
        
        # Save the processed image
        output_path = input_path.replace(".jpg", "_output.jpg")
        cv2.imwrite(output_path, output_img)

        return output_img, detections, output_path

    # Process a video
    else:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Error: Video file '{input_path}' not found.")

        output_video_path = input_path.replace(".mp4", "_output.mp4")
        process_video(input_path, output_video_path, model)
        return output_video_path, []

def process_results(results, image):
    """
    Extracts detections and draws bounding boxes on the image.
    """
    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = result.names[class_id]

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{class_name} {confidence:.2f}",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return detections, image

def process_video(input_video_path, output_video_path, model):
    """
    Processes a video frame by frame with YOLOv8.
    """
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*"H264")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        _, frame = process_results(results, frame)
        out.write(frame)

    cap.release()
    out.release()
    print(f"Video processing complete! Saved at {output_video_path}")

# Example Usage: Test on Image and Video
if __name__ == "__main__":
    # Test Image Detection for Traffic Violation
    test_img = "static/Traffic_violation.jpg"  # Ensure this file exists in static/
    output_img, detected_objects, output_img_path = detect_objects(test_img, model_type="traffic_violation")

    print("Traffic Violation Detection Complete!")
    print("Processed Image Saved at:", output_img_path)
    print("Detected Objects:", detected_objects)

    # Test Image Detection for Pothole
    test_img_pothole = "static/pothole.jpg"  # Ensure this file exists in static/
    output_img, detected_objects, output_img_path = detect_objects(test_img_pothole, model_type="pothole")

    print("Pothole Detection Complete!")
    print("Processed Image Saved at:", output_img_path)
    print("Detected Objects:", detected_objects)

    # Test Video Detection for Traffic Violation
    #test_video = "static/Traffic_violation.mp4"  # Ensure this file exists in static/
    #output_video_path, _ = detect_objects(test_video, model_type="traffic_violation", is_video=True)

    #print("Traffic Violation Video Processing Complete!")
    #print("Processed Video Saved at:", output_video_path)

    # Test Video Detection for Pothole
    test_video_pothole = "static/potholes.mp4"  # Ensure this file exists in static/
    output_video_path, _ = detect_objects(test_video_pothole, model_type="pothole", is_video=True)

    print("Pothole Video Processing Complete!")
    print("Processed Video Saved at:", output_video_path)
