import streamlit as st
import json
import os
import tempfile
from extract_timestamps import detect_objects_in_video, save_results
import pandas as pd
from collections import defaultdict


# Page configuration
st.set_page_config(
    page_title="YOLO Video Object Timestamp Extractor",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .timestamp-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .detection-summary {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_detection_results(json_path):
    """Load detection results from JSON file"""
    with open(json_path, 'r') as f:
        return json.load(f)


def format_timestamp_display(seconds):
    """Format timestamp for display"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 60 - secs) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def main():
    # Header
    st.markdown('<h1 class="main-header">🎥 YOLO Video Object Timestamp Extractor</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_options = {
            "YOLOv8 Nano (Fastest)": "yolov8n.pt",
            "YOLOv8 Small": "yolov8s.pt",
            "YOLOv8 Medium": "yolov8m.pt",
            "YOLOv8 Large": "yolov8l.pt",
            "YOLOv8 XLarge (Most Accurate)": "yolov8x.pt"
        }
        selected_model = st.selectbox(
            "Select YOLO Model",
            options=list(model_options.keys()),
            index=0
        )
        model_path = model_options[selected_model]
        
        # Confidence threshold
        conf_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.25,
            step=0.05,
            help="Lower values detect more objects but may include false positives"
        )
        
        # Class filtering
        st.subheader("Class Filtering")
        detect_all = st.checkbox("Detect all classes", value=True)
        
        common_classes = [
            "person", "car", "truck", "bus", "motorcycle", "bicycle",
            "dog", "cat", "bird", "horse", "sheep", "cow",
            "bottle", "cup", "bowl", "chair", "couch", "bed"
        ]
        
        selected_classes = None
        if not detect_all:
            selected_classes = st.multiselect(
                "Select classes to detect",
                options=common_classes,
                default=["person", "car"]
            )
            if not selected_classes:
                st.warning("Please select at least one class")
                selected_classes = None
    
    # Main content area
    tab1, tab2 = st.tabs(["📹 Video Analysis", "📊 Detection Results"])
    
    with tab1:
        st.header("Upload and Analyze Video")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'],
            help="Upload a video file to analyze"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            video_bytes = uploaded_file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(video_bytes)
                video_path = tmp_file.name
                video_name = os.path.splitext(uploaded_file.name)[0]
            
            # Store video data in session state
            st.session_state.video_path = video_path
            st.session_state.video_name = video_name
            st.session_state.video_bytes = video_bytes
            
            # Display video
            st.subheader("📺 Video Player")
            st.video(video_bytes)
            
            # Detection button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Start Detection", type="primary", use_container_width=True):
                    with st.spinner("Processing video... This may take a while..."):
                        try:
                            # Run detection
                            results = detect_objects_in_video(
                                video_path=video_path,
                                model_path=model_path,
                                conf_threshold=conf_threshold,
                                target_classes=selected_classes
                            )
                            
                            # Save results to session state
                            st.session_state.detection_results = results
                            
                            # Save to file
                            output_file = f"{video_name}_timestamps.json"
                            save_results(results, output_file, format='json')
                            st.session_state.output_file = output_file
                            
                            st.success("✅ Detection complete! Check the 'Detection Results' tab.")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error during detection: {str(e)}")
            
            # Load existing results if available
            if 'detection_results' not in st.session_state:
                st.info("👆 Click 'Start Detection' to analyze the video and extract object timestamps.")
            else:
                st.success("✅ Detection results are available! Check the 'Detection Results' tab.")
        
        else:
            st.info("👆 Please upload a video file to get started.")
    
    with tab2:
        st.header("Detection Results & Timestamps")
        
        # Check if results exist
        if 'detection_results' not in st.session_state:
            st.warning("⚠️ No detection results available. Please upload a video and run detection in the 'Video Analysis' tab.")
        else:
            results = st.session_state.detection_results
            
            # Display video with controls
            if 'video_bytes' in st.session_state:
                st.subheader("📺 Video Player with Timestamp Navigation")
                st.video(st.session_state.video_bytes)
            
            # Video information
            st.subheader("📋 Video Information")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("FPS", f"{results['video_properties']['fps']:.2f}")
            with col2:
                st.metric("Total Frames", results['video_properties']['total_frames'])
            with col3:
                st.metric("Duration", results['video_properties']['duration_formatted'])
            with col4:
                total_detections = sum(len(v) for v in results['detections_by_class'].values())
                st.metric("Total Detections", total_detections)
            
            # Detection settings
            with st.expander("🔧 Detection Settings", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Model:** {results['detection_settings']['model']}")
                with col2:
                    st.write(f"**Confidence Threshold:** {results['detection_settings']['confidence_threshold']}")
                with col3:
                    st.write(f"**Target Classes:** {results['detection_settings']['target_classes']}")
            
            # Summary statistics
            st.subheader("📊 Detection Summary by Class")
            
            if results['summary']:
                # Create summary DataFrame
                summary_data = []
                for class_name, summary in results['summary'].items():
                    summary_data.append({
                        'Class': class_name.title(),
                        'Total Detections': summary['count'],
                        'First Appearance': summary['first_appearance'],
                        'Last Appearance': summary['last_appearance']
                    })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
            else:
                st.info("No objects detected in the video.")
            
            # Detailed timestamps by class
            st.subheader("⏱️ Detailed Timestamps")
            
            # Class selector
            detected_classes = list(results['detections_by_class'].keys())
            if detected_classes:
                selected_class_view = st.selectbox(
                    "Select class to view timestamps",
                    options=detected_classes,
                    index=0
                )
                
                # Get detections for selected class
                class_detections = results['detections_by_class'][selected_class_view]
                
                if class_detections:
                    # Display first appearance button
                    first_appearance = class_detections[0]['timestamp_formatted']
                    first_appearance_seconds = class_detections[0]['timestamp_seconds']
                    last_appearance = class_detections[-1]['timestamp_formatted']
                    last_appearance_seconds = class_detections[-1]['timestamp_seconds']
                    
                    st.markdown(f"### 🎯 {selected_class_view.title()} Detections")
                    
                    # First appearance navigation
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"""
                        <div class="detection-summary">
                            <strong>First Appearance:</strong> {first_appearance}<br>
                            <strong>Last Appearance:</strong> {last_appearance}<br>
                            <strong>Total Detections:</strong> {len(class_detections)}
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown("### ⏱️ Jump to Timestamp")
                        st.markdown(f"**First:** `{first_appearance}`")
                        st.markdown(f"**Seconds:** `{first_appearance_seconds:.3f}s`")
                    with col3:
                        st.markdown("### 📍 Navigation")
                        st.info("💡 **Tip:** Use the video player's seek bar to jump to the timestamp above. Click on the progress bar and drag to navigate.")
                    
                    # Highlight first appearance
                    st.success(f"🎯 **First Appearance of {selected_class_view.title()}:** {first_appearance} ({first_appearance_seconds:.3f} seconds)")
                    
                    # Quick navigation buttons for first and last appearance
                    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])
                    with nav_col1:
                        if st.button(f"📍 Show First Appearance ({first_appearance})", key=f"first_{selected_class_view}"):
                            st.session_state.selected_timestamp = first_appearance_seconds
                            st.info(f"Navigate to: {first_appearance} in the video player above")
                    with nav_col2:
                        if st.button(f"📍 Show Last Appearance ({last_appearance})", key=f"last_{selected_class_view}"):
                            st.session_state.selected_timestamp = last_appearance_seconds
                            st.info(f"Navigate to: {last_appearance} in the video player above")
                    
                    # Show selected timestamp if set
                    if 'selected_timestamp' in st.session_state:
                        selected_ts = st.session_state.selected_timestamp
                        formatted_ts = format_timestamp_display(selected_ts)
                        st.warning(f"🎯 Navigate to timestamp: **{formatted_ts}** ({selected_ts:.3f} seconds) in the video player above")
                    
                    # Create DataFrame for detections
                    detections_data = []
                    for idx, det in enumerate(class_detections):
                        detections_data.append({
                            'Timestamp': det['timestamp_formatted'],
                            'Seconds': det['timestamp_seconds'],
                            'Frame': det['frame_number'],
                            'Confidence': f"{det['confidence']:.3f}",
                            'BBox': f"({det['bbox']['x1']:.0f},{det['bbox']['y1']:.0f},{det['bbox']['x2']:.0f},{det['bbox']['y2']:.0f})"
                        })
                    
                    detections_df = pd.DataFrame(detections_data)
                    
                    # Search functionality
                    search_term = st.text_input("🔍 Search timestamps", key=f"search_{selected_class_view}", placeholder="Search by timestamp (e.g., 00:00:05)...")
                    
                    # Filter dataframe if search term exists
                    if search_term:
                        filtered_df = detections_df[detections_df['Timestamp'].str.contains(search_term, case=False)]
                    else:
                        filtered_df = detections_df
                    
                    # Display timestamps in a scrollable format with clickable buttons
                    st.markdown("### 📋 All Timestamps (Click to Navigate)")
                    
                    # Pagination
                    items_per_page = 20
                    total_pages = (len(filtered_df) + items_per_page - 1) // items_per_page
                    
                    if total_pages > 1:
                        page_num = st.number_input(f"Page (1-{total_pages})", min_value=1, max_value=total_pages, value=1, key=f"page_{selected_class_view}")
                        start_idx = (page_num - 1) * items_per_page
                        end_idx = start_idx + items_per_page
                        page_df = filtered_df.iloc[start_idx:end_idx]
                    else:
                        page_num = 1
                        page_df = filtered_df
                    
                    # Display timestamps with navigation buttons
                    # Use a more efficient approach for many timestamps
                    if len(page_df) > 0:
                        # Create a selectbox for quick navigation
                        timestamp_options = [f"{row['Timestamp']} (Conf: {row['Confidence']})" for _, row in page_df.iterrows()]
                        selected_timestamp_idx = st.selectbox(
                            "Select timestamp to navigate to:",
                            options=range(len(timestamp_options)),
                            format_func=lambda x: timestamp_options[x],
                            key=f"timestamp_select_{selected_class_view}_{page_num}"
                        )
                        
                        if st.button("📍 Jump to Selected Timestamp", key=f"jump_btn_{selected_class_view}_{page_num}"):
                            selected_row = page_df.iloc[selected_timestamp_idx]
                            st.session_state.selected_timestamp = selected_row['Seconds']
                            st.session_state.selected_timestamp_label = selected_row['Timestamp']
                            st.rerun()
                        
                        st.divider()
                        
                        # Display all timestamps in the current page
                        for idx, (_, row) in enumerate(page_df.iterrows()):
                            timestamp = row['Timestamp']
                            seconds = row['Seconds']
                            confidence = row['Confidence']
                            frame = row['Frame']
                            
                            # Highlight selected timestamp
                            is_selected = (idx == selected_timestamp_idx)
                            highlight_style = "background-color: #e8f4f8; padding: 0.5rem; border-radius: 0.25rem;" if is_selected else ""
                            
                            col1, col2, col3 = st.columns([4, 1, 1])
                            with col1:
                                st.markdown(f"<div style='{highlight_style}'><strong>{timestamp}</strong> (Frame: {frame})</div>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"Conf: {confidence}")
                            with col3:
                                st.markdown(f"`{seconds:.3f}s`")
                            
                            if idx < len(page_df) - 1:
                                st.divider()
                    
                    # Show selected timestamp
                    if 'selected_timestamp' in st.session_state:
                        selected_ts = st.session_state.selected_timestamp
                        selected_label = st.session_state.get('selected_timestamp_label', format_timestamp_display(selected_ts))
                        st.success(f"🎯 **Selected Timestamp:** {selected_label} ({selected_ts:.3f} seconds) - Use the video player controls above to navigate to this time")
                    
                    # Display full dataframe view (collapsed)
                    with st.expander("📊 View Full Timestamp Table"):
                        st.dataframe(
                            filtered_df.style.format({'Seconds': '{:.3f}'}), 
                            use_container_width=True, 
                            hide_index=True
                        )
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Timestamps (CSV)",
                        data=detections_df.to_csv(index=False),
                        file_name=f"{st.session_state.video_name}_{selected_class_view}_timestamps.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(f"No detections found for {selected_class_view}.")
            else:
                st.info("No objects detected. Try lowering the confidence threshold or selecting different classes.")
            
            # Download full results
            st.subheader("💾 Download Results")
            col1, col2 = st.columns(2)
            with col1:
                if 'output_file' in st.session_state and os.path.exists(st.session_state.output_file):
                    with open(st.session_state.output_file, 'r') as f:
                        st.download_button(
                            label="📥 Download Full Results (JSON)",
                            data=f.read(),
                            file_name=st.session_state.output_file,
                            mime="application/json"
                        )
            
            # Show all classes at once option
            with st.expander("📋 View All Timestamps (All Classes)", expanded=False):
                all_detections_data = []
                for class_name, detections_list in results['detections_by_class'].items():
                    for det in detections_list:
                        all_detections_data.append({
                            'Class': class_name.title(),
                            'Timestamp': det['timestamp_formatted'],
                            'Seconds': f"{det['timestamp_seconds']:.3f}",
                            'Frame': det['frame_number'],
                            'Confidence': f"{det['confidence']:.3f}"
                        })
                
                if all_detections_data:
                    all_df = pd.DataFrame(all_detections_data)
                    st.dataframe(all_df, use_container_width=True, hide_index=True)
                    
                    st.download_button(
                        label="📥 Download All Timestamps (CSV)",
                        data=all_df.to_csv(index=False),
                        file_name=f"{st.session_state.video_name}_all_timestamps.csv",
                        mime="text/csv"
                    )


if __name__ == "__main__":
    main()

