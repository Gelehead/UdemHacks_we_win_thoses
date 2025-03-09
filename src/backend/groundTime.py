import json
import argparse

# Function to check if a foot is on the ground based on z-coordinate threshold
def is_feet_on_ground(landmark, threshold=0.1):
    # Assuming z-coordinate near zero means on the ground
    return landmark['z'] < threshold

# Function to calculate ground time from pose data in JSON file
def calculate_ground_time_from_json(json_file, frame_rate=10, threshold=0.1):
    ground_time_left = 0
    ground_time_right = 0

    # Load JSON data from file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Iterate over the frames data (assuming the data contains keys like 'frame_105')
    for frame_key, landmarks in data.items():
        # Create a list of landmark indices that correspond to the feet
        left = [29, 30]
        right = [31, 32]
    
        # Check if all the feet landmarks (indices 27-32) exist and are on the ground
        left_landmarks = []
        for idx in left:
            if idx < len(landmarks):  # Ensure the index exists in the data
                left_landmarks.append(landmarks[idx])
        
        # Check if all extracted feet landmarks are on the ground
        if all(is_feet_on_ground(landmark, threshold) for landmark in left_landmarks):
            ground_time_left += 1  # Increase ground time count based on frame

        right_landmarks = []
        for idx in right:
            if idx < len(landmarks):  # Ensure the index exists in the data
                right_landmarks.append(landmarks[idx])
        
        # Check if all extracted feet landmarks are on the ground
        if all(is_feet_on_ground(landmark, threshold) for landmark in right_landmarks):
            ground_time_right += 1  # Increase ground time count based on frame

    # Convert frame count to time in seconds
    gt_rights = (ground_time_right / frame_rate)*1000
    gt_lefts = (ground_time_left / frame_rate)*1000
    return [gt_rights, gt_lefts]

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate ground time from MediaPipe pose JSON data.")
    parser.add_argument('json_file', help="Path to the JSON file containing pose landmarks data")
    return parser.parse_args()


# Main function
def main():
    # Parse arguments
    args = parse_arguments()

    # Calculate ground time from the provided JSON file
    ground_time = calculate_ground_time_from_json(args.json_file)
    
    # Output the result
    print(f"Ground time right: {ground_time[0]//10:.2f} ms")
    print(f"Ground time left: {ground_time[1]//10:.2f} ms")
    print(f"Ground time average: {(ground_time[0] + ground_time[1])/2//10:.2f} ms")


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
