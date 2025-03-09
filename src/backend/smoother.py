import numpy as np
import pose_extraction
from collections import deque

#01001

# Filter Constants
MOV_AVERAGE = 1  # 00001
KALMAN_FIL = 2   # 00010
LIN_INTERP = 4   # 00100
HI_TRACK_CONF = 8  # 01000
CUBIC_SPLINE = 16  # 10000

def moving_average_smoothing(landmarks_list, window_size=5):
    """Applies a moving average filter to smooth pose landmark positions."""
    history = deque(maxlen=window_size)
    smoothed_landmarks = []

    for landmarks in landmarks_list:
        if landmarks is None:  # Skip empty frames
            smoothed_landmarks.append(None)
            continue
        
        history.append(landmarks)
        avg_landmarks = []
        for i in range(len(landmarks)):
            avg_x = sum(frame[i]['x'] for frame in history) / len(history)
            avg_y = sum(frame[i]['y'] for frame in history) / len(history)
            avg_z = sum(frame[i]['z'] for frame in history) / len(history)
            avg_landmarks.append({"id": landmarks[i]["id"], "x": avg_x, "y": avg_y, "z": avg_z})
        
        smoothed_landmarks.append(avg_landmarks)
    
    return smoothed_landmarks

def linear_interpolation(landmarks_list):
    """Interpolates missing frames using linear interpolation."""
    if not landmarks_list:
        return landmarks_list

    for i in range(len(landmarks_list)):
        if landmarks_list[i] is None:
            prev_idx, next_idx = None, None
            for j in range(i - 1, -1, -1):
                if landmarks_list[j] is not None:
                    prev_idx = j
                    break
            for j in range(i + 1, len(landmarks_list)):
                if landmarks_list[j] is not None:
                    next_idx = j
                    break
            
            if prev_idx is not None and next_idx is not None:
                # Linear interpolation between prev_idx and next_idx
                alpha = (i - prev_idx) / (next_idx - prev_idx)
                interpolated = [
                    {
                        "id": landmarks_list[prev_idx][k]["id"],
                        "x": (1 - alpha) * landmarks_list[prev_idx][k]["x"] + alpha * landmarks_list[next_idx][k]["x"],
                        "y": (1 - alpha) * landmarks_list[prev_idx][k]["y"] + alpha * landmarks_list[next_idx][k]["y"],
                        "z": (1 - alpha) * landmarks_list[prev_idx][k]["z"] + alpha * landmarks_list[next_idx][k]["z"],
                    }
                    for k in range(len(landmarks_list[prev_idx]))
                ]
                landmarks_list[i] = interpolated
    return landmarks_list

def kalman_filter(landmarks_list):
    return landmarks_list

def apply_smoothing(landmarks_list, filters):
    """Applies the chosen smoothing filters based on binary flags."""
    filters = int(filters)
    
    if filters & KALMAN_FIL:
        landmarks_list = kalman_filter(landmarks_list)
        
    if filters & MOV_AVERAGE:
        landmarks_list = moving_average_smoothing(landmarks_list)

    if filters & LIN_INTERP:
        landmarks_list = linear_interpolation(landmarks_list)
    
    if filters & HI_TRACK_CONF:
        a=0
        
    if filters & CUBIC_SPLINE:
        a=0

    return landmarks_list

def smooth(landmarks_list, filters):
    """Main function to apply smoothing filters and return processed landmarks."""
    return apply_smoothing(landmarks_list, filters)
