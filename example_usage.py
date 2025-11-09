"""
Example script showing how to use the timestamp extraction functionality programmatically.
"""

from extract_timestamps import detect_objects_in_video, save_results, format_timestamp


def example_basic_usage():
    """Basic example: detect all objects in a video"""
    print("Example 1: Basic usage - detect all objects")
    print("-" * 50)
    
    video_path = "sample_video.mp4"  # Replace with your video path
    
    # Detect objects (this will download yolov8n.pt automatically on first run)
    results = detect_objects_in_video(
        video_path=video_path,
        model_path='yolov8n.pt',
        conf_threshold=0.25
    )
    
    # Save results
    save_results(results, "output_basic.json", format='json')
    
    # Print summary
    print("\nSummary:")
    for class_name, summary in results['summary'].items():
        print(f"  {class_name}: {summary['count']} detections")


def example_specific_classes():
    """Example: detect only specific classes"""
    print("\nExample 2: Detect specific classes only")
    print("-" * 50)
    
    video_path = "sample_video.mp4"  # Replace with your video path
    
    # Detect only people and cars
    results = detect_objects_in_video(
        video_path=video_path,
        model_path='yolov8n.pt',
        conf_threshold=0.3,
        target_classes=['person', 'car', 'bicycle']
    )
    
    # Save as CSV
    save_results(results, "output_specific_classes.csv", format='csv')
    
    print(f"\nDetected {sum(len(v) for v in results['detections_by_class'].values())} objects")


def example_get_timestamps_for_class():
    """Example: extract timestamps for a specific class"""
    print("\nExample 3: Get all timestamps for a specific class")
    print("-" * 50)
    
    video_path = "sample_video.mp4"  # Replace with your video path
    
    results = detect_objects_in_video(
        video_path=video_path,
        conf_threshold=0.25
    )
    
    # Get all timestamps for 'person' class
    if 'person' in results['detections_by_class']:
        person_detections = results['detections_by_class']['person']
        timestamps = [det['timestamp_formatted'] for det in person_detections]
        
        print(f"Person detected at {len(timestamps)} timestamps:")
        for i, ts in enumerate(timestamps[:10], 1):  # Show first 10
            print(f"  {i}. {ts}")
        if len(timestamps) > 10:
            print(f"  ... and {len(timestamps) - 10} more")
    else:
        print("No person detected in the video")


def example_detection_intervals():
    """Example: find time intervals where objects appear"""
    print("\nExample 4: Find detection intervals")
    print("-" * 50)
    
    video_path = "sample_video.mp4"  # Replace with your video path
    
    results = detect_objects_in_video(
        video_path=video_path,
        target_classes=['car']
    )
    
    # Group consecutive detections into intervals
    if 'car' in results['detections_by_class']:
        car_detections = results['detections_by_class']['car']
        
        if car_detections:
            intervals = []
            current_start = car_detections[0]['timestamp_seconds']
            current_end = car_detections[0]['timestamp_seconds']
            
            for det in car_detections[1:]:
                ts = det['timestamp_seconds']
                # If detection is within 1 second of previous, extend interval
                if ts - current_end <= 1.0:
                    current_end = ts
                else:
                    # Save current interval and start new one
                    intervals.append({
                        'start': format_timestamp(current_start),
                        'end': format_timestamp(current_end),
                        'duration': current_end - current_start
                    })
                    current_start = ts
                    current_end = ts
            
            # Add last interval
            intervals.append({
                'start': format_timestamp(current_start),
                'end': format_timestamp(current_end),
                'duration': current_end - current_start
            })
            
            print(f"Car detection intervals:")
            for i, interval in enumerate(intervals, 1):
                print(f"  {i}. {interval['start']} - {interval['end']} "
                      f"({interval['duration']:.1f}s)")


if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # example_basic_usage()
    # example_specific_classes()
    # example_get_timestamps_for_class()
    # example_detection_intervals()
    
    print("Please uncomment one of the example functions to run it.")
    print("Make sure to update the video_path variable with your video file path.")


