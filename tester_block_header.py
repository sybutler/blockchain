from block_header import BlockHeaderParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
from transaction import TransactionParser
from FUK import convert_float_for_printing



# recent
# url = 'https://blockchain.info/rawblock/00000000000000000008728c89b229864c5c6e85f67e46981d7e605c9d08c700?format=hex'

# the one right before recent
# url = 'https://blockchain.info/rawblock/000000000000000000037de3eb131329d8ebd7697d79e2821754a8f19592fad9?format=hex'

# random 33,000 height block
# url = "https://blockchain.info/rawblock/00000000942725dd706c453fd044c5542f638c02a6982732fcc32e35ae532f10?format=hex"

# random 300,500 height block
url = "https://blockchain.info/rawblock/000000000000000038d7cdcbd44b407f757f30f76f6dbe3d96bd050db3c230df?format=hex"

# getting block hash from cmd line
# url = "https://blockchain.info/rawblock/" + sys.argv[1] + "?format=hex"
# print('querying:', url)

# genesis
# url = "https://blockchain.info/rawblock/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f?format=hex"

try:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    raw_hex = soup.get_text()
except:
    print('Unable to access URL. Please check your block hash')
    exit()


block_header_info, start_pos = BlockHeaderParser.parse_block_header(raw_hex)

block_header_info.print_block_header()
try:
    transactions = TransactionParser.parse_all_block_transactions(raw_hex[start_pos:], block_header_info.tx_counter)
except:
    print('Error: Timeout. The Bitcoin website may be down. Please try again later.')

total_volume = 0

total_fee = 0
total_other = 0
test_reward = 0

for i in range(len(transactions)):

    curr_volume, curr_fee, curr_other = transactions[i].print_tx()

    if i == 0:
        test_reward = curr_volume
    else:
        total_volume += curr_volume
    total_fee += curr_fee
    total_other += curr_other
    print()

print('Transaction Volume:', total_volume)
print('Fee Reward:', total_fee - total_volume)
print('Block Reward:', test_reward)