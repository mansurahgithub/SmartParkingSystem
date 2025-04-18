
# Parking Space Detection System

A computer vision system that detects available parking spaces in real-time and provides an interactive map interface for visualization.

## Project Overview

This system combines computer vision techniques with mapping capabilities to:
- Detect and monitor parking spaces in video feeds
- Track parking space occupancy in real-time
- Display results on an interactive web-based map
- Calculate distances to available parking spaces

## Project Structure

```
├── ParkingSpace.py       # Core parking space detection logic ( in the uploaded files section, you will find 3 such files because i implemented it for 3 videos)
├── interactive_map.py    # Map interface implementation
├── main_with_interactive.py # Main application entry point
├── requirements.txt     # Project dependencies
├── carPark.mp4         # Sample video feed ( you will find 3 such video files in the uplaoded section, because i used 3 sample videos)
└── interactive_parking_map.html  # Generated map interface
```

## Setup Instructions

1. Set up Python virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare video source:
   - Place your parking lot video file (e.g., `carPark.mp4`) in the project directory
   - Or configure webcam input in the main script

4. Run the application:
   ```bash
   python main_with_interactive.py
   ```

## Features

### Parking Space Detection
- Real-time video processing
- Automatic space occupancy detection
- Support for multiple parking areas
- Configurable detection parameters

### Interactive Map
- Web-based visualization
- Real-time updates of space availability
- Color-coded parking space markers
- Distance calculation to available spaces

### Data Management
- JSON-based storage of space counts
- Configurable parking location coordinates
- Support for multiple parking areas

## Dependencies

- OpenCV (cv2)
- NumPy
- Folium (for map visualization)
- Python 3.x

## Usage Tips

1. **Configuring Parking Spaces**:
   - Use the provided scripts to define parking space coordinates
   - Adjust detection parameters in ParkingSpace.py

2. **Map Interface**:
   - Access the interactive map through generated HTML file
   - Markers update automatically with space availability
   - Click markers for detailed information

3. **Performance Optimization**:
   - Adjust video resolution as needed
   - Configure detection frequency
   - Optimize space coordinates for accuracy

Output Screenshots : 
The three parking area locations are plotted in the gmap interface, the user's location is represented as " i " 
![WhatsApp Image 2025-04-17 at 20 24 47_9fdf3e14](https://github.com/user-attachments/assets/b7261584-8550-4834-8100-0d4e1994a4ed)
![WhatsApp Image 2025-04-17 at 20 25 00_d512d818](https://github.com/user-attachments/assets/0a7bb8cc-f619-4c9f-a395-8e91a23f8d94)
![WhatsApp Image 2025-04-17 at 20 25 28_12c715ab](https://github.com/user-attachments/assets/f60600d8-5f6d-465c-8e69-3fb6ccc27bf9)
Video 1 : ![WhatsApp Image 2025-04-17 at 20 17 43_1095ed16](https://github.com/user-attachments/assets/09710b2e-7086-4f69-87d8-3f31734c0a98)
Video 2 : ![WhatsApp Image 2025-04-17 at 20 17 44_9f99f529](https://github.com/user-attachments/assets/4fdcb2a8-2422-40c1-9c28-1ca0b8eb51ba)
Video 3 : ![WhatsApp Image 2025-04-17 at 20 17 44_f0cfbe8e](https://github.com/user-attachments/assets/08f1235b-f892-4912-ae10-56bce0461480)

Acknowledgement : Murtaza's Workshop. Learnt the Parking Space Detection logic with his youtube video. 
