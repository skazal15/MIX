#!/usr/bin/env python
# coding: utf-8

# In[1]:
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.ar_model import AutoReg
from keras.models import Sequential
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import numpy
from pandas import read_csv
import pandas as pd
from math import sqrt
from sklearn.linear_model import ElasticNet
import pandas as pd # Import Pandas for data manipulation using dataframes
import numpy as np # Import Numpy for data statistical analysis 
import matplotlib.pyplot as plt # Import matplotlib for data visualisation
import random
import seaborn as sns
from datetime import date

all_colors = {'Autoregresif': '#FF9EDD',
              'SimpleExpSmoothing': '#FFFD7F',
              'ExpSmoothing': '#FFA646'}
instances = ['Emas1','SCM','ERM','MUF','AML','MANDIRI ONLINE']
period = {'Disk_Emas1.xlsx':'Day',
           'Exadata.xlsx':'Month'}
data_all = {'Emas1':'Disk_Emas1.xlsx',
           'SCM':'Exadata.xlsx','ERM':'Exadata.xlsx','MUF':'Exadata.xlsx','AML':'Exadata.xlsx','MANDIRI ONLINE':'Exadata.xlsx'}

# In[2]:


def inti(i):
    instance = i
    df = pd.read_excel(data_all[instance], engine='openpyxl')
    df = df[df['Date'].notna()]
    end = []
    data = df.sort_index(ascending=True, axis=0)
    if period[data_all[instance]] == 'Month':
        new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Data'])
        for i in range(0,len(data)):
             new_data['Date'][i] = data['Date'][i]
             new_data['Data'][i] = data[instance][i]
        new_data.to_csv('proses.csv', encoding='utf-8', index=False)
        series = pd.read_csv('proses.csv', index_col=0, squeeze=True, dtype={1: np.float})
        series.index = pd.PeriodIndex(series.index, freq='M', name="Period")
        series.name = "Data"
    if period[data_all[instance]] == 'Day':
        new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Data'])
        for i in range(0,len(data)):
             new_data['Date'][i] = data['Date'][i]
             new_data['Data'][i] = data['Disk'][i]
        new_data.to_csv('proses.csv', encoding='utf-8', index=False)
        series = pd.read_csv('proses.csv', index_col=0, squeeze=True, dtype={1: np.float})
        series.index = pd.PeriodIndex(series.index, freq='D', name="Period")
        series.name = "Data"
    
    if period[data_all[instance]] == 'Month': 
        def autoreg(df):
            model = AutoReg(series, lags=1)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series)-1)
            data0 = yhat
            rmse1=sqrt(mean_squared_error(yhat[1:],series[1:]))
            rmse1=float(rmse1)
            yhat = model_fit.predict(1, len(series)+12)
            data1= yhat
            return rmse1,data1,data0
    
        def smplexpsmth(df):
            # fit model
            model = SimpleExpSmoothing(series)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series)-1)
            data0 = yhat
            rmse2=sqrt(mean_squared_error(yhat,series))
            rmse2=float(rmse2)
            yhat = model_fit.predict(0, len(series)+12)
            data2=yhat
            return rmse2,data2,data0
    
        def Expsmth(df):
            # fit model
            model = ExponentialSmoothing(series)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series)-1)
            data0 = yhat
            rmse3=sqrt(mean_squared_error(yhat,series))
            rmse3=float(rmse3)
            yhat = model_fit.predict(0, len(series)+12)
            data3=yhat
            return rmse3,data3,data0
        rsme1=autoreg(series)
        rsme2=smplexpsmth(series)
        rsme3=Expsmth(series)
    
        s = {'Autoregresif':rsme1[0],'SimpleExpSmoothing':rsme2[0],'ExpSmoothing':rsme3[0]}
        key2 = min(s, key = lambda k: s[k])
        mse=s[key2]
        color = all_colors[key2]
    
        if key2 == 'Autoregresif':
            data = rsme1[1]
            data0 = rsme1[2]
        if key2 == 'SimpleExpSmoothing':
            data = rsme2[1]
            data0 = rsme1[2]
        if key2 == 'ExpSmoothing':
            data = rsme3[1]
            data0 = rsme1[2]
    
        prediction_date = data.index[-1]
        predict = data.values[-1]
        predictdate = data.index[len(series):len(data)].strftime('%b,%Y')
        predictdat = data.values[len(series):len(data)]
        dates = series.index[1:].strftime('%b,%Y')
        d=[]
        d1=[]
        for item in dates:
            d.append(item)
        for item1 in predictdate:
            d1.append(item1)
        
        end = series.values[-1]
        series = series.values[1:]
        predictiondat = data0.values[1:]
        series1 = []
        predictiondat1 = []
        predictdat1 = []
        series1.append(series)
        predictiondat1.append(predictiondat)
        for item2 in predictdat:
            predictdat1.append(item2)
        
    if period[data_all[instance]] == 'Day': 
        def autoreg(df):
            model = AutoReg(series, lags=1)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series))
            data0 = yhat
            rmse1=sqrt(mean_squared_error(yhat[1:],series))
            rmse1=float(rmse1)
            yhat = model_fit.predict(1, len(series)+360)
            data1= yhat
            return rmse1,data1,data0
    
        def smplexpsmth(df):
            # fit model
            model = SimpleExpSmoothing(series)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series)-1)
            data0 = yhat
            rmse2=sqrt(mean_squared_error(yhat,series))
            rmse2=float(rmse2)
            yhat = model_fit.predict(0, len(series)+360)
            data2=yhat
            return rmse2,data2,data0
    
        def Expsmth(df):
            # fit model
            model = ExponentialSmoothing(series)
            model_fit = model.fit()
            # make prediction
            yhat = model_fit.predict(0, len(series)-1)
            data0 = yhat
            rmse3=sqrt(mean_squared_error(yhat,series))
            rmse3=float(rmse3)
            data3=yhat
            return rmse3,data3,data0
    
        rsme1=autoreg(series)
        rsme2=smplexpsmth(series)
        rsme3=Expsmth(series)
    
        s = {'Autoregresif':rsme1[0],'SimpleExpSmoothing':rsme2[0],'ExpSmoothing':rsme3[0]}
        key2 = min(s, key = lambda k: s[k])
        mse=s[key2]
        color = all_colors[key2]
    
        if key2 == 'Autoregresif':
            data = rsme1[1]
            data0 = rsme1[2]
        if key2 == 'SimpleExpSmoothing':
            data = rsme2[1]
            data0 = rsme1[2]
        if key2 == 'ExpSmoothing':
            data = rsme3[1]
            data0 = rsme1[2]
    
        prediction_date = data.index[-1]
        predictdate = data.index[len(series):len(data)].strftime('%m, %Y, %d')
        predictdat = data.values[len(series):len(data)]
        predict = data.values[-1]
        dates = series.index[1:].strftime('%m, %Y, %d')
        end = series.values[-1]

        d=[]
        d1=[]
        for item in dates:
            d.append(item)
        for item1 in predictdate:
            d1.append(item1)
        series = series.values[1:]
        predictiondat = data0.values[1:len(data0)-1]
       
        series1 = []
        predictiondat1 = []
        predictdat1 = []
        series1.append(series)
        predictiondat1.append(predictiondat)
        for item2 in predictdat:
            predictdat1.append(item2)
        print(dates)
    return(prediction_date,predict,d,series1,predictiondat1,key2,color,mse,instance,d1,predictdat1,data,end)


# In[3]:
all_data=[]
m=[]
def hit():
    c=list(set(instances) - set(m))
    print(c)
    if not m:
        for i in instances:
            a=inti(i)
            key2=a[5]
            prediction_date=a[0] 
            d=a[2]
            series1=a[3]  
            color=a[6]
            predictiondat1=a[4]
            mse=a[7]
            instance=a[8]
            predict=a[1]
            d1=a[9]
            predictdat1=a[10]
            data=a[11]
            last=a[12]
            folder = data_all[i]
            all_data.append((key2,prediction_date,d,series1,color,predictiondat1,mse,instance,predict,d1,predictdat1,data,folder,last))
        m.extend(instances)
    else:
        for i in c:
            a=inti(i)
            key2=a[5]
            prediction_date=a[0] 
            d=a[2]
            series1=a[3]  
            color=a[6]
            predictiondat1=a[4]
            mse=a[7]
            instance=a[8]
            predict=a[1]
            d1=a[9]
            predictdat1=a[10]
            data=a[11]
            last=a[12]
            folder = data_all[i]
            all_data.append((key2,prediction_date,d,series1,color,predictiondat1,mse,instance,predict,d1,predictdat1,data,folder,last))
        m.extend(c)
hit()
# In[4]:


ex = []
for i in range(len(instances)):
    if all_data[i][7].lower() in ['scm','erm','aml','muf','mandiri online']:
        ex.append(all_data[i][8])
exadata = round(sum(ex),2)
exa=str(exadata)+' GB'

