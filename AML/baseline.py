import numpy as np
import pandas as pd
import re
import math
from reader import *
from loss import *




train, test =read()


def median(train, test):
	Windows = [6, 12, 18, 30, 48, 78, 126, 203, 329]
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
	test[['Id','Visits']].to_csv('sub.csv', index=False)