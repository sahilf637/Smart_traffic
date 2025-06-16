from ultralytics import YOLO
import os

# Define absolute model path
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))

# Load YOLO Models
def load_models():
    model_paths = {
        "pothole": os.path.join(MODEL_DIR, "pothole_best.pt"),
        "traffic_violation": os.path.join(MODEL_DIR, "traffic_best.pt")
    }

    models = {}
    for model_name, model_path in model_paths.items():
        if os.path.exists(model_path):
            models[model_name] = YOLO(model_path)
            print(f"Loaded {model_name} model successfully from {model_path}")
        else:
            print(f"Error: {model_name} model not found at {model_path}")

    return models

# Load models when script is executed
models = load_models()
