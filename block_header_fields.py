from FUK import convert_hex, reverse_bytes, convert_unix


class Block_Header:
    def __init__(self, version, prev_block_hash, merkle_root_hash, timestamp, dif_bits, nonce, tx_counter):
        self.version = reverse_bytes(version)
        self.prev_block_hash = reverse_bytes(prev_block_hash)
        self.merkle_root_hash = reverse_bytes(merkle_root_hash)
        self.timestamp = convert_unix(convert_hex(reverse_bytes(timestamp)))
        self.dif_bits = convert_hex(reverse_bytes(dif_bits))
        self.nonce = convert_hex(reverse_bytes(nonce))
        self.tx_counter = tx_counter

    def print_block_header(self):
        print('version:', self.version)
        print('prev_block_hash:', self.prev_block_hash)
        print('merkle_root_hash:', self.merkle_root_hash)
        print('timestamp:', self.timestamp)
        print('dif_bits:', self.dif_bits)
        print('nonce:', self.nonce)
        print('tx_counter:', self.tx_counter)
        print()
