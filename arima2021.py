#https://towardsdatascience.com/advanced-time-series-analysis-with-arma-and-arima-a7d9b589ed6d
#https://machinelearningmastery.com/tune-arima-parameters-python/
import numpy as np
import pandas as pd
import yfinance as yf
import warnings
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import datetime
import time

ticker = input('ticker: ')
stock = yf.Ticker(ticker)
time1 = input('time1(yyyy mm dd): ').split()
td = datetime.date.today()
data_frame = stock.history(start="{0}-{1}-{2}".format(time1[0],time1[1],time1[2]), end="{0}".format(td))
df = data_frame[['Close']]
lndf = np.log(df).fillna(np.log(df))
def stationarization(dt):
    number_of_diff = 0
    ddt = dt
    while adfuller(ddt)[1]>0.01:
        ddt = ddt.diff().fillna(ddt)[1:]
        number_of_diff+=1
    print('serie is been stationarized, diff=',number_of_diff)
    return ddt, number_of_diff
lndiff,numberof_diff= stationarization(lndf)

if numberof_diff>1:
    print('number_of_diff > 1')
plot_acf(lndiff)
plot_pacf(lndiff)
#pyplot.show()
lag = 6
results = list()
i = []
for x in range(len(lndiff)):
    i.append(lndiff['Close'].iloc[x])
lndiff = np.array(i)
#print(lndiff)
ARIMA1 = ARIMA(lndiff,order=(1,0,1)).fit()
ARIMA1.summary()

for x in range(lag+1):
    for y in range(lag+1):
        try:
            ARIMA1 = ARIMA(lndiff,order=(1,0,1)).fit()
            print('helllo')
            lg = tuple([x,numberof_diff,y])
            results.append((lg,ARIMA1.aic))
            print(lg,ARIMA1.aic)
        except:
            continue
print('$$$')
print(results)
print('$$$')
result_df = pd.DataFrame(results)

result_df.columns = ['(p, d, q)', 'AIC']
#Sort in ascending order, the lower AIC the better so
#I will pick the p,q which have lowest AIC
result_df = result_df.sort_values(by='AIC', ascending=True).reset_index(drop=True)
best_p_q = result_df['(p, d, q)'][0]
p = best_p_q[0]
q = best_p_q[2]

#I kept a part of data and creat a model with the rest of the data and the p,q just got
# so I can get the residuel between the forecast value given by the model for next time period and
# the real value I spared.
X = lndiff.values
S = len(X)
n = int(S/4)
size = S-n
train,test = X[0:size],X[size:len(X)]
train1 = [x for x in train]
prediction = list()
iteration = 0
for t in range(len(test)):
    try:
        ARIMAdata = ARIMA(train1,order=(p,0,q)).fit(disp = -1, transparams=False)
        warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',FutureWarning)
        yhat = ARIMAdata.forecast()[0]
        prediction.append(yhat)
        train1.append(test[t])
        iteration += 1
        print('times of iteration: ',iteration)
        print(yhat)
        #input('')
    except:
        continue
print(ARIMAdata.summary())
# I want to check the differenct of the original value
# the data has been stationarized, so I have to transfer back to original scale
l1 = lndf[S-n:S]
predict_lnYhat = l1+np.array(prediction)
predict_Yhat = np.exp(predict_lnYhat)
idx =list(range(1,n+1))
predict_Yhat.index = idx
actual_value = df[S-n+1:]
actual_value.index = idx

residuel = actual_value-predict_Yhat
Diff =  df.diff()[-n:]
SSR = sum(list(residuel['Close']**2))
TSS = sum(list(Diff['Close']**2))
print('sample R: ', 1-SSR/TSS,'\n')

rmseOfResiduel = np.sqrt(np.mean(residuel)**2)
rmseOfFristDiff = np.sqrt(np.mean(Diff)**2)

print('rmse of residuel: ', rmseOfResiduel['Close'])
print('rmse of first difference: ', rmseOfFristDiff['Close'])


#ljung_box, p_value = acorr_ljungbox(ARIMAdata.resid)
#print(f'Ljung-Box test : {ljung_box[:10]}')
#print(f'   p-value     : {p_value[:10]}')

pyplot.show()
pyplot.plot(actual_value)
pyplot.plot(predict_Yhat,color = 'red')
pyplot.legend(['actual value', 'predicted value'])
pyplot.show()

pyplot.scatter(residuel,idx,cmap='Orange')
pyplot.title('residuel scatter plot')
