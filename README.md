# YOLO Video Object Timestamp Extraction

This project uses YOLO (You Only Look Once) to detect objects in videos and extract timestamps when each object appears.

## Features

- 🎯 Detect objects in video using YOLOv8
- ⏱️ Extract precise timestamps for each detection
- 📊 Export results in JSON or CSV format
- 🎨 Support for filtering specific object classes
- 📈 Detailed summary statistics

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The YOLO model will be automatically downloaded on first use (default: yolov8n.pt)

## Usage

### Basic Usage

Detect all objects in a video:
```bash
python extract_timestamps.py --video path/to/your/video.mp4
```

### Advanced Usage

**Detect specific classes only:**
```bash
python extract_timestamps.py --video video.mp4 --classes person car bicycle
```

**Adjust confidence threshold:**
```bash
python extract_timestamps.py --video video.mp4 --conf 0.5
```

**Use a different YOLO model:**
```bash
python extract_timestamps.py --video video.mp4 --model yolov8s.pt
```

## Output Format

### JSON Output

The JSON output includes:
- Video properties (FPS, duration, total frames)
- Detection settings (model, confidence threshold, target classes)
- Detections grouped by class with timestamps
- Summary statistics (count, first/last appearance)

Example JSON structure:
```json
{
  "video_path": "video.mp4",
  "video_properties": {
    "fps": 30.0,
    "total_frames": 1800,
    "duration_seconds": 60.0,
    "duration_formatted": "00:01:00.000"
  },
  "detections_by_class": {
    "person": [
      {
        "timestamp_seconds": 5.233,
        "timestamp_formatted": "00:00:05.233",
        "frame_number": 157,
        "class_name": "person",
        "confidence": 0.85,
        "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 500}
      }
    ]
  },
  "summary": {
    "person": {
      "count": 45,
      "first_appearance": "00:00:05.233",
      "last_appearance": "00:00:58.567"
    }
  }
}
```

### CSV Output

CSV format includes columns:
- Timestamp (seconds)
- Timestamp (formatted)
- Frame
- Class
- Confidence
- X1, Y1, X2, Y2 (bounding box coordinates)

## Supported Object Classes

YOLOv8 can detect 80 different object classes including:
- person
- car, bus, truck, motorcycle, bicycle
- dog, cat, bird
- bottle, cup, bowl
- chair, couch, bed
- And many more...

See the full list in the YOLOv8 documentation.

## Requirements

- Python 3.8+
- CUDA-capable GPU (optional, but recommended for faster processing)
- Sufficient RAM (depends on video resolution)

## Performance Tips

1. **Use a smaller model** (yolov8n.pt) for faster processing
2. **Filter by specific classes** to reduce processing time
3. **Adjust confidence threshold** - lower values detect more objects but may include false positives
4. **Use GPU** if available - YOLO will automatically use CUDA if PyTorch is installed with CUDA support

## Troubleshooting

**Issue: Video file not found**
- Make sure the video path is correct
- Use absolute paths if relative paths don't work

**Issue: Out of memory**
- Use a smaller YOLO model (yolov8n.pt)
- Process shorter video segments
- Reduce video resolution

**Issue: Slow processing**
- Use GPU acceleration
- Use a smaller model
- Filter by specific classes only

## Web Interface (Streamlit)

A user-friendly web interface is available for easy video analysis:

```bash
streamlit run app.py
```

### Features:
- 🎥 Upload videos through the web interface
- 🔍 Configure detection settings in the sidebar
- ⏱️ View timestamps in an interactive table
- 🎯 Jump to first appearance of objects
- 📊 Search and filter timestamps
- 📥 Export results as JSON or CSV

See [STREAMLIT_README.md](STREAMLIT_README.md) for detailed usage instructions.

## License

This project uses the Ultralytics YOLOv8 library. Please refer to their license for usage terms.

