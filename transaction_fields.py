from FUK import convert_hex, reverse_bytes, convert_float_for_printing

class TxIn:
    def __init__(self, prev_txid, index, script_length, input_script, sequence, value):
        self.previous_txid_hash = reverse_bytes(prev_txid)
        self.index_of_prev_txid_hash = convert_hex(reverse_bytes(index))
        self.script_length = script_length
        self.input_script = input_script
        self.sequence = sequence
        self.value = value

    def print_txIn(self):
        # print('previous txid hash:', self.previous_txid_hash)
        # print('index:', self.index_of_prev_txid_hash)
        # print('script length:', self.script_length)
        # print('input script:', self.input_script)
        # print('sequence:', self.sequence)
        # print('value:', self.value)
        return self.value

    def get_value(self):
        return self.value


class TxOut:
    def __init__(self, value, script_length, output_script):
        self.value = value
        self.script_length = script_length
        self.output_script = output_script

    def print_txOut(self):
        # print('value:', self.value)
        # print('script length:', self.script_length)
        # print('output script:', self.output_script)
        return self.value


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
            # print('version:', self.version)
            # print()
            # print('COINBASE')
            # print()
            # print('output count:', self.output_count)
            for i in range(self.output_count):
                # print()
                # print('outputs:', self.outputs[i])
                total_output += self.outputs[i].print_txOut()  # sums outputs and prints individual output
            # print()
            # print('lock time:', self.timelock)
            # print('total output:', total_output)
            # print('fee:', convert_float_for_printing(total_output_of_inputs - total_output))
            return total_output, total_output_of_inputs



        # print('version:', self.version)
        # print()
        # print('input count:', self.input_count)
        for i in range(self.input_count):
            # print()
            # print('inputs:', self.inputs[i])
            total_output_of_inputs += self.inputs[i].print_txIn()
        # print()
        # print('output count:', self.output_count)
        for i in range(self.output_count):
            # print()
            # print('outputs:', self.outputs[i])
            total_output += self.outputs[i].print_txOut()  # sums outputs and prints individual output
        # print()
        # print('lock time:', self.timelock)
        # print('total output:', total_output)
        # print('fee:', convert_float_for_printing(total_output_of_inputs - total_output))
        print('fee:', total_output_of_inputs - total_output)
        return total_output, total_output_of_inputs, total_output_of_inputs- total_output
