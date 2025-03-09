def create_video_from_frames(frames_list, output_path, fps=10):
    """
    Creates a video from a list of already processed frames.
    
    Args:
        frames_list: List of image frames (numpy arrays)
        output_path: Path to save the output MP4 video
        fps: Frames per second for the output video
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not frames_list or len(frames_list) == 0:
        print("Error: No frames provided")
        return False
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Get dimensions from the first frame
    height, width = frames_list[0].shape[:2]
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Check if VideoWriter was successfully created
    if not out.isOpened():
        print(f"Error: Could not create output video at {output_path}")
        return False
    
    print(f"Creating video with {len(frames_list)} frames...")
    
    # Write each frame to the video
    for i, frame in enumerate(frames_list):
        out.write(frame)
        
        # Show progress
        if i % 10 == 0:
            print(f"Processing frame {i}/{len(frames_list)}", end='\r')
    
    # Release the video writer
    out.release()
    print(f"\nVideo saved to {output_path}")
    return True