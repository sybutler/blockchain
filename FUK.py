from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://blockchain.info/rawblock/0000000000000000000af1a5baef627412f1774dbf9f37ed7e16c9c923f66897?format=hex"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()

txs = raw_hex[80:]
print(raw_hex[0])
print(int(raw_hex[0]))