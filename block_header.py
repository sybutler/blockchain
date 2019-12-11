from utils import reverse_bytes, convert_hex
from block_header_fields import Block_Header


class BlockHeaderParser:

    @staticmethod
    def parse_block_header(hex_data):   # returns Block_Header object with the below fields, final value of start_pos
        transaction_bytes = [4, 32, 32, 4, 4, 4, -1]
        fields = ['version', 'prev_block_hash', 'merkle_root_hash',
                  'timestamp', 'dif_bits', 'nonce', 'tx_counter']
        start_pos = 0
        field_vals = dict()
        for i in range(len(fields)):

            field_vals[fields[i]] = hex_data[start_pos:start_pos + transaction_bytes[i] * 2]
            start_pos = start_pos + transaction_bytes[i]*2

            if fields[i] is 'tx_counter':

                # weird - but getting a byte that shouldn't be there. for now, quick fix...
                start_pos = start_pos + 2

                first_byte = hex_data[start_pos:start_pos + 2]
                start_pos = start_pos + 2

                first_byte = convert_hex(first_byte)

                if first_byte < 253:
                    field_vals[fields[i]] = first_byte

                elif first_byte == 253:
                    next_bytes = hex_data[start_pos:start_pos + 4]
                    field_vals[fields[i]] = convert_hex(reverse_bytes(next_bytes))
                    start_pos = start_pos + 4

                elif first_byte == 254:
                    next_bytes = hex_data[start_pos:start_pos + 8]
                    field_vals[fields[i]] = convert_hex(reverse_bytes(next_bytes))
                    start_pos = start_pos + 8

                elif first_byte == 255:
                    next_bytes = hex_data[start_pos:start_pos + 16]
                    field_vals[fields[i]] = convert_hex(reverse_bytes(next_bytes))
                    start_pos = start_pos + 16

        return Block_Header(field_vals['version'],
                            field_vals['prev_block_hash'],
                            field_vals['merkle_root_hash'],
                            field_vals['timestamp'],
                            field_vals['dif_bits'],
                            field_vals['nonce'],
                            field_vals['tx_counter']), start_pos
