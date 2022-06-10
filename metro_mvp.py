import pandas_datareader as web
import pandas as pd
import numpy as np
import math
import random
import time
from matplotlib import pyplot
def Returns(tickers,Start,End):
    returns = []
    for i in tickers:
        SumReturn = 0
        df= web.DataReader(i, data_source='yahoo', start='{0}-1-1'.format(Start), end='{0}-12-31'.format(End))['Close']
        start = '1000'
        firstDay,lastDay,yesterday = 0,0,0
        totalReturn = 0
        lastdata = df.index[-1]
        for x in df.index:
            year = str(x)[0:4]
            if year!=start:
                start = year
                if yesterday == 0:
                    firstDay = df.loc[x]
                else:
                    lastDay = df.loc[yesterday]
                    returnThisYear = (lastDay-firstDay)/firstDay
                    totalReturn += returnThisYear
                    firstDay = df.loc[x]
            if x==lastdata:
                lastDay = df.loc[x]
                returnThisYear = (lastDay-firstDay)/firstDay
                totalReturn += returnThisYear
                Average_return = totalReturn/(End-Start)
                returns.append(Average_return)
            yesterday = x
    return returns
def corr(tickers,Start,End):
    df = pd.DataFrame()
    for x in tickers:
        stock = web.DataReader(x, data_source='yahoo', start='{0}-1-1'.format(Start), end='{0}-12-31'.format(End))
        df[x]=stock['Close']
    C = df.corr()
    return C
start_time = time.time()
Ticker = ['JD','TQQQ','O','VYM','VXX']
#['TQQQ','FXI','YXI','VIXM']
number_of_stocks = len(Ticker)
C = corr(Ticker,2019,2021)
print('...')
m = Returns(Ticker,2018,2020)
#print(m)
w = np.array([round(1/len(Ticker),3) for x in Ticker])

OldEnerge = 100
T = 0.0001
m = np.array(m)
risk = []
mu = []
rrMax = 0
for x in range(1000000):
    i = random.randrange(0,number_of_stocks)
    j = i
    while i==j:
        j = random.randrange(0,number_of_stocks)
        if w[j]<0.001:
            j=i
    w[i]+=0.001
    w[j]-=0.001

    NewEnerge = np.dot(np.dot(w,C),w.T)
    deltaEnerge = NewEnerge-OldEnerge
    r = np.dot(w,m.T)
    if deltaEnerge<0:
        OldEnerge=NewEnerge
    else:
        b = random.uniform(0,1)
        if b<math.exp(-deltaEnerge/T):
            OldEnerge = NewEnerge
        else:
            w[j]+=0.001
            w[i]-=0.001

    if x%20000==0:
        if x%100000==0:
            n = (1000000-x)/100000
            print(n, w, r)
        risk.append(OldEnerge)
        mu.append(r)
    #    print(x/10000,returnOverRisk,r,std,w)
print(C)
print(rrMax,w,r,OldEnerge)
print("--- %s seconds ---" % (time.time() - start_time))
pyplot.scatter(risk,mu,s=3)
pyplot.xlabel('risk')
pyplot.ylabel('return')
pyplot.show()

#7.772668388295422 [0.205 0.408 0.109 0.129 0.102 0.047] 0.4976312090362304 0.06350858989167371
