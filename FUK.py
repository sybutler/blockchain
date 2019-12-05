from urllib.request import urlopen
from bs4 import BeautifulSoup

"""Returns the decimal conversion of the specified number of bytes of hex data from the start bit (zero by default)"""
def convert_hex(hex_data, num_bytes, offset=0):
    return int(hex_data[offset:offset + num_bytes*2], 16)

def n(label, s, i):
    print(label, s[:i])
    return s[i:]

# genesis block
# url = "https://blockchain.info/rawblock/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f?format=hex"

# just some recent block
url = 'https://blockchain.info/rawblock/00000000000000000008728c89b229864c5c6e85f67e46981d7e605c9d08c700?format=hex'

html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()

txs = raw_hex[80:]

p = raw_hex


print(raw_hex.find('4570e820145155293685a5c0c4a72dd38ce3971d410055'))
# for i in range(30):
#     print('\n', i)
#     print('four byte quantity:')
#     print(raw_hex[i:i + 64])
    # print(convert_hex(raw_hex, 32, i))

# print('\nHEADER')
# p = n('block size', p, 8)
# p = n('version', p, 8)
# p = n('previous block', p, 64)
# p = n('merkle root:', p, 64)
# p = n('timestamp', p, 8)
# p = n('difficulty target', p, 8)
# p = n('nonce', p, 8)
# p = n('number of transactions', p, 2)  # can range from 1-9 bytes
#
# p = n('version', p, 8)
# p = n('input', p, 2)  # 1-9 bytes
# p = n('prev output', p, 72)
# p = n('script length', p, 2)
# p = n('scriptsig', p, 154)
# p = n('sequence', p, 8)
# p = n('outputs', p, 2)
# p = n('num BTC?', p, 16)
# p = n('pk_script length', p, 2)
# p = n('pk_script', p, 134)
# p = n('lock time', p, 8)





# print('version:', p[:8])
# p = p[8:]
# print('previous block:', p[:64])
# p = p[64:]
# print('merkle root:', p[:64])
# p = p[64:]

