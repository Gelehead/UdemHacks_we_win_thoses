import cv2
import smoother
import video_player
import mediapipe as mp
import json
import sys
import numpy as np
from collections import deque
import os

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def extract_pose_landmarks(frame, pose):
    """Detects pose landmarks in a frame and returns a skeleton image."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    frame_landmarks = []
    black_frame = np.zeros_like(frame)

    if results.pose_landmarks:
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            frame_landmarks.append({
                "id": idx,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z
            })
        mp_drawing.draw_landmarks(black_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    else:
        frame_landmarks = None  # No landmarks detected

    return frame, black_frame, frame_landmarks

def process_video(video_path, output_json_path, filters):
    """Processes video, extracts pose landmarks, and applies smoothing."""
    cap = cv2.VideoCapture(video_path)
    frames, landmarks_list = [], []
    
    print("")
    print("cccccccccccccccc")
    print("")

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, black_frame, landmark = extract_pose_landmarks(frame, pose)

            landmarks_list.append(landmark)
            frames.append(black_frame)

    cap.release()

    # Apply smoothing filters
    smoothed_landmarks = smoother.apply_smoothing(landmarks_list, filters)

    # Save smoothed landmarks
    landmarks_dict = {f"frame_{i}": smoothed_landmarks[i] if smoothed_landmarks[i] else "No landmarks detected"
                      for i in range(len(smoothed_landmarks))}
    
    with open(output_json_path, "w") as outfile:
        json.dump(landmarks_dict, outfile, indent=4)
    
    print(f"Pose landmarks data saved to {output_json_path}")

    return frames

if __name__ == "__main__":
    video_path, output_json_path, filters = sys.argv[1], sys.argv[2], sys.argv[3]
    frames = process_video(video_path, output_json_path, filters)
    video_player.read_video(frames)
