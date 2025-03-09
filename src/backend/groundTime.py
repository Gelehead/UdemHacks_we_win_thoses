import json
import argparse

<<<<<<< Updated upstream
# Function to check if a foot is on the ground based on y-coordinate threshold
def is_feet_on_ground(landmark, threshold=0.01):
    # Assuming y-coordinate near zero means on the ground
    return abs(landmark.get('y', 0)) < threshold  # Use absolute value and default to 0 if 'y' is missing

# Function to calculate ground time from pose data in JSON file
def calculate_ground_time_from_json(json_file, frame_rate=10, threshold=0.01):
    ground_time_frames = 0
=======
# Function to check if a foot is on the ground based on z-coordinate threshold
def is_feet_on_ground(landmark, threshold=0.1):
    # Assuming z-coordinate near zero means on the ground
    return landmark['z'] < threshold

# Function to calculate ground time from pose data in JSON file
def calculate_ground_time_from_json(json_file, frame_rate=10, threshold=0.1):
    ground_time_left = 0
    ground_time_right = 0
>>>>>>> Stashed changes

    # Load JSON data from file
    with open(json_file, 'r') as f:
        data = json.load(f)

<<<<<<< Updated upstream
    # Iterate over the frames data (assuming the data is a list of frames)
    for frame in data:
        # Create a list of landmark indices that correspond to the feet
        feet_landmarks_indices = [29, 30, 31, 32]  # MediaPipe foot landmarks

        # Extract foot landmarks
        feet_landmarks = []
        for idx in feet_landmarks_indices:
            if idx < len(frame):  # Ensure the index exists in the frame
                feet_landmarks.append(frame[idx])

        # Check if all extracted foot landmarks are on the ground
        if all(is_feet_on_ground(landmark, threshold) for landmark in feet_landmarks):
            ground_time_frames += 1  # Increase ground time count based on frame

    # Convert frame count to time in milliseconds
    frame_duration_ms = (1 / frame_rate) * 1000  # Duration of one frame in milliseconds
    ground_time_ms = ground_time_frames * frame_duration_ms
    return ground_time_ms
=======
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
>>>>>>> Stashed changes

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate ground time from MediaPipe pose JSON data.")
    parser.add_argument('json_file', help="Path to the JSON file containing pose landmarks data")
<<<<<<< Updated upstream
    parser.add_argument('--frame_rate', type=float, default=10, help="Frame rate of the video (default: 10 fps)")
    parser.add_argument('--threshold', type=float, default=0.01, help="Threshold for y-coordinate to determine if feet are on the ground (default: 0.01)")
    return parser.parse_args()

=======
    return parser.parse_args()


>>>>>>> Stashed changes
# Main function
def main():
    # Parse arguments
    args = parse_arguments()

<<<<<<< Updated upstream
    input_step = sys.stdin.read().strip()
    print(input_step)
    # Calculate ground time from the provided JSON file
    ground_time_ms = calculate_ground_time_from_json(args.json_file, args.frame_rate, args.threshold)

    # Output the result
    print(f"Ground time: {ground_time_ms:.2f} ms")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
=======
    # Calculate ground time from the provided JSON file
    ground_time = calculate_ground_time_from_json(args.json_file)
    
    # Output the result
    print(f"Ground time right: {ground_time[0]//10:.2f} ms")
    print(f"Ground time left: {ground_time[1]//10:.2f} ms")
    print(f"Ground time average: {(ground_time[0] + ground_time[1])/2//10:.2f} ms")


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
