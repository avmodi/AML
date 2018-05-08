import numpy as np
import pandas as pd
import re
import math

def smape(y_true, y_pred):
	denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
	diff = np.abs(y_true - y_pred) / denominator
	diff[denominator == 0] = 0.0
	return np.nanmean(diff)