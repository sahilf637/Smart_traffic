
# 🚦 AI-Powered Traffic Violation & Pothole Detection System  

## 🔥 Project Overview  
This project is an **AI-powered system** that detects **traffic violations** (wrong-way driving, red-light running, etc.) and **road conditions** (potholes, cracks, lane damage) using **YOLOv8 object detection**.  

### **✨ Key Features**  
✅ **Traffic Violation Detection** – Identifies violations such as motorcycle on pedestrian road, jaywalking, and more.  
✅ **Pothole Detection** – Detects potholes and road damages for better infrastructure monitoring.  
✅ **Real-time Detection API** – Uses a Flask backend to process images & videos.  
✅ **Interactive Dashboard** – A **Streamlit-powered UI** for real-time monitoring & analysis.  
✅ **Live Detection Statistics** – Displays violation counts, trends, and a heatmap of detections.  

---

## **🛠️ Tech Stack**  
| Component  | Technology |
|------------|------------|
| **Object Detection** | YOLOv8 |
| **Backend API** | Flask |
| **Frontend Dashboard** | Streamlit |
| **Data Processing** | OpenCV, NumPy, Pandas |
| **Visualization** | Plotly, Folium (for live maps) |
| **Deployment** | AWS EC2, tmux (for persistent processes) |
| **Version Control** | Git & GitHub |

---

## **🚀 Installation & Setup (Local Machine)**  

### **📌 Step 1: Clone the Repository**  
```bash
git clone https://github.com/YOUR_USERNAME/AI-Traffic-Violation-Detection.git
cd AI-Traffic-Violation-Detection
```

### **📌 Step 2: Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac  
venv\Scripts\activate  # For Windows  
```

### **📌 Step 3: Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **📌 Step 4: Run the Flask API**  
```bash
python src/routes.py
```
- The API should now be running at **`http://127.0.0.1:5000/`**.  
- You can test it by opening the URL in your browser.  

### **📌 Step 5: Start the Streamlit Dashboard**  
In a new terminal, run:  
```bash
streamlit run src/dashboard.py
```
- The dashboard should open at **`http://localhost:8501/`**.  

---

## **🚀 Cloud Deployment on AWS EC2**
💡 **Follow these steps to deploy the system on AWS EC2.**

### **📌 Step 1: Launch an EC2 Instance**
1. Log in to [AWS Console](https://aws.amazon.com/console/).
2. Go to **EC2** and click **Launch Instance**.
3. Choose **Ubuntu 22.04 LTS** as the OS.
4. Select instance type **t2.medium** (at least 4GB RAM).
5. Configure security groups:
   - Allow **SSH (22)**
   - Allow **Flask API (5000)**
   - Allow **Streamlit (8501)**
6. **Launch** and download the **private key file (.pem)**.

---

### **📌 Step 2: Connect to EC2**
```bash
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

---

### **📌 Step 3: Install Required Packages**
Run the following commands:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip tmux -y
```

---

### **📌 Step 4: Clone the GitHub Repository**
```bash
git clone https://github.com/YOUR_USERNAME/AI-Traffic-Violation-Detection.git
cd AI-Traffic-Violation-Detection
```

---

### **📌 Step 5: Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### **📌 Step 6: Transfer YOLOv8 Models to EC2**
1. **From your local machine, copy the trained models to EC2:**
```bash
scp -i "your-key.pem" path/to/pothole_best.pt ubuntu@your-ec2-public-ip:~/AI-Traffic-Violation-Detection/models/
scp -i "your-key.pem" path/to/traffic_best.pt ubuntu@your-ec2-public-ip:~/AI-Traffic-Violation-Detection/models/
```
2. **Verify that the models exist in EC2:**
```bash
ls -lh ~/AI-Traffic-Violation-Detection/models/
```

---

### **📌 Step 7: Start Flask API & Streamlit UI**
- **Open a tmux session for Flask API:**
```bash
tmux new -s flask_server
cd ~/AI-Traffic-Violation-Detection/src
python3 routes.py
```
- **Detach the session (Ctrl+B, then D).**
- **Start another tmux session for Streamlit UI:**
```bash
tmux new -s streamlit_ui
cd ~/AI-Traffic-Violation-Detection/src
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

---

### **📌 Step 8: Configure Auto-Start on Reboot**
Run the following command:
```bash
crontab -e
```
Add these lines at the bottom:
```
@reboot tmux new -d -s flask_server 'cd ~/AI-Traffic-Violation-Detection/src && python3 routes.py'
@reboot tmux new -d -s streamlit_ui 'cd ~/AI-Traffic-Violation-Detection/src && streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0'
```
Press **Ctrl+X**, then **Y**, then **Enter** to save.

---

### **📌 Step 9: Test the Deployment**
- API should be running at:  
  **`http://your-ec2-public-ip:5000`**
- Dashboard should be accessible at:  
  **`http://your-ec2-public-ip:8501`**

---

## **📸 How to Use?**  
1️⃣ **Upload an Image or Video** via the Streamlit UI.  
2️⃣ **Select the Model Type** (`Traffic Violation` or `Pothole`).  
3️⃣ **View Results** with detections highlighted.  
4️⃣ **Check Analytics** – Live detection statistics & violation trends.  

---

## **📦 Project Structure**  
```
AI-Traffic-Violation-Detection/
│── models/                 # YOLOv8 trained models
│── src/
│   ├── inference.py        # YOLO detection functions
│   ├── routes.py           # Flask API
│   ├── dashboard.py        # Streamlit dashboard
│── static/
│   ├── uploads/            # Stores processed images & videos
│── requirements.txt        # Required dependencies
│── README.md               # Project documentation
│── .gitignore              # Ignore unnecessary files
```

---

## **Live Dashboard Features**  
🔹 **Upload images & videos for detection**  
🔹 **Track detected violations & potholes over time**  
🔹 **View recent detections with confidence scores**  
🔹 **See detected locations on an interactive map**  
🔹 **Monitor real-time detection trends**  

---

## **Future Improvements**
- **Optimize YOLOv8 models** (Hyperparameter tuning, dataset enhancement)  
- **Add Email Alerts** when violations are detected  
- **Integrate with city traffic systems**  

---
## Demo Video

**[Click here to watch the demo]https://drive.google.com/file/d/12aouwBh70zLMTTOVkT5f_VQj7GfxI9Mz/view?usp=drive_link**


**Star the repository if you like this project!**  
**Have suggestions? Feel free to open an issue!**  