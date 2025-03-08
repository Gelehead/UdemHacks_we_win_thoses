import cv2
import mediapipe as mp
import json
import sys

def process_video(video_path, output_json_path):
    # Initialize MediaPipe Pose and drawing utilities.
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Open the video file.
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    landmarks_dict = {}
    frame_idx = 0

    # Initialize the Pose model.
    with mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            # Convert the image from BGR (OpenCV format) to RGB.
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            # Create a key for the current frame.
            frame_key = f"frame_{frame_idx}"
            if results.pose_landmarks:
                # If landmarks are detected, extract and store each as a dictionary.
                frame_landmarks = []
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    frame_landmarks.append({
                        "id": idx,
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z
                    })
                landmarks_dict[frame_key] = frame_landmarks

                # Optional: draw landmarks on the frame for visualization.
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                landmarks_dict[frame_key] = "No landmarks detected"

            frame_idx += 1

            # Optional: display the processed frame.
            # cv2.imshow("Pose Detection", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    cap.release()
    # cv2.destroyAllWindows()

    # Write the dictionary to a JSON file.
    with open(output_json_path, "w") as outfile:
        json.dump(landmarks_dict, outfile, indent=4)
    print(f"Pose landmarks data saved to {output_json_path}")

if __name__ == "__main__":
    # Usage: python pose_extraction.py <input_video_path> <output_json_path>
    if len(sys.argv) < 3:
        print("Usage: python pose_extraction.py <input_video_path> <output_json_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    output_json_path = sys.argv[2]
    process_video(video_path, output_json_path)
