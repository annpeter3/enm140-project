import numpy as np
import math

def build(number_of_districts, shape, amplitude):
    districts = np.zeros(number_of_districts, dtype=int)
    length = int(number_of_districts)
    if shape == "stair" :
        for i in range(length):
            if i < int(length/2):
                districts[i] = amplitude * length/2 - i * amplitude
            else:
                districts[i] = - districts[- (i + 1)]
    elif shape == "flat":
        return np.zeros(number_of_districts)
    elif shape == "polarized":
        for i in range(length):
            if i == int(length/2) and (i + 1) * 2 > length:
                districts[i] = 0
            elif i >= length/2:
                districts[i] = -amplitude
            else:
                districts[i] = amplitude
    elif shape == "cosine":
        for i in range(length):
            if i < int(length/2):
                districts[i] = int(amplitude * math.cos(i * 1.57 / (length / 2 -1)))
            else:
                districts[i] = - districts[- (i + 1)]
    return districts