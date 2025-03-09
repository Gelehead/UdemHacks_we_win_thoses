import os
import json
from pose_extraction import process_video
from strideanalalysis import get_data
from noLandmarks import filter_consecutive_frames, load_json
import time
import numpy as np


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
        json_output_path = os.path.join(output_dir, "json", f"{video_filename}.json")
        video_output_path = os.path.join(output_dir, "videos", f"{video_filename}.json")

        print("")
        print("bbbbbbbbbbbbbbbbb")
        print("")

        # 1. Pose landmark extraction
        process_video(video_path, video_output_path, "00111")  # Using default filters

        # 2. Handling missing landmarks
        frames_data = load_json(json_output_path)
        filtered_data = filter_consecutive_frames(frames_data)

        # Save filtered data to a new JSON file
        filtered_json_path = os.path.join(output_dir, f"{video_filename}_filtered.json")
        with open(filtered_json_path, 'w') as f:
            json.dump(filtered_data, f, indent=4)
            

        # 3. Stride analysis
        step_count, peak_indices, distances = get_data(filtered_json_path)

        results = {
            "step_count": step_count,
            "peak_indices": peak_indices.tolist() if isinstance(peak_indices, np.ndarray) else peak_indices,
            "distances": distances.tolist() if isinstance(distances, np.ndarray) else distances,
            "filtered_data": filtered_data.tolist() if isinstance(filtered_data, np.ndarray) else filtered_data
        }
        
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "out", "json", "results.json")
        with open("results.json", "w") as json_file:
            json.dump(results, json_file, indent=4)

        return results

    except FileNotFoundError:
        print(f"Error: Video file not found at {video_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


