# -*- coding: utf-8 -*-
"""linear_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1USc1-t1JUxyFc326VZygtAXRiktddjiy
"""

import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
numberOfPrev=5

#Create a dataframe for the data from Tata Motors
df=pd.read_csv('TTM.csv')

# df.info()

#Filter the dataframe to retain only necessary columns
required_fields=['Date','Close']
df= df[required_fields]

#Change the type of 'Date' to datetime
df.Date=pd.to_datetime(df.Date)
df.tail

#Set Date as the index of dataframe
df=df.set_index(['Date'])
df

#A plot depicting the close values across years
plt.figure(figsize=(16,8))
plt.plot(df['Close'])
plt.xlabel('Year')
plt.ylabel("Closing price")
plt.show()

#This method takes a dataframe with 2 columns(Date and Close) and converts it into required format for training(Date, Close and Close values of previous 5 days)
def format_dataframe(df1,n):
  close=list(df['Close'])
  df1=df[n::]
  df1=df1.T
  for i in range(1,n+1):
    day="Day-"+str(i)
    df1.loc[day,:]=close[n-i:-i]
  return df1.T

# df=format_dataframe(df)

df=format_dataframe(df,numberOfPrev)

df.head(25)

def obtain_training_data(df1,n):
  dates=list(df.index)
  columnList=[]
  for i in range(1,n+1):
    day="Day-"+str(i)
    columnList.append(df[day])

  x=list(list(x) for x in columnList)
  X=np.array(x).T
  # X=x.reshape(len(dates),x.shape[1],1)
  y=list(df['Close'])
  return np.array(dates),X,np.array(y)

# dates,input, output=obtain_training_data(df)
# input.shape,output.shape,dates.shape

dates,input, output=obtain_training_data(df,numberOfPrev)
input.shape,output.shape,dates.shape

#Splits dates, inputs and actual outputs to train,validation and test sets (80%-10%-10%)
lenEightyPercent = int(len(dates) * .8)
lenNinetyPercent= int(len(dates) * .9)

inputTrain = input[ :lenEightyPercent]
outputTrain = output[ :lenEightyPercent]
datesTrain =dates[ :lenEightyPercent]

inputVal = input[lenEightyPercent : lenNinetyPercent]
outputVal = output[lenEightyPercent : lenNinetyPercent]
datesVal =dates[lenEightyPercent : lenNinetyPercent]

inputTest = input[lenNinetyPercent: ]
outputTest = output[lenNinetyPercent: ]
datesTest =dates[lenNinetyPercent: ]

plt.figure(figsize=(16,8))
plt.plot(datesTrain, outputTrain)
plt.plot(datesVal, outputVal)
plt.plot(datesTest, outputTest)
plt.xlabel('Year')
plt.ylabel("Closing price")
plt.legend(['Train', 'Validation', 'Test'])
plt.show()

from sklearn.linear_model import LinearRegression
reg_model=LinearRegression()

reg_model.fit(inputTrain,outputTrain)

predict_train=reg_model.predict(inputTrain)
predict_val=reg_model.predict(inputVal)
predict_test=reg_model.predict(inputTest)

plt.figure(figsize=(16,8))
plt.plot(datesTest, predict_test)
plt.plot(datesTest, outputTest)
plt.legend(['Testing Predictions', 'Testing Observations'])

from sklearn.metrics import mean_absolute_error
mean_absolute_error(outputTest,predict_test)
import math
from sklearn.metrics import mean_squared_error
k=math.sqrt(mean_squared_error(outputTest,predict_test))
print(k)

plt.figure(figsize=(25,12))
plt.plot(datesTrain, predict_train)
plt.plot(datesTrain, outputTrain)
plt.plot(datesVal, predict_val)
plt.plot(datesVal, outputVal)
plt.plot(datesTest, predict_test)
plt.plot(datesTest, outputTest)
plt.legend(['Training Predictions',
            'Training Observations',
            'Validation Predictions',
            'Validation Observations',
            'Testing Predictions',
            'Testing Observations'])

import copy
output_test_prediction=[]
output_test_prediction=np.array(output_test_prediction)
temp_array_test_input=[]
temp_array_test_input=np.array(temp_array_test_input)
for i in range(len(inputTest[0])):
  temp_array_test_input=np.append(temp_array_test_input,float(inputTest[0][i]))

temp_array_test_input1=np.flip(temp_array_test_input)
# print(temp_array_test_input1)

for i in range(len(inputTest)):
  ip=temp_array_test_input[0:numberOfPrev]
  # ip=np.flip(ip)
  ip=ip.reshape(1,numberOfPrev)
  res=reg_model.predict(ip).flatten()
  output_test_prediction=np.append(output_test_prediction,res)
  temp_array_test_input=np.insert(temp_array_test_input,0,res)

plt.figure(figsize=(16,8))
plt.plot(datesTest, output_test_prediction)
plt.plot(datesTest, outputTest)
plt.legend(['Testing Predictions', 'Testing Observations'])

# from sklearn.linear_model import Lasso
# lasso_model=Lasso(alpha=1.0)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(outputTest,output_test_prediction)

plt.figure(figsize=(16,8))
plt.plot(datesTrain, predict_train)
plt.plot(datesTrain, outputTrain)
plt.plot(datesVal, predict_val)
plt.plot(datesVal, outputVal)
plt.plot(datesTest, output_test_prediction)
plt.plot(datesTest, outputTest)
# plt.legend(['Testing Predictions', 'Testing Observations'])
plt.legend(['Training Predictions',
            'Training Observations',
            'Validation Predictions',
            'Validation Observations',
            'Testing Predictions',
            'Testing Observations'])