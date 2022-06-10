import robin_stocks as r
from matplotlib import pyplot
from datetime import timezone, datetime, timedelta,date
import time
p = 12
P = 26
class build_holdings:
    def __init__(self):
        self._holding = dict()
        self._net_profit = 0
        self._free_space = 20
        self._ema = {}
        self._sold = []
    def buy(self,name,price,ema1,ema2):
        quantity = 20/float(price)
        self._holding[name] = (price,quantity)
        self._free_space = 20-len(self._holding)
        if name in self._sold:
            id = self._sold.index(name)
            del self._sold[id]
        else:
            self._ema[name] = (price,ema1,ema2)
        print('*bought {0} at price {1}'.format(x['symbol'],price))
    def sell(self,name,price):
        profit = (float(price)-float(self._holding[name][0]))*self._holding[name][1]
        self._net_profit+=profit
        del self._holding[name]
        self._sold.append(name)
        self._free_space = 20-len(self._holding)
        print('*sold {0} with profit: {1:.2f}'.format(name,profit))
    def update_ema(self,p,P,name,price):
        alpha1 = 2/(p+1)
        alpha2 = 2/(P+1)
        new_ema1 = alpha1*float(price)+(1-alpha1)*float(self._ema[name][1])
        new_ema2 = alpha2*float(price)+(1-alpha2)*float(self._ema[name][2])
        self._ema[name] = (price,new_ema1,new_ema2)
r.authentication.login(username="jz.141001@gmail.com",password="Zhiyuan1010",expiresIn=86400,scope='internal',by_sms=True,store_session=True,mfa_code=None)
today = date.today().strftime("%Y-%m-%d")
timestamp = time.mktime(datetime.strptime(today, "%Y-%m-%d").timetuple())
current_time= datetime.today().strftime("%Y-%m-%d %H:%M:%S")
current_timestamp = time.mktime(datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").timetuple())
mark = current_timestamp
mark1 = current_timestamp
my_stocks = build_holdings()
def EMA(n,N,original_data):
    output_list = []
    alpha1 = 2/(n+1)
    alpha2 = 2/(N+1)
    output_list.append((original_data[0]['begins_at'],float(original_data[0]['close_price']),float(original_data[0]['close_price']),float(original_data[0]['close_price'])))
    reserve_s1 = float(original_data[0]['close_price'])
    reserve_s2 = float(original_data[0]['close_price'])
    for x in original_data[1:]:
        s1 = alpha1*float(x['close_price'])+(1-alpha1)*reserve_s1
        s2 = alpha2*float(x['close_price'])+(1-alpha2)*reserve_s2
        reserve_s1 = s1
        reserve_s2 = s2
        output_list.append((x['begins_at'],float(x['close_price']),s1,s2))
    return output_list
while current_timestamp < timestamp+86400:
    current_time= datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    current_timestamp = time.mktime(datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S").timetuple())
    if current_timestamp%60==0 and mark!=current_timestamp:
        sold = 0
        unrealized_profit = 0
        min = {}
        reserve = []
        print(current_time)
        if current_timestamp<=mark1 + 60:
            for x in r.markets.get_top_movers():
                if x['symbol'] in my_stocks._ema:
                    latest_price = r.stocks.get_latest_price(x['symbol'], priceType=None, includeExtendedHours=True)[0]
                    my_stocks.up`date_ema(p,P,x['symbol'],latest_price) # --> update my_stocks._ema >> {name:(latest_price,ema1,ema2)}
                else:
                    price = r.stocks.get_stock_historicals('{0}'.format(x['symbol']),interval='5minute',span='week')
                    current_ema = EMA(p,P,price)[-1]
                    if current_ema[2]>current_ema[3]:
                        my_stocks._ema[x['symbol']] = (x['last_trade_price'],current_ema[2],current_ema[3])
                print('{0}'.format(x['symbol']),end=' ')
            print()
        else:
            try:
                if len(my_stocks._holding)!=0:
                    for x in my_stocks._ema:
                        latest_price = r.stocks.get_latest_price(x, priceType=None, includeExtendedHours=False)[0]
                        my_stocks.update_ema(p,P,x,latest_price) # --> update my_stocks._ema >> {name:(latest_price,ema1,ema2)}
                        if x in my_stocks._holding:
                            reserve.append(x)
                    for y in reserve:
                        if my_stocks._ema[y][1]<=my_stocks._ema[y][2]:
                            profit = my_stocks.sell(y,my_stocks._ema[y][0])
                if my_stocks._free_space!=0:
                    for x in r.markets.get_top_movers():
                        if x['symbol'] not in reserve and len(my_stocks._holding)<20:
                            if x['symbol'] in my_stocks._sold:
                                ema1 = my_stocks._ema[x['symbol']][1]
                                ema2 = my_stocks._ema[x['symbol']][2]
                                price1 = my_stocks._ema[x['symbol']][0]
                                if ema1>ema2:
                                    my_stocks.buy(x['symbol'],price1,ema1,ema2)
                            else:
                                price = r.stocks.get_stock_historicals('{0}'.format(x['symbol']),interval='5minute',span='week')
                                current_ema = EMA(p,P,price)[-1] # --> (xxx,xxx,ema1,ema2)
                                if current_ema[2]>current_ema[3]:
                                    current_price = r.stocks.get_latest_price(x['symbol'], priceType=None, includeExtendedHours=False)[0]
                                    my_stocks.buy(x['symbol'],current_price,current_ema[2],current_ema[3])
                                    my_stocks.update_ema(p,P,x['symbol'],current_price)
                print('###holding: ',end='')
                for x in my_stocks._holding:
                    current_price1 = r.stocks.get_latest_price(x, priceType=None, includeExtendedHours=False)[0]
                    unrealized_profit += (float(current_price1)-float(my_stocks._holding[x][0]))*float(my_stocks._holding[x][1])
                    print((x,round(float(current_price1),2),round(float(my_stocks._holding[x][0]),2)),end = ',')
                print()
                print('***relized profit: {0:.4f}, ***unrealized_profit: {1:.4f}, ***total = {2:.4f}'.format(my_stocks._net_profit,round(unrealized_profit,4),round(unrealized_profit,4)+my_stocks._net_profit))
                print()
            except :
                print('haha')
                r.authentication.login(username="jz.141001@gmail.com",password="Zhiyuan1010",expiresIn=86400,scope='internal',by_sms=True,store_session=True,mfa_code=None)
    mark = current_timestamp
