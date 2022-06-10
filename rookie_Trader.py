#https://pypi.org/project/yfinance/
#https://www.programiz.com/python-programming/csv
#https://github.com/ine-rmotr-curriculum/FreeCodeCamp-Pandas-Real-Life-Example/blob/master/Lecture_1.ipynb
#https://realpython.com/beautiful-soup-web-scraper-python/class
import yfinance as yf
from urllib.request	import urlopen, Request
from bs4 import	BeautifulSoup
import gzip
import time
start_time = time.time()
url = 'https://finance.yahoo.com/trending-tickers'
req = Request(url)
decompress_html = gzip.decompress(urlopen(req).read()).decode('utf-8')
soup = BeautifulSoup(decompress_html,"html.parser")
Top_Mover = {}
for x in soup.body.tbody.find_all("tr"):
    for y in x.find_all("td"):
        if y['aria-label']=='Symbol':
            Top_Mover[y.text] = []
            ticker = y.text
        if y['aria-label']=='Last Price':
            Top_Mover[ticker].append(y.text)
        if y['aria-label']=='% Change':
            Top_Mover[ticker].append(y.text)
for x in Top_Mover:
    print(x,Top_Mover[x])

print(" %s second " %(time.time()-start_time))
