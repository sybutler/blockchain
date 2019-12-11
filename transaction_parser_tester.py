from transaction import TransactionParser
from urllib.request import urlopen
from bs4 import BeautifulSoup

# url = 'https://blockchain.info/rawtx/45bf99a6d2caa6fe092cdb77d9fd3364ada30133c7c8d01e86eaf10682168d70?format=hex' # OG
url = 'https://blockchain.info/rawtx/fe6c48bbfdc025670f4db0340650ba5a50f9307b091d9aaa19aa44291961c69f?format=hex' # weird zeroes one: INPUT IS TYPE 3!
# url = 'https://blockchain.info/rawtx/a8d0c0184dde994a09ec054286f1ce581bebf46446a512166eae7628734ea0a5?format=hex'  # coinbase
# url = 'https://blockchain.info/rawtx/0de586d0c74780605c36c0f51dcd850d1772f41a92c549e3aa36f9e78e905284?format=hex'
# url = 'https://blockchain.info/rawtx/ee475443f1fbfff84ffba43ba092a70d291df233bd1428f3d09f7bd1a6054a1f?format=hex'
# url = 'https://blockchain.info/rawtx/e69ceee20e0e487882393a6882c0e6720e1a98fd77d215cc658d896ab29ba020?format=hex'
# url = 'https://blockchain.info/rawtx/0d5238c83599d7dc40eabef05f7a6cf66518e78375ab5bb7e84612ea73329f64?format=hex' # weird one... no 1 or 3 on input
# url = 'https://blockchain.info/rawtx/f6b382d31d8ec48cb273300287b753773b677ace769277eb073bf7301a5a2955?format=hex'
# url = 'https://blockchain.info/rawtx/80975cddebaa93aa21a6477c0d050685d6820fa1068a2731db0f39b535cbd369?format=hex'

html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
raw_hex = soup.get_text()

tx_info, num_txns = TransactionParser.parse_transaction(raw_hex)
for input in tx_info.inputs:
    print(input.address)
for output in tx_info.outputs:
    print(output.address)
