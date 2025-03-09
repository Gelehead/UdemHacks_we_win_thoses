import os
import json
from pose_extraction import process_video
from strideanalalysis import get_data
from noLandmarks import filter_consecutive_frames, load_json
import time
import numpy as np

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
                    - "json_path": Path to the filtered json path.
    """
    try:
        # Extract filename without extension
        video_filename = os.path.splitext(os.path.basename(video_path))[0]
        
        # Create json and videos directory if they don't exist
        json_dir = os.path.join(output_dir, "json")
        videos_dir = os.path.join(output_dir, "videos")
        
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
            
        json_output_path = os.path.join(json_dir, f"{video_filename}.json")
        video_output_path = os.path.join(videos_dir, f"{video_filename}.mp4")  # Changed extension to mp4 for videos

        print("")
        print("bbbbbbbbbbbbbbbbb")
        print("")

        # 1. Pose landmark extraction
        process_video(video_path, json_output_path, "00111")  # Changed to json_output_path
        
        print("")
        print("cccccccccccccccc")
        print("")

        # 2. Handling missing landmarks
        frames_data = load_json(json_output_path)
        filtered_data = filter_consecutive_frames(frames_data)

        # Save filtered data to a new JSON file
        filtered_json_path = os.path.join(json_dir, f"{video_filename}_filtered.json")
        with open(filtered_json_path, 'w') as f:
            json.dump(filtered_data, f, indent=4)
            
        print("")
        print("dddddddddddddddd")
        print("")

        # 3. Stride analysis
        step_count, peak_indices, distances = get_data(filtered_json_path)

        # Convert numpy types to standard Python types for JSON serialization
        if isinstance(step_count, np.integer):
            step_count = int(step_count)
        
        results = {
            "step_count": step_count,
            "peak_indices": peak_indices.tolist() if isinstance(peak_indices, np.ndarray) else peak_indices,
            "distances": distances.tolist() if isinstance(distances, np.ndarray) else distances,
            "filtered_json_path": filtered_json_path
        }
        
        results_path = os.path.join(json_dir, "results.json")
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
        return {"error": str(e)}