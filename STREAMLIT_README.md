# Streamlit Web Interface for YOLO Video Object Timestamp Extraction

This Streamlit application provides a user-friendly web interface for detecting objects in videos and extracting timestamps.

## Features

- 🎥 **Video Upload**: Upload video files directly through the web interface
- 🔍 **Object Detection**: Run YOLO detection with customizable settings
- ⏱️ **Timestamp Display**: View all detection timestamps in an organized table
- 🎯 **First Appearance Navigation**: Quick buttons to jump to first/last appearance of objects
- 📊 **Interactive Tables**: Search and filter timestamps
- 📥 **Export Results**: Download detection results as JSON or CSV
- 🎨 **Modern UI**: Clean and intuitive interface

## Installation

1. Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Direct Streamlit Command
```bash
streamlit run app.py
```

### Method 2: Using Python
```bash
python -m streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Step 1: Upload Video
1. Go to the "📹 Video Analysis" tab
2. Click "Browse files" or drag and drop a video file
3. Supported formats: MP4, AVI, MOV, MKV, FLV, WMV

### Step 2: Configure Detection Settings
In the sidebar, you can:
- **Select YOLO Model**: Choose from Nano (fastest) to XLarge (most accurate)
- **Adjust Confidence Threshold**: Lower values detect more objects but may include false positives
- **Filter Classes**: Select specific object classes to detect (or detect all)

### Step 3: Run Detection
1. Click the "🔍 Start Detection" button
2. Wait for processing to complete (progress will be shown)
3. Once complete, navigate to the "📊 Detection Results" tab

### Step 4: View Results
- **Video Player**: The video is displayed at the top with playback controls
- **Video Information**: See FPS, duration, total frames, and detection count
- **Detection Summary**: Overview of all detected object classes
- **Detailed Timestamps**: View all timestamps for each object class

### Step 5: Navigate to Timestamps
- **First Appearance Button**: Click to see the first appearance timestamp
- **Jump Buttons**: Click "📍 Jump" next to any timestamp to navigate to that moment
- **Video Player**: Use the video player's seek bar to manually navigate to timestamps

### Step 6: Export Results
- Download individual class timestamps as CSV
- Download full detection results as JSON
- Download all timestamps combined as CSV

## Navigation Features

### Jump to First Appearance
1. Select an object class from the dropdown
2. Click "📍 Show First Appearance" button
3. The timestamp will be highlighted
4. Use the video player controls to navigate to that timestamp

### Navigate to Specific Timestamps
1. Scroll through the timestamp list
2. Click "📍 Jump" next to any timestamp
3. The selected timestamp will be displayed
4. Navigate to it using the video player

### Search Timestamps
- Use the search box to filter timestamps by time
- Enter a time format like "00:00:05" to find specific timestamps

## Tips

1. **For Faster Processing**: Use YOLOv8 Nano model and filter by specific classes
2. **For Better Accuracy**: Use YOLOv8 XLarge model and lower confidence threshold
3. **For Large Videos**: Processing may take time; be patient
4. **Video Navigation**: Use the video player's progress bar to seek to specific timestamps
5. **Export Data**: Download results for further analysis in Excel or other tools

## Troubleshooting

**Issue: Video won't upload**
- Check file format (must be MP4, AVI, MOV, MKV, FLV, or WMV)
- Ensure file size is not too large
- Try a different browser

**Issue: Detection is slow**
- Use a smaller YOLO model (Nano or Small)
- Filter by specific classes only
- Reduce video resolution if possible

**Issue: No objects detected**
- Lower the confidence threshold
- Select "Detect all classes" option
- Check if the video actually contains detectable objects

**Issue: Can't navigate to timestamp**
- Streamlit's video player doesn't support programmatic seeking
- Manually use the video player's progress bar to navigate
- The timestamp is displayed for your reference

## Advanced Usage

### Custom Models
You can use custom YOLO models by:
1. Placing the model file (.pt) in the project directory
2. Selecting it from the model dropdown (if it appears)
3. Or modifying the model path in the code

### Batch Processing
For batch processing multiple videos, use the command-line script:
```bash
python extract_timestamps.py --video video1.mp4
python extract_timestamps.py --video video2.mp4
```

## Performance Notes

- **GPU Acceleration**: If you have a CUDA-capable GPU, YOLO will automatically use it
- **Memory Usage**: Large videos may require significant RAM
- **Processing Time**: Depends on video length, resolution, and selected model
- **Browser Compatibility**: Works best in Chrome, Firefox, or Edge

## Support

For issues or questions, please refer to the main README.md file or check the YOLOv8 documentation.

