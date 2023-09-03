# portfolio_optimizer

this experiment is about to invest base on the optimized sharpe value of portfolio of given stock and given risk free rate, and update portfolio every week(because return and corelation changes).

I choose a certain period of time(12 weeks), and choose few stocks.
sharpe ratio = (portfolio return - risk free rate)/ std of portfolio

return of a single stock =  return on price change + return from divident
return on price change = (price(t1)-price(t0))/price(t0)
return on divident = total divident from last year * (period)/52  
--period is number of weeks

portfolio return = optimized weight * return of each stock
I want to get the optimized weight of portfolio to have the hightest sharpe ratio.
I used the function minimize from scipy.optimize to get the opimized weight of portfolio of minimum of -sharpe ratio

### stimulation
initial asset is 100
