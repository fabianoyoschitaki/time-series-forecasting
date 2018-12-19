# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:43:56 2018

@author: Fabiano Yoschitaki
"""

# -*- coding: utf-8 -*-
# Made available at http://www.mariofilho.com
# For educational purposes only, Author offers NO GUARANTEES
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd

#MAPE calculation function
def mape(y_pred,y_true):
  return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


#Loading the data
data = pd.read_csv('COTAHIST_A2018_PROCESSED_PETR4.CSV', delimiter=';')
print "PETR4 data: {} linhas e {} colunas".format(data.shape[0], data.shape[1])

x_data = []
y_data = []

# Creates a feature matrix with values from previous 6 months
#for d in xrange(6, data.shape[0]):
for d in xrange(6, data.shape[0]):
    x = data.iloc[d-6:d]['Fechamento'].values.ravel()
    y = data.iloc[d]['Fechamento']
    x_data.append(x)
    y_data.append(y)
    if d % 10000 == 0:
        print d
    
x_data = np.array(x_data)
y_data = np.array(y_data)

#Lists to store the predictions of the models
y_pred = []
y_pred_last = []
y_pred_ma = []
y_true = []

#Iterate over the time series creating a new model each month
end = y_data.shape[0]
for i in range(30,end):

    x_train = x_data[:i,:]
    y_train = y_data[:i]
    
    x_test = x_data[i,:]
    y_test = y_data[i]


    model = LinearRegression(normalize=True)
    model.fit(x_train,y_train)

    y_pred.append(model.predict(x_test.reshape(1, -1))[0])
    y_pred_last.append(x_test[-1])
    y_pred_ma.append(x_test.mean())
    y_true.append(y_test)


#Transforms the lists into numpy arrays
y_pred = np.array(y_pred)
y_pred_last = np.array(y_pred_last)
y_pred_ma = np.array(y_pred_ma)
y_true = np.array(y_true)


#Print errors
print '\nMean Absolute Percentage Error'
print 'MAPE Linear Regression', mape(y_pred,y_true)
print 'MAPE Last Value Benchmark', mape(y_pred_last,y_true)
print 'MAPE Moving Average Benchmark', mape(y_pred_ma,y_true)


print '\nMean Absolute Error'
print 'MAE Linear Regression', mean_absolute_error(y_pred,y_true)
print 'MAE Last Value Benchmark', mean_absolute_error(y_pred_last,y_true)
print 'MAE Moving Average Benchmark', mean_absolute_error(y_pred_ma,y_true)


#Cria um gráfico dos valores reais, previsões da regressão linear e do modelo utilizando o último valor
# OPCIONAL - REQUER MATPLOTLIB
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
plt.title("Fechamento PETR4 - Diariamente - {} a {}".format(data['Data'][0], data['Data'][data.shape[0]-1]))
plt.ylabel('Valor Fechamento')
plt.xlabel(u'Período (Dias)')
reg_val, = plt.plot(y_pred,color='b',label=u'Linear Regression')
true_val, = plt.plot(y_true,color='g', label='True Values')
plt.xlim([0,data.shape[0]-6])
plt.legend(handles=[true_val,reg_val])
plt.show()