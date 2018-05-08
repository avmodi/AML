import numpy as np
import pandas as pd
import re
import math
from reader import *
from loss import *

def smape(y_true, y_pred):
	denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
	diff = np.abs(y_true - y_pred) / denominator
	diff[denominator == 0] = 0.0
	return np.nanmean(diff)



train, test =read()


def median(train, test):
	Windows = [6, 12, 18, 30, 48, 78]
	n = train.shape[1] - 1
	#print(n)
	Visits = np.zeros(train.shape[0])

	# Each row in train.iterrows() is a time series
	for index, timeSeries in train.iterrows():
		M = []
		# Ignore First column. First column is article name
		begin = timeSeries[1:].nonzero()[0]

		if len(begin) == 0:
			continue

		interval=n - begin[0]
		if interval < Windows[0]:
			Visits[index] = timeSeries.iloc[begin[0]+1:].median()
			continue
		for W in Windows:
			if W > interval:
				break
			M.append(timeSeries.iloc[-W:].median())
		Visits[index] = np.median(M)

	Visits[np.where(Visits < 1)] = 0.
	train['Visits'] = Visits
	#print(Visits)


	test['Page'] = test.Page.apply(lambda x: x[:-11])
	#print(test)

	print('Creating submission file')
	test = test.merge(train[['Page','Visits']], on='Page', how='left')
	test[['Id','Visits']].to_csv('sub_baseline.csv', index=False)

	


median(train,test)
actual=pd.read_csv("test.csv")
actual=actual.drop("Id",axis=1)
actual=actual.values

predictions=pd.read_csv("sub_baseline.csv")
predictions=predictions.drop("Id",axis=1)
predictions=predictions.values

print('Final Smape score is : ', smape(actual,predictions))




