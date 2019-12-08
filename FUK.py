from urllib.request import urlopen
from bs4 import BeautifulSoup

"""Returns the decimal conversion of the specified number of bytes of hex data from the start bit (zero by default)"""
def convert_hex(hex_data):
    return int(hex_data, 16)

def reverse_bytes(hex_data):
    new_hex = ""
    for i in range(int(len(hex_data)/2)):
        new_hex = new_hex + hex_data[len(hex_data) - 1 - 2*i - 1:len(hex_data) - 1 - 2*i + 1]
    return new_hex

def parse_hex(hex_data, field_names, field_bytes):
    start_pos = 0
    field_vals = []
    for i in range(len(field_names)):
        field_vals.append(hex_data[start_pos:start_pos + field_bytes[i]*2])
        start_pos = start_pos + field_bytes[i]*2
    return field_vals

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
q = reverse_bytes(raw_hex)
part_merkle_root = '4570e820145155293685a5c0c4a72dd38ce3971d410055'
# print(q.find(part_merkle_root))
# for i in range(30):
#     print('\n', i)
#     print('four byte quantity:')
#     print(raw_hex[i:i + 64])
    # print(convert_hex(raw_hex, 32, i))

genesis_field_names = ['version', 'previous block', 'merkle root', 'timestamp', 'difficulty target', 'nonce', 'no. tx',
               'version', 'input', 'prev output', 'script length', 'scriptsig', 'sequence', 'outputs', 'no. BTC', 'PK script length',
               'pk script', 'lock time']

genesis_field_bytes = [4, 32, 32, 4, 4, 4, 1, 4, 1, 36, 1, 77, 4, 1, 8, 1, 67, 4]

field_names = ['version', 'prev block hash', 'merkle root hash', 'timestamp', 'difficulty target', 'nonce']

field_bytes = [4, 32, 32, 4, 4, 4]

field_vals = parse_hex(p, field_names, field_bytes)

for i in range(len(field_bytes)):
    print(field_names[i] + ": " + field_vals[i])
    print()

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

