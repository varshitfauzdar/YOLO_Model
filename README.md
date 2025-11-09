# YOLO Video Object Timestamp Extraction

Detect objects in videos using YOLOv8 and extract precise timestamps when each object appears.

## Features

- 🎯 Detect objects using YOLOv8 (80+ object classes)
- ⏱️ Extract precise timestamps for each detection
- 📊 Export results in JSON or CSV format
- 🎨 Filter by specific object classes
- 🎥 Web interface (Streamlit) or command-line
- 📈 Detailed summary statistics

## Installation

```bash
pip install -r requirements.txt
```

The YOLO model (yolov8n.pt) will be automatically downloaded on first use.

## Usage

### Option 1: Web Interface (Recommended)

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

**Steps:**
1. Upload a video file (MP4, AVI, MOV, MKV, FLV, WMV)
2. Configure settings in the sidebar:
   - Select YOLO model (Nano=fastest, XLarge=most accurate)
   - Adjust confidence threshold (0.1-1.0)
   - Choose classes to detect (or detect all)
3. Click "Start Detection"
4. View results with timestamps, search, and navigation
5. Export results as JSON or CSV

**Web Interface Features:**
- Video player with playback controls
- First appearance navigation buttons
- Interactive timestamp tables with search
- Real-time detection progress
- Export individual or all timestamps

### Option 2: Command-Line

**Basic usage:**
```bash
python extract_timestamps.py --video path/to/video.mp4
```

**Advanced options:**
```bash
# Detect specific classes
python extract_timestamps.py --video video.mp4 --classes person car bicycle

# Adjust confidence threshold
python extract_timestamps.py --video video.mp4 --conf 0.5

# Use different model
python extract_timestamps.py --video video.mp4 --model yolov8s.pt

# Export as CSV
python extract_timestamps.py --video video.mp4 --format csv
```

**Available models:** `yolov8n.pt` (fastest), `yolov8s.pt`, `yolov8m.pt`, `yolov8l.pt`, `yolov8x.pt` (most accurate)

## Output Format

### JSON Output
Includes video properties, detection settings, timestamps grouped by class, and summary statistics.

```json
{
  "video_properties": {
    "fps": 30.0,
    "duration_formatted": "00:01:00.000"
  },
  "detections_by_class": {
    "person": [
      {
        "timestamp_formatted": "00:00:05.233",
        "timestamp_seconds": 5.233,
        "frame_number": 157,
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
Columns: Timestamp (seconds), Timestamp (formatted), Frame, Class, Confidence, BBox coordinates

## Supported Object Classes

YOLOv8 detects 80+ classes including: person, car, bus, truck, motorcycle, bicycle, dog, cat, bird, bottle, cup, chair, couch, bed, and many more.

## Requirements

- Python 3.8+
- CUDA-capable GPU (optional, recommended for speed)
- Sufficient RAM (depends on video resolution)

## Performance Tips

1. **Faster processing**: Use YOLOv8 Nano model + filter by specific classes
2. **Better accuracy**: Use YOLOv8 XLarge model + lower confidence threshold
3. **GPU acceleration**: Automatically used if CUDA is available
4. **Memory optimization**: Process shorter segments or reduce video resolution

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Video file not found | Check file path, use absolute paths if needed |
| Out of memory | Use smaller model (yolov8n.pt), reduce video resolution |
| Slow processing | Use GPU, smaller model, or filter by classes |
| No objects detected | Lower confidence threshold, check if video contains detectable objects |
| Video won't upload (web) | Check file format, ensure file size is reasonable |
| Can't navigate to timestamp (web) | Use video player's progress bar manually (programmatic seeking not supported) |

## Quick Start Scripts

- **Windows**: `run_app.bat`
- **Linux/Mac**: `chmod +x run_app.sh && ./run_app.sh`

## License

This project uses the Ultralytics YOLOv8 library. Please refer to their license for usage terms.
