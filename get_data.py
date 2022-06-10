from urllib.request	import urlopen
from bs4 import	BeautifulSoup
import json
import re
import csv
import datetime
import time
one_more = True
while one_more == True:
    Check = False
    while Check == False:
        try:
            whichstock = input("which stock are yuo looking for? : ")
            print('please input the date ')
            year = input("year: ")
            month = input("month: ")
            day = input("day: ")
            from_ = "{0}-{1}-{2}".format(year,month,day)
            td = datetime.date.today()
            today = time.mktime(datetime.datetime.strptime(str(td), "%Y-%m-%d").timetuple())
            from_date = time.mktime(datetime.datetime.strptime(from_, "%Y-%m-%d").timetuple())
            Check = True
            html = urlopen(("https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(whichstock,int(from_date),int(today))))
            soup = BeautifulSoup(html,"html.parser")
            Check = True
        except:

            print('invalide input, try agian')

    for x in soup.body.findAll("script"):
        if "HistoricalPriceStore" in str(x):
            info = str(x)
    Info = re.findall("root.App.main = (.+})",info)
    for n in Info:
        if len(n)>=0:
            data = json.loads(n)
    data_history = data["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]["prices"][::-1]
    for x in data_history:
        dt_object = datetime.date.fromtimestamp(x['date'])
        x['date']=dt_object
        print(x)

    data_store= open(r"C:\Users\johnk\OneDrive\Desktop\project\SASUniversityEdition\myfolders\{0}.csv".format(whichstock),"wt")
    writer = csv.writer(data_store)
    writer.writerow(data_history[1].keys())
    for x in data_history:
        if "open" in x:
            writer.writerow(x.values())
    data_store.close()
    print('***data of {0} from {1} to {2} is been saved***'.format(whichstock,from_,data_history[-1]['date']).upper())
    print()
    onemore = input('do you want to check one more?(yes--> Y, no-->N): '.upper()).upper()
    if onemore == "N":
        one_more = False
