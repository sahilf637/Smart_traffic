import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium
import requests
import plotly.express as px

# API URL (Make sure Flask is running)
API_URL = "http://127.0.0.1:5000"

# Define file paths for processed images & videos
IMAGE_FOLDER = "static/uploads/"
VIDEO_FOLDER = "static/uploads/"

# Page Title
st.title("🚦 AI-Powered Traffic & Pothole Detection Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📸 Upload Image", "🎥 Upload Video", "📸 Image Results", "🎥 Video Results", "📊 Detection Analytics"])

# IMAGE UPLOAD & DETECTION
if page == "📸 Upload Image":
    st.subheader("📸 Upload an Image for Detection")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    model_type = st.selectbox("Select Model", ["traffic_violation", "pothole"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Detect Objects"):
        files = {"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
        data = {"model_type": model_type}

        response = requests.post(f"{API_URL}/detect_image", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            st.write("Detection Complete!")
            st.image(result["processed_image"], caption="Processed Image", use_container_width=True)
            st.json(result["detected_objects"])
        else:
            st.error(f"Detection failed! Error {response.status_code}: {response.text}")

# VIDEO UPLOAD & DETECTION
elif page == "🎥 Upload Video":
    st.subheader("🎥 Upload a Video for Detection")
    uploaded_video = st.file_uploader("Choose a video...", type=["mp4"])
    model_type = st.selectbox("Select Model", ["traffic_violation", "pothole"])

    if uploaded_video is not None:
        st.video(uploaded_video)

        if st.button("Detect Objects in Video"):
            files = {"file": (uploaded_video.name, uploaded_video, "video/mp4")}
            data = {"model_type": model_type}
            response = requests.post(f"{API_URL}/detect_video", files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                st.write("Video Processing Complete!")
                st.video(result["processed_video"])
            else:
                st.error("Detection failed! Try again.")

# IMAGE DETECTION RESULTS PAGE
elif page == "📸 Image Results":
    st.subheader("📸 Processed Images")

    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".png"))]

    if len(image_files) == 0:
        st.warning("No processed images found. Upload an image first.")
    else:
        for img_file in image_files:
            st.image(os.path.join(IMAGE_FOLDER, img_file), caption=f"Detected - {img_file}", use_container_width=True)

# VIDEO DETECTION RESULTS PAGE
elif page == "🎥 Video Results":
    st.subheader("🎥 Processed Videos")

    video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4")]

    if len(video_files) == 0:
        st.warning("No processed videos found. Upload a video first.")
    else:
        for vid_file in video_files:
            st.video(os.path.join(VIDEO_FOLDER, vid_file))

# DETECTION ANALYTICS PAGE (Real-Time Updates)
elif page == "📊 Detection Analytics":
    st.subheader("📊 Detection Statistics (Live)")

    # Fetch detection counts
    response = requests.get(f"{API_URL}/get_detection_stats")
    detection_data = response.json() if response.status_code == 200 else {"Traffic Violation": 0, "Potholes": 0}

    col1, col2 = st.columns(2)
    col1.metric("🚦 Traffic Violations", detection_data["Traffic Violation"])
    col2.metric("🛣️ Potholes Detected", detection_data["Potholes"])

    # Fetch recent detections log
    response = requests.get(f"{API_URL}/get_recent_detections")
    recent_detections = response.json() if response.status_code == 200 else []

    st.subheader("📝 Recent Detections (Last 5)")
    if recent_detections:
        df_logs = pd.DataFrame(recent_detections)
        st.table(df_logs)
    else:
        st.info("No recent detections available.")

    # Pie Chart for Violation Distribution
    df_pie = pd.DataFrame(detection_data.items(), columns=["Violation Type", "Count"])
    fig = px.pie(df_pie, values="Count", names="Violation Type", title="🚦 Violation Distribution")
    st.plotly_chart(fig)

    # Show Live Map of Detections
    st.subheader("📍 Live Violation & Pothole Locations")
    response = requests.get(f"{API_URL}/get_detection_locations")

    if response.status_code == 200:
        detection_data = response.json()
    else:
        detection_data = []

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    for detection in detection_data:
        folium.Marker(
            [detection["latitude"], detection["longitude"]],
            popup=detection["event"]
        ).add_to(m)

    st_folium(m)
