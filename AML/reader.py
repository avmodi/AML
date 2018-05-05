import numpy as np
import pandas as pd
import re
import math
import pickle

TRAIN_FILE='data/train_2.csv'
KEYS_FILE='data/key_2.csv'

TRAIN_BINARY='data/train_2.pkl'
KEYS_BINARY='data/keys_2.pkl'



def read():
	# Load the data
	print('Reading train file')
	try:
		train= pickle.load(open(TRAIN_BINARY,'rb'))
	except:
		train=pd.read_csv(TRAIN_FILE)
		pickle.dump(train,open(TRAIN_BINARY,'wb'))

	print('Reading keys file')
	try:
		keys=pickle.load(open(KEYS_BINARY,'rb'))
	except:
		keys=pd.read_csv(KEYS_FILE)
		pickle.dump(keys,open(KEYS_BINARY,'wb'))

	# Check for missing values
	print('Checking for missing values')
	nulls=train[train.isnull().any(axis=1)]

	# Replace nulls with 0
	print('Replacing nulls with 0')
	train=train.fillna(0.0)
	return train, keys

def getMetadata(train):
	page_metadata=train.Page.str.extract(r'(?P<article>.*)\_(?P<language>.*).wikipedia.org\_(?P<access>.*)\_(?P<type>.*)', expand=False)
	return page_metadata


def split(spercent):
	train, keys, nulls =read()
	page_metadata = getMetadata(train)

	train=pd.concat((page_metadata, train), axis=1)
	forecast_point=math.floor((train.shape[1]-5)*(1-spercent))
	print('Forecast Point is: ',forecast_point)
	X_train=train.iloc[:,0:forecast_point]
	Y_train=train.iloc[:, np.r_[0,1,2,3,4,forecast_point:train.shape[1]]]

	print(X_train[0:5])
	print(Y_train[0:5])
	return X_train, Y_train


#split(0.1)
