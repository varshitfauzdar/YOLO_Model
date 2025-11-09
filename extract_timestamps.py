import cv2
from ultralytics import YOLO
import json
from datetime import timedelta
from collections import defaultdict
import argparse
import os


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS.mmm format"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def detect_objects_in_video(video_path, model_path='yolov8n.pt', conf_threshold=0.25, 
                           target_classes=None, output_format='json'):
    """
    Detect objects in a video and extract timestamps.
    
    Args:
        video_path: Path to the input video file
        model_path: Path to YOLO model weights (default: yolov8n.pt)
        conf_threshold: Confidence threshold for detections (default: 0.25)
        target_classes: List of class names to track (None = all classes)
        output_format: Output format - 'json' or 'csv' (default: 'json')
    
    Returns:
        Dictionary containing detection results with timestamps
    """
    
    # Load YOLO model
    print(f"Loading YOLO model: {model_path}")
    model = YOLO(model_path)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file {video_path}")
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video FPS: {fps:.2f}")
    print(f"Total frames: {total_frames}")
    print(f"Video duration: {format_timestamp(video_duration)}")
    print(f"Processing video...")
    
    # Store detection results
    detections = defaultdict(list)
    frame_number = 0
    
    # Process video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate timestamp for current frame
        timestamp_seconds = frame_number / fps if fps > 0 else 0
        timestamp_formatted = format_timestamp(timestamp_seconds)
        
        # Run YOLO detection
        results = model(frame, conf=conf_threshold, verbose=False)
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class name and confidence
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                
                # Filter by target classes if specified
                if target_classes is not None and class_name not in target_classes:
                    continue
                
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Store detection
                detection = {
                    'timestamp_seconds': round(timestamp_seconds, 3),
                    'timestamp_formatted': timestamp_formatted,
                    'frame_number': frame_number,
                    'class_name': class_name,
                    'class_id': class_id,
                    'confidence': round(confidence, 3),
                    'bbox': {
                        'x1': round(float(x1), 2),
                        'y1': round(float(y1), 2),
                        'x2': round(float(x2), 2),
                        'y2': round(float(y2), 2)
                    }
                }
                
                detections[class_name].append(detection)
        
        frame_number += 1
        
        # Progress update every 100 frames
        if frame_number % 100 == 0:
            progress = (frame_number / total_frames) * 100
            print(f"Progress: {progress:.1f}% ({frame_number}/{total_frames} frames)")
    
    cap.release()
    print(f"Processing complete! Detected {sum(len(v) for v in detections.values())} objects")
    
    # Prepare output data
    output_data = {
        'video_path': video_path,
        'video_properties': {
            'fps': round(fps, 2),
            'total_frames': total_frames,
            'duration_seconds': round(video_duration, 3),
            'duration_formatted': format_timestamp(video_duration)
        },
        'detection_settings': {
            'model': model_path,
            'confidence_threshold': conf_threshold,
            'target_classes': target_classes if target_classes else 'all classes'
        },
        'detections_by_class': dict(detections),
        'summary': {
            class_name: {
                'count': len(detections_list),
                'first_appearance': detections_list[0]['timestamp_formatted'] if detections_list else None,
                'last_appearance': detections_list[-1]['timestamp_formatted'] if detections_list else None
            }
            for class_name, detections_list in detections.items()
        }
    }
    
    return output_data


def save_results(data, output_path, format='json'):
    """Save detection results to file"""
    if format.lower() == 'json':
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Results saved to: {output_path}")
    
    elif format.lower() == 'csv':
        import csv
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Timestamp (seconds)', 'Timestamp (formatted)', 'Frame', 
                           'Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])
            
            # Write detections
            for class_name, detections_list in data['detections_by_class'].items():
                for det in detections_list:
                    writer.writerow([
                        det['timestamp_seconds'],
                        det['timestamp_formatted'],
                        det['frame_number'],
                        det['class_name'],
                        det['confidence'],
                        det['bbox']['x1'],
                        det['bbox']['y1'],
                        det['bbox']['x2'],
                        det['bbox']['y2']
                    ])
        print(f"Results saved to: {output_path}")
    
    else:
        raise ValueError(f"Unsupported output format: {format}")


def main():
    parser = argparse.ArgumentParser(description='Extract object timestamps from video using YOLO')
    parser.add_argument('--video', type=str, required=True, help='Path to input video file')
    parser.add_argument('--model', type=str, default='yolov8n.pt', 
                       help='Path to YOLO model weights (default: yolov8n.pt)')
    parser.add_argument('--conf', type=float, default=0.25, 
                       help='Confidence threshold (default: 0.25)')
    parser.add_argument('--classes', type=str, nargs='+', default=None,
                       help='Target classes to detect (e.g., person car). If not specified, detects all classes')
    parser.add_argument('--output', type=str, default=None,
                       help='Output file path (default: video_name_timestamps.json)')
    parser.add_argument('--format', type=str, choices=['json', 'csv'], default='json',
                       help='Output format: json or csv (default: json)')
    
    args = parser.parse_args()
    
    # Validate video file
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        return
    
    # Set output path
    if args.output is None:
        video_name = os.path.splitext(os.path.basename(args.video))[0]
        ext = 'json' if args.format == 'json' else 'csv'
        args.output = f"{video_name}_timestamps.{ext}"
    
    # Run detection
    try:
        results = detect_objects_in_video(
            video_path=args.video,
            model_path=args.model,
            conf_threshold=args.conf,
            target_classes=args.classes,
            output_format=args.format
        )
        
        # Save results
        save_results(results, args.output, format=args.format)
        
        # Print summary
        print("\n" + "="*50)
        print("DETECTION SUMMARY")
        print("="*50)
        for class_name, summary in results['summary'].items():
            print(f"\n{class_name.upper()}:")
            print(f"  Total detections: {summary['count']}")
            print(f"  First appearance: {summary['first_appearance']}")
            print(f"  Last appearance: {summary['last_appearance']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

