# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Streamlit App

### Windows:
```bash
run_app.bat
```

### Linux/Mac:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Or directly:
```bash
streamlit run app.py
```

## Basic Usage

1. **Start the app**: Run `streamlit run app.py`
2. **Upload video**: Go to "Video Analysis" tab and upload your video
3. **Configure settings**: Adjust model, confidence, and classes in the sidebar
4. **Run detection**: Click "Start Detection" button
5. **View results**: Go to "Detection Results" tab
6. **Navigate timestamps**: 
   - Click "Show First Appearance" button for any class
   - Use the timestamp dropdown to select a specific timestamp
   - Click "Jump to Selected Timestamp" to navigate
   - Use the video player's progress bar to seek manually

## Key Features

- ✅ Video upload and playback
- ✅ Object detection with YOLO
- ✅ Timestamp extraction
- ✅ First appearance navigation
- ✅ Search and filter timestamps
- ✅ Export results (JSON/CSV)

## Tips

- Use YOLOv8 Nano for faster processing
- Lower confidence threshold to detect more objects
- Filter by specific classes for faster results
- Use video player controls to navigate to timestamps manually

## Troubleshooting

If the app doesn't start:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Try: `python -m streamlit run app.py`

If detection is slow:
- Use a smaller model (Nano)
- Filter by specific classes
- Reduce video resolution

