
class TxIn:
    def __init__(self, prev_txid, index, script_length, input_script, sequence):
        self.previous_txid_hash = prev_txid
        self.index_of_prev_txid_hash = index
        self.script_length = script_length
        self.input_script = input_script
        self.sequence = sequence


class TxOut:
    def __init__(self, value, script_length, output_script):
        self.value = value
        self.script_length = script_length
        self.output_script = output_script


class Transaction:
    def __init__(self, version, input_count, txIn_list, output_count, txOut_list, timelock):
        self.version = version
        self.input_count = input_count
        self.inputs = txIn_list
        self.output_count = output_count
        self.outputs = txOut_list
        self.timelock = timelock

