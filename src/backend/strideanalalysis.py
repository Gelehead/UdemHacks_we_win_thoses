import json
import math
import numpy as np
from scipy.signal import find_peaks

def calculate_distance(landmark1, landmark2):
    """Calculates the Euclidean distance between two landmarks."""
    x1, y1, z1 = landmark1['x'], landmark1['y'], landmark1['z']
    x2, y2, z2 = landmark2['x'], landmark2['y'], landmark2['z']

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def get_max_distances(filepath):
    """Reads the JSON file and calculates the distance between landmarks 31 and 32 for each frame."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    distances = []
    i = 0
    for frame, landmark in data.items():
        i += 1

        landmark31 = landmark[31]
        landmark32 = landmark[32]
        if landmark31 and landmark32:
            distance = calculate_distance(landmark31, landmark32)
            distances.append(distance)
        else:
            distances.append(None) # Handle cases where a landmark is missing
            
    peaks, _ = find_peaks(np.array(distances), prominence=0.01)
    
    return peaks, distances

def get_data(filepath):
    """ returns: step count, peak indices and distances """
    
    
    peak_indices, distances = get_max_distances(filepath)
    step_count = len(peak_indices)
    
    # every other thing here can be infered based on returned variables
    # leaving code here for lazy people
    """left_group = list(peak_indices[i] for i in range(0, step_count, 2))
    right_group = list(peak_indices[i] for i in range(1, step_count, 2))
    
    overall_avg = sum(distances) / step_count
    
    normalizing_factor_left = overall_avg / (sum(left_group) / len(left_group))
    normalizing_factor_right = overall_avg / (sum(right_group) / len(right_group))
    
    avg_right = list(map(lambda x : normalizing_factor_right, right_group))
    avg_left = list(map(lambda x : normalizing_factor_left, left_group)) """
    
    return step_count, peak_indices, distances
    
print(get_data("output.json"))
