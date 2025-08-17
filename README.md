Overview
This project detects traffic control types at different intersections using computer vision and machine learning. The system takes intersection coordinates (latitude and longitude), retrieves four directional street view images, and uses a fine-tuned YOLOv8 model to identify traffic control devices.
Features

Automated Image Collection: Retrieves four heading images (North, South, East, West) from Google Street View API for any intersection
Traffic Control Detection: Uses a custom-trained YOLOv8 model to detect traffic lights and other control devices
Batch Processing: Process multiple intersections efficiently
Comprehensive Results: Provides detection confidence scores and bounding box coordinates

