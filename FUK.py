from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://blockchain.info/rawblock/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f?format=hex"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()

txs = raw_hex[80:]
print(txs[0:2])
print(int(txs[0], 16))

'''Returns the decimal conversion of the specified number of bytes of
 hex data from the start bit (zero by default)'''
def convert(hex_data, num_bytes, start_bit=0):
    return int(hex_data[start_bit:num_bytes*2], 16)
