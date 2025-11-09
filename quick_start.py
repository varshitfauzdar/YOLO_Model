"""
Quick start script for YOLO video timestamp extraction.
This is a simplified version for quick testing.
"""

import sys
from extract_timestamps import detect_objects_in_video, save_results


def quick_start(video_path, classes=None):
    """
    Quick start function to extract timestamps from a video.
    
    Args:
        video_path: Path to the video file
        classes: List of class names to detect (None for all classes)
    """
    print("=" * 60)
    print("YOLO Video Object Timestamp Extraction - Quick Start")
    print("=" * 60)
    print(f"\nVideo: {video_path}")
    print(f"Target classes: {classes if classes else 'All classes'}")
    print("\nStarting detection...\n")
    
    try:
        # Run detection
        results = detect_objects_in_video(
            video_path=video_path,
            model_path='yolov8n.pt',  # Using nano model for speed
            conf_threshold=0.25,
            target_classes=classes
        )
        
        # Generate output filename
        import os
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file = f"{video_name}_timestamps.json"
        
        # Save results
        save_results(results, output_file, format='json')
        
        # Print summary
        print("\n" + "=" * 60)
        print("DETECTION COMPLETE")
        print("=" * 60)
        print(f"\nResults saved to: {output_file}\n")
        print("Summary by class:")
        print("-" * 60)
        
        for class_name, summary in results['summary'].items():
            print(f"{class_name.upper():<20} {summary['count']:>5} detections")
            print(f"  First: {summary['first_appearance']}")
            print(f"  Last:  {summary['last_appearance']}")
            print()
        
        total_detections = sum(len(v) for v in results['detections_by_class'].values())
        print(f"Total detections: {total_detections}")
        print("=" * 60)
        
        return results
        
    except FileNotFoundError:
        print(f"Error: Video file not found: {video_path}")
        print("Please check the file path and try again.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_start.py <video_path> [class1 class2 ...]")
        print("\nExample:")
        print("  python quick_start.py video.mp4")
        print("  python quick_start.py video.mp4 person car")
        sys.exit(1)
    
    video_path = sys.argv[1]
    classes = sys.argv[2:] if len(sys.argv) > 2 else None
    
    quick_start(video_path, classes)


