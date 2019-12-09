from block_header import BlockHeaderParser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from transaction import TransactionParser


# recent
# url = 'https://blockchain.info/rawblock/00000000000000000008728c89b229864c5c6e85f67e46981d7e605c9d08c700?format=hex'

# the one right before recent
# url = 'https://blockchain.info/rawblock/000000000000000000037de3eb131329d8ebd7697d79e2821754a8f19592fad9?format=hex'

# random 33,000 height block
# url = "https://blockchain.info/rawblock/00000000942725dd706c453fd044c5542f638c02a6982732fcc32e35ae532f10?format=hex"

# random 300,500 height block
url = "https://blockchain.info/rawblock/000000000000000038d7cdcbd44b407f757f30f76f6dbe3d96bd050db3c230df?format=hex"


# genesis
# url = "https://blockchain.info/rawblock/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f?format=hex"


html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()


block_header_info, start_pos = BlockHeaderParser.parse_block_header(raw_hex)
block_header_info.print_block_header()

transactions = TransactionParser.parse_all_block_transactions(raw_hex[start_pos:], block_header_info.tx_counter)
print(len(transactions))
total = 0
for i in range(len(transactions)):

    total += transactions[i].print_tx()
    print()

print(total)