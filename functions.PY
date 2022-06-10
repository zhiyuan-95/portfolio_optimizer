import pandas_datareader as web
import csv
import pandas as pd
import numpy as np
import time
start_time = time.time()
class portfolio:
    def __init__(self,u,C):
        self._u1 = u[0]
        self._u2 = u[1]
        self._u3 = u[2]
        self._m = np.array([self._u1,self._u2,self._u3])
        self._C = C
        self._Cinv = np.linalg.inv(self._C)
        self._U = np.ones(3)
    def dot_product_3(self,x,y,z):
        xy = np.dot(x,y)
        xyz = np.dot(xy,z)
        return xyz
    def mvp(self):
        U_Cinv = np.dot(self._U,self._Cinv)
        U_Cinv_U = np.dot(U_Cinv,self._U.T)
        Wmvp = U_Cinv/U_Cinv_U
        return Wmvp
    def CML(self,R):
        RU_m = R*self._U-self._m
        w = np.dot(RU_m,self._Cinv)/self.dot_product_3(RU_m,self._Cinv,self._U.T)
        return w
    def show_mvp(self):# print w expected return, varience, std
        w = self.mvp()
        u_v = np.dot(w,self._m.T)
        var = self.dot_product_3(w,self._C,w.T)
        std = np.sqrt(var)
        print('m = ', self._m)
        print('w = ', w)
        print('expected return = {0:.6f}'.format(u_v))
        print('varience = {0:.6f}'.format(var))
        print('std = {0:.6f}'.format(std))
    def show_CML(self,R):
        w = self.CML(R)
        u_v = np.dot(w,self._m.T)
        var = self.dot_product_3(w,self._C,w.T)
        std = np.sqrt(var)
        print('m = ', self._m)
        print('w = ', w)
        print('expected return = {0:.6f}'.format(u_v))
        print('varience = {0:.6f}'.format(var))
        print('std = {0:.6f}'.format(std))
def get_stocks(tickers,start,end):
    for x in tickers:
        df = web.DataReader(x, data_source='yahoo', start='{0}-1-1'.format(start), end='{0}-12-31'.format(end))
        fileName = x+str(start)+str(end)
        df.to_csv(r"C:\Users\johnk\OneDrive\Desktop\project\data_store\{0}.csv".format(str(fileName)))
def ave_Returns(tickers,Start,End):
    AverageR = []
    for i in tickers:
        SumReturn = 0
        for x in range(Start,End+1):
            df1 = web.DataReader(i, data_source='yahoo', start='{0}-1-1'.format(x), end='{0}-12-31'.format(x))
            price1 = df1['Close'][0]
            price2 = df1['Close'][-1]
            Return = (price2-price1)/price1
            SumReturn+=Return
        period = End-Start
        print(i)
        AverageR.append(SumReturn/period)
    return AverageR
def corr(tickers,Start,End):
    df = pd.DataFrame()
    for x in tickers:
        stock = web.DataReader(x, data_source='yahoo', start='{0}-1-1'.format(Start), end='{0}-12-31'.format(End))
        df[x]=stock['Close']
    C = df.corr()
    return C
def Returns(tickers,Start,End):
    returns = []
    for i in tickers:
        SumReturn = 0
        df= web.DataReader(i, data_source='yahoo', start='{0}-1-1'.format(Start), end='{0}-12-31'.format(End))['Close']
        start = '1000'
        firstDayPrice,lastDayPrice,yesterday = 0,0,0
        totalReturn = 0
        lastdata = df.index[-1]
        for x in df.index:
            year = str(x)[0:4]
            if year!=start:
                n = 0
                start = year
                if yesterday == 0:
                    firstDayPrice = df.loc[x]
                else:
                    lastDayPrice = df.loc[yesterday]
                    returnThisYear = (lastDayPrice-firstDayPrice)/firstDayPrice
                    totalReturn += returnThisYear
                    firstDayPrice = df.loc[x]
            if x==lastdata:
                lastDayPrice = df.loc[x]
                current_return = (lastDayPrice-firstDayPrice)/firstDayPrice
                Average_return0 = totalReturn/(End-Start-1)
                returnThisYear = current_return*n/253+Average_return0*(253-n)/253
                totalReturn += returnThisYear
                Average_return = totalReturn/(End-Start)
                returns.append(Average_return)
            yesterday = x
            n+=1
    return returns

get_stocks(['MSFT'],2015,2021)
Returns(MSFT,2015,2021)
#stock_csv(['JD','TQQQ','VXX','O','XPP','FXP'],2018,2020)
#df = pd.read_csv(r"C:\Users\johnk\OneDrive\Desktop\project\data_store\TQQQ20182020.csv")
print("--- %s seconds ---" % (time.time() - start_time))
#fileName = ticker+str(x)+'.csv'
#df1.to_csv(r"C:\Users\johnk\OneDrive\Desktop\project\da
