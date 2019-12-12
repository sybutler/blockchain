from datetime import datetime
from base58 import b58encode
from hashlib import sha256
import hashlib



# Returns the decimal conversion of the specified number of bytes of hex data from the start bit (zero by default)
def convert_hex(hex_data):
    return int(hex_data, 16)


# converts unix time stamp in hex to a datetime (timezone...?)
def convert_unix(unix_time):
    return datetime.fromtimestamp(unix_time)

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

# def convert_float_for_printing(x):
#
#     if x < 0:
#         return '0.00000000'
#
#     # ctx = decimal.Context()
#
#     fee_to_print = format(ctx.create_decimal(repr(x)), 'f')
#     if fee_to_print == '0.0':
#         return '0.00000000'
#     if (len(fee_to_print)) < 5:
#         return fee_to_print
#
#     for i in range(len(fee_to_print) - 2):
#
#         # print(fee_to_print[i:i+3])
#         if fee_to_print[i:i + 3] == '999':
#             fee_to_print = fee_to_print[:i]
#             break
#
#     fee_to_print = fee_to_print[:len(fee_to_print) - 1] + str(int(fee_to_print[-1]) + 1)
#     dec_point = fee_to_print.index('.')
#     while len(fee_to_print[dec_point:]) <= 8:
#         fee_to_print = fee_to_print + '0'
#     return fee_to_print

def double_sha256(hexstr):
    bytes_ext_pubkey = bytes.fromhex(hexstr)
    return sha256(sha256(bytes_ext_pubkey).digest()).hexdigest()

def get_output_address(hashed_pubkey, op_dup):
    if op_dup:
        prefix = '00'
    else:
        prefix = '05'
    ext_pubkey = prefix + hashed_pubkey
    hash = double_sha256(ext_pubkey)
    bin_adr = bytes.fromhex(ext_pubkey + hash[:8])
    return b58encode(bin_adr).decode()

def get_input_address(pubkey, op_dup):
    bytes_pubkey = bytes.fromhex(pubkey)
    h = hashlib.new('ripemd160')
    h.update(sha256(bytes_pubkey).digest())
    return get_output_address(h.hexdigest(), op_dup)