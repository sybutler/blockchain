from utils import convert_hex, reverse_bytes, get_output_address, get_input_address, double_sha256
from input_output_parser import IO_Parser

class TxIn:
    def __init__(self, prev_txid, index, script_length, input_script, sequence, value):
        self.previous_txid_hash = reverse_bytes(prev_txid)
        self.index_of_prev_txid_hash = convert_hex(reverse_bytes(index))
        self.script_length = script_length
        self.input_script = input_script
        self.sequence = sequence
        self.value = value
        self.signature = None
        self.pubkey = None
        self.address = None
        if self.value != -1:        # if not coinbase tx
            self.get_script_info()

    def print_txIn(self):
        print('previous txid hash:', self.previous_txid_hash)
        print('index:', self.index_of_prev_txid_hash)
        print('script length:', self.script_length)
        print('input script:', self.input_script)
        print('sequence:', self.sequence)
        print('value:', self.value)
        print('signature:', self.signature)
        print('pubkey:', self.pubkey)
        print('address:', self.address)
        return self.value

    def get_addends_txIn(self):
        return self.value

    def get_value(self):
        return self.value

    def get_script_info(self):
        self.signature, self.pubkey = IO_Parser.parse_input(self.input_script)
        self.address = get_input_address(self.pubkey, True)


class TxOut:
    def __init__(self, value, script_length, output_script):
        self.value = value
        self.script_length = script_length
        self.output_script = output_script
        self.pubkey_hash = None
        self.address = None
        self.get_script_info()

    def print_txOut(self):
        print('value:', self.value)
        print('script length:', self.script_length)
        print('output script:', self.output_script)
        print('pubkey hash:', self.pubkey_hash)
        print('address:', self.address)
        return self.value

    def get_addends_txOut(self):
        return self.value

    def get_script_info(self):
        self.output_script, self.pubkey_hash, op_dup = IO_Parser.parse_output(self.output_script)
        self.address = get_output_address(self.pubkey_hash, op_dup)



class Transaction:
    def __init__(self, version, input_count, txIn_list, output_count, txOut_list, timelock):
        self.version = version
        self.input_count = convert_hex(reverse_bytes(input_count))
        self.inputs = txIn_list
        self.output_count = convert_hex(reverse_bytes(output_count))
        self.outputs = txOut_list
        self.timelock = convert_hex(reverse_bytes(timelock))

    def print_tx(self):

        total_output = 0
        total_output_of_inputs = 0

        if self.inputs[0].get_value() == -1:
            print('version:', self.version)
            print()
            print('COINBASE')
            print()
            print('output count:', self.output_count)
            for i in range(self.output_count):
                print()
                print('outputs:', self.outputs[i])
                total_output += self.outputs[i].print_txOut()  # sums outputs and prints individual output
            print()
            print('lock time:', self.timelock)
            print('total output:', total_output)
            # print('fee:', convert_float_for_printing(total_output_of_inputs - total_output))
            print('fee:', total_output_of_inputs - total_output)
            return total_output, total_output_of_inputs, 0



        print('version:', self.version)
        print()
        print('input count:', self.input_count)
        for i in range(self.input_count):
            print()
            print('inputs:', self.inputs[i])
            total_output_of_inputs += self.inputs[i].print_txIn()
        print()
        print('output count:', self.output_count)
        for i in range(self.output_count):
            print()
            print('outputs:', self.outputs[i])
            total_output += self.outputs[i].print_txOut()  # sums outputs and prints individual output
        print()
        print('lock time:', self.timelock)
        print('total output:', total_output)
        # print('fee:', convert_float_for_printing(total_output_of_inputs - total_output))
        print('fee:', total_output_of_inputs - total_output)
        return total_output, total_output_of_inputs, total_output_of_inputs- total_output

    def get_addends(self):
        total_output = 0
        total_output_of_inputs = 0

        if self.inputs[0].get_value() == -1:
            for i in range(self.output_count):
                total_output += self.outputs[i].get_addends_txOut()  # sums outputs and prints individual output

            return total_output, total_output_of_inputs, 0

        for i in range(self.input_count):

            total_output_of_inputs += self.inputs[i].get_addends_txIn()
        for i in range(self.output_count):

            total_output += self.outputs[i].get_addends_txOut()  # sums outputs and prints individual output

        # print('fee:', convert_float_for_printing(total_output_of_inputs - total_output))
        return total_output, total_output_of_inputs, total_output_of_inputs - total_output