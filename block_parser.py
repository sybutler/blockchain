from block_header import BlockHeaderParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
from transaction import TransactionParser


# block_hash = sys.argv[1]
block_hash = '000000000000000038d7cdcbd44b407f757f30f76f6dbe3d96bd050db3c230df'
url = "https://blockchain.info/rawblock/" + block_hash + "?format=hex"


try:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    raw_hex = soup.get_text()
except:
    print('Unable to access URL. Please check your block hash')
    exit()


block_header_info, start_pos = BlockHeaderParser.parse_block_header(raw_hex)
print()
print('Block Header:')
block_header_info.print_block_header()
try:
    transactions = TransactionParser.parse_all_block_transactions(raw_hex[start_pos:], block_header_info.tx_counter)
except:
    print('Error: Timeout. The Bitcoin website may be down. Please try again later.')
    sys.exit()

total_volume = 0

total_fee = 0
total_other = 0
test_reward = 0

print()
for i in range(len(transactions)):

    curr_volume, curr_fee, curr_other = transactions[i].print_tx()

    if i == 0:
        test_reward = curr_volume
    else:
        total_volume += curr_volume
    total_fee += curr_fee
    total_other += curr_other
    print()

print('====================================')
print('Final Block Info...')
print('Transaction Volume:', total_volume)
print('Fee Reward:', total_fee - total_volume)
print('Block Reward:', test_reward)