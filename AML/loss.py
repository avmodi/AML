import numpy as np
import pandas as pd
import re
import math

def smapeScore(groundTruth, predictions):
    
    # Fill NaN values with 0
    groundTruth = groundTruth.fillna(0)

    data = pd.concat([predictions, groundTruth], axis=1, keys=['predictions', 'groundTruth'])
    data = data[data.groundTruth.notnull()]
    
    scores = (abs(data.predictions - data.groundTruth) * 2.0 )/ (abs(data.predictions) + abs(data.groundTruth))
    scores[scores.isnull()] = 0

    result = np.sum(scores) / len(data)
    
    return result