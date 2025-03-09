import os
import sys
import argparse
import json
from pose_extraction import process_video
from strideanalalysis import get_data
from noLandmarks import filter_consecutive_frames, load_json

def main():
    parser = argparse.ArgumentParser(description="Process video, extract pose landmarks, and analyze strides.")
    parser.add_argument("video_path", help="Path to the input video file.")
    parser.add_argument("-o", "--output_dir", default=".", help="Directory to save output files (default: current directory).")
    parser.add_argument("-f", "--filters", default="00111", help="Smoothing filters (default: 00111).")
    args = parser.parse_args()

    video_path = args.video_path
    output_dir = args.output_dir
    filters = args.filters

    # Extract filename without extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    json_output_path = os.path.join(output_dir, f"{video_filename}.json")


    try:
        # 1. Pose landmark extraction
        frames = process_video(video_path, json_output_path, filters)

        #2. Handling missing landmarks (optional but recommended):
        frames_data = load_json(json_output_path)
        filtered_data = filter_consecutive_frames(frames_data)

        #Save filtered data to a new json file:
        filtered_json_path = os.path.join(output_dir, f"{video_filename}_filtered.json")
        with open(filtered_json_path, 'w') as f:
            json.dump(filtered_data, f, indent=4)


        # 3. Stride analysis
        step_count, peak_indices, distances = get_data(filtered_json_path)

        print(f"\nStride Analysis Results for {video_filename}:")
        print(f"Step Count: {step_count}")
        print(f"Peak Indices: {peak_indices}")
        #print(f"Distances: {distances}") #uncomment if you want to see the distances

    except FileNotFoundError:
        print(f"Error: Video file not found at {video_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
