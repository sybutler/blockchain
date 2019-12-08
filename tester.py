from FUK import reverse_bytes, convert_hex
from transaction_fields import Transaction
from transaction_fields import TxIn
from transaction_fields import TxOut
from transaction import TransactionParser
from urllib.request import urlopen
from bs4 import BeautifulSoup

# url = 'https://blockchain.info/rawtx/45bf99a6d2caa6fe092cdb77d9fd3364ada30133c7c8d01e86eaf10682168d70?format=hex' # OG
# url = 'https://blockchain.info/rawtx/fe6c48bbfdc025670f4db0340650ba5a50f9307b091d9aaa19aa44291961c69f?format=hex' # weird zeroes one
# url = 'https://blockchain.info/rawtx/a8d0c0184dde994a09ec054286f1ce581bebf46446a512166eae7628734ea0a5?format=hex'  # coinbase
# url = 'https://blockchain.info/rawtx/0de586d0c74780605c36c0f51dcd850d1772f41a92c549e3aa36f9e78e905284?format=hex'
url = 'https://blockchain.info/rawtx/ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f?format=hex'

html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()

# raw_hex = '01000000000101d553fbabaf1b26977b6e5d403af9f4b567b3e28484321a6fb02e2824984e3e5000000000171600142b2296c588ec413cebd19c3cbc04ea830ead6e78ffffffff01be1611020000000017a91487e4e5a7ff7bf78b8a8972a49381c8a673917f3e870247304402205f39ccbab38b644acea0776d18cb63ce3e37428cbac06dc23b59c61607aef69102206b8610827e9cb853ea0ba38983662034bd3575cc1ab118fb66d6a98066fa0bed01210304c01563d46e38264283b99bb352b46e69bf132431f102d4bd9a9d8dab075e7f00000000'

tx_info = TransactionParser.parse_transaction(raw_hex)
tx_info.print_tx()