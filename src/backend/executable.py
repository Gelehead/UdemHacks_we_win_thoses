import os
import json
from pose_extraction import process_video
from strideanalalysis import get_data
from noLandmarks import filter_consecutive_frames, load_json
import time
import numpy as np
import cv2

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def create_video_from_frames(frames_list, output_path, fps=30):
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

def analyze_video(video_path, output_dir="."):
    """
    Analyzes a video to extract pose landmarks, handle missing landmarks, and perform stride analysis.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str, optional): Directory to save output files. Defaults to ".".

    Returns:
        dict: A dictionary containing the stride analysis results, or None if an error occurred.
                The dictionary will have the following keys:
                    - "step_count": The number of steps detected.
                    - "peak_indices": A list of indices representing the peak positions.
                    - "distances": A list of distances between certain keypoints in each stride.
                    - "animation_path": Path to the animation video.
    """
    try:
        # Extract filename without extension
        video_filename = os.path.splitext(os.path.basename(video_path))[0]
        
        # Create json directory if it doesn't exist
        json_dir = os.path.join(output_dir, "json")
        animations_dir = os.path.join(output_dir, "animations")
        
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        if not os.path.exists(animations_dir):
            os.makedirs(animations_dir)
            
        # Temporary path for intermediate processing
        temp_output_path = os.path.join(json_dir, f"{video_filename}_temp_data.json")

        print("")
        print("Starting pose landmark extraction...")
        print("")

        # 1. Pose landmark extraction 
        # Modified to capture the black_frames that are already created
        drawn_frames, pose_data = process_video(video_path, temp_output_path, "00111", return_frames=True)
        
        print("")
        print("Pose extraction complete. Creating animation...")
        print("")

        # Create animation video from the drawn frames
        animation_path = os.path.join(animations_dir, f"{video_filename}_animation.mp4")
        if drawn_frames and len(drawn_frames) > 0:
            create_video_from_frames(drawn_frames, animation_path)
        else:
            print("No drawn frames were returned from pose extraction.")
        
        # 2. Handling missing landmarks
        print("Processing landmark data...")
        frames_data = load_json(temp_output_path)
        filtered_data = filter_consecutive_frames(frames_data)
            
        print("")
        print("Performing stride analysis...")
        print("")

        # 3. Stride analysis - use the in-memory filtered data
        # Create a temporary file for stride analysis if needed by get_data
        temp_filtered_path = os.path.join(json_dir, f"{video_filename}_temp.json")
        with open(temp_filtered_path, 'w') as f:
            json.dump(filtered_data, f, indent=4)
            
        step_count, peak_indices, distances = get_data(temp_filtered_path)
        
        # Clean up the temporary files
        if os.path.exists(temp_filtered_path):
            os.remove(temp_filtered_path)
        
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        # Convert numpy types to standard Python types for JSON serialization
        if isinstance(step_count, np.integer):
            step_count = int(step_count)
        
        results = {
            "step_count": step_count,
            "peak_indices": peak_indices.tolist() if isinstance(peak_indices, np.ndarray) else peak_indices,
            "distances": distances.tolist() if isinstance(distances, np.ndarray) else distances,
            "animation_path": animation_path
        }
        
        # Save results with the same name as the video file
        results_path = os.path.join(json_dir, f"{video_filename}.json")
        with open(results_path, "w") as json_file:
            json.dump(results, json_file, cls=NumpyEncoder, indent=4)

        # Convert results to JSON-compatible format for return
        return json.loads(json.dumps(results, cls=NumpyEncoder))

    except FileNotFoundError as e:
        print(f"Error: Video file not found at {video_path}")
        print(f"Exception details: {str(e)}")
        return {"error": f"Video file not found at {video_path}"}
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}