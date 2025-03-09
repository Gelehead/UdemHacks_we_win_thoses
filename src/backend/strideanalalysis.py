import json
import math

def calculate_distance(landmark1, landmark2):
    """Calculates the Euclidean distance between two landmarks."""
    x1, y1, z1 = landmark1['x'], landmark1['y'], landmark1['z']
    x2, y2, z2 = landmark2['x'], landmark2['y'], landmark2['z']

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def get_distances(filepath):
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

    return distances

# Example usage
#filepath = r"c:\Users\thoml\UdemHacks_we_win_thoses\src\backend\pose_landmarks.json"

# distances_array = get_distances(filepath)

# returns the frames of the max stride lenght
def find_max_distance(distances_array):
    maximums = []
    climbin = False
    for i in range(1, len(distances_array)):
        first = distances_array[i-1]
        second = distances_array[i]

        if first is not None and second is not None:
            if max(first,second) == first:
                maximums.append(i-1)
                climbin = False
            else:
                climbin = True

    sum = 0
    for i in range(1,len(maximums)):
        sum += maximums[i] - maximums[i-1]
    average = sum / len(maximums)
    
    temp = maximums.copy()

    for i in range(1,len(maximums)):
        if (maximums[i] - maximums[i-1]) < average * 0.25:
            if i-1 == 0:
                temp = temp[1:]
            elif i == len(maximums):
                temp = temp[:-1]
            else:
                temp = temp[:i-1] + [(temp[i] - temp[i-1]) / 2] + temp[i+1:]
    return temp

# Example usage:
# this function takes in the filepath (readable to open()) and outputs 
# a table containing the step count and an array containg the lenght of each 
# step
def get_data(filepath):
    distances_array = get_distances(filepath)
    print(distances_array)
    maximums = find_max_distance(distances_array)
    step_count = len(maximums)
    step_lenght = []
    for i in maximums:
        step_lenght.append(distances_array[i])
    return [step_count, step_lenght]
    
print(get_data("test3.json"))
