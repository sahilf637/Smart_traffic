from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from inference import detect_objects

# Define the correct path to the models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go one level up
MODEL_DIR = os.path.join(BASE_DIR, "models")  # Locate models folder

pothole_model_path = os.path.join(MODEL_DIR, "pothole_best.pt")
traffic_violation_model_path = os.path.join(MODEL_DIR, "traffic_best.pt")

# Ensure models exist
if not os.path.exists(pothole_model_path):
    print(f"Error: Pothole model not found at {pothole_model_path}")

if not os.path.exists(traffic_violation_model_path):
    print(f"Error: Traffic violation model not found at {traffic_violation_model_path}")


app = Flask(__name__)

# Create an uploads folder if it doesn't exist
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4"}

# 🔹 Global storage for tracking detection counts
detection_stats = {"Traffic Violation": 0, "Potholes": 0}
recent_detections = []

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Define class names for Traffic Violation Model
TRAFFIC_VIOLATION_CLASSES = {
    "0 - motorcycle": "Motorcycle Violation",
    "1 - motorcycle - pedestrian road": "Motorcycle on Pedestrian Road",
    "13 - bicycle - stop line": "Bicycle on Stop Line",
    "14 - bicycle - crosswalk": "Bicycle on Crosswalk",
    "3 - motorcycle - jaywalk": "Motorcycle Jaywalking",
    "5 - motorcycle - stop line": "Motorcycle on Stop Line",
    "6 - motorcycle - crosswalk": "Motorcycle on Crosswalk",
    "7 - bicycle": "Bicycle Violation",
    "9 - bicycle - pedestrian road": "Bicycle on Pedestrian Road"
}

@app.route("/detect_image", methods=["POST"])
def detect_image():
    """
    API to detect objects in an uploaded image.
    Returns detected objects in JSON format.
    """
    global detection_stats, recent_detections

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    model_type = request.form.get("model_type", "traffic_violation")  # Default to traffic violation

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Run YOLO detection
        _, detections, output_path = detect_objects(file_path, model_type=model_type)

        # Convert traffic violation class names to readable labels
        for detection in detections:
            if model_type == "traffic_violation":
                detection["class"] = TRAFFIC_VIOLATION_CLASSES.get(detection["class"], detection["class"])

        # Update detection count
        if model_type == "pothole":
            detection_stats["Potholes"] += len(detections)
        else:
            detection_stats["Traffic Violation"] += len(detections)

        # Store recent detections
        for detection in detections:
            recent_detections.append({
                "Type": detection["class"],  # Now stores readable class names
                "Confidence": round(detection["confidence"], 2),
                "Model": model_type  # Track the source of detection
            })

        return jsonify({
            "message": "Detection complete",
            "model_used": model_type,
            "detected_objects": detections,
            "processed_image": output_path
        })

    else:
        return jsonify({"error": "Invalid file format"}), 400

#  Video Detection API
@app.route("/detect_video", methods=["POST"])
def detect_video():
    """
    API to detect objects in an uploaded video.
    Returns the processed video path.
    """
    global detection_stats, recent_detections

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    model_type = request.form.get("model_type", "traffic_violation")  # Default to traffic violation

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Run YOLO detection on video
        output_video_path, detections = detect_objects(file_path, model_type=model_type, is_video=True)

        # Update detection count
        if model_type == "pothole":
            detection_stats["Potholes"] += len(detections)
        else:
            detection_stats["Traffic Violation"] += len(detections)

        # Store recent detections
        for detection in detections:
            recent_detections.append({
                "Type": detection["class"],
                "Confidence": round(detection["confidence"], 2)
            })

        return jsonify({
            "message": "Video processing complete",
            "model_used": model_type,
            "processed_video": output_video_path
        })
    else:
        return jsonify({"error": "Invalid file format"}), 400

# API to Get Detection Statistics
@app.route("/get_detection_stats", methods=["GET"])
def get_detection_stats():
    return jsonify(detection_stats)

# API to Get Recent Detections
@app.route("/get_recent_detections", methods=["GET"])
def get_recent_detections():
    return jsonify(recent_detections[-5:])  # Send only last 5 detections

# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Traffic Violation & Pothole Detection API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
