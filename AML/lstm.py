import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from reader import *


train,test = read() 
page = train['Page']
train = train.drop('Page',axis = 1)

m=train.shape[1]
n=train.shape[0]
print(m)

X = train.iloc[:,0:m-1].values
y = train.iloc[:,1:m].values



X_train=X
y_train=y

print(X_train.shape)


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

# Initialising the RNN
regressor = Sequential()

# Adding the input layerand the LSTM layer
regressor.add(LSTM(units = 8, activation = 'relu', input_shape = (None, 1)))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
print(X_train.shape)
c=0
for col in range(len(X_train[0])-1):
	c+=1
	show=0
	if (c%100 == 0):
		print('Scanned ', str(c), 'sequences')
		show=1
	X_t=X_train[:,col]
	#print(X_t.shape)
	y_t=y_train[:,col]
	X_t=np.reshape(X_t,(X_t.shape[0],1,1))
	regressor.fit(X_t, y_t, batch_size = 10000, epochs = 3, verbose = show)

inputs = X_train[:,-1]

inputs = np.reshape(inputs, (inputs.shape[0],1, 1))
y_pred = regressor.predict(inputs)

print(y_pred.shape)

print(y_pred)
train['Page']=page
train['Visits']=y_pred
test['Page'] = test.Page.apply(lambda x: x[:-11])

print('Creating submission file')
test = test.merge(train[['Page','Visits']], on='Page', how='left')
test[['Id','Visits']].to_csv('sub.csv', index=False)