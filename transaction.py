from FUK import reverse_bytes, convert_hex
from transaction_fields import Transaction
from transaction_fields import TxIn
from transaction_fields import TxOut


class TransactionParser:

    @staticmethod
    def parse_transaction(hex_data):
        transaction_bytes = [4, 1, -1, 1, -2, 4]
        fields = ['version', 'input count', 'txIns',
                  'output count', 'txOuts', 'timelock']
        start_pos = 0
        field_vals = dict()
        for i in range(len(fields)):
            if fields[i] is 'txIns':
                txIns, offset = TransactionParser.parse_txIns(convert_hex(field_vals['input count']), hex_data[start_pos:])
                field_vals[fields[i]] = txIns
                start_pos = start_pos + offset
            elif fields[i] is 'txOuts':
                txOuts, offset = TransactionParser.parse_txOuts(convert_hex(field_vals['output count']), hex_data[start_pos:])
                field_vals[fields[i]] = txOuts
                start_pos = start_pos + offset
            else:
                field_vals[fields[i]] = hex_data[start_pos:start_pos + transaction_bytes[i]*2]
                start_pos = start_pos + transaction_bytes[i]*2
        return Transaction(field_vals['version'],
                           field_vals['input count'],
                           field_vals['txIns'],
                           field_vals['output count'],
                           field_vals['txOuts'],
                           field_vals['timelock'])

    @staticmethod
    def parse_txIns(num_txIns, hex_data):
        txIn_bytes = [32, 4, 1, -1, 4]
        txIns = []
        start_pos = 0
        for i in range(num_txIns):
            txIn_fields = []
            for j in range(len(txIn_bytes)):
                txIn_fields.append(hex_data[start_pos:start_pos + txIn_bytes[j]*2])
                start_pos = start_pos + txIn_bytes[j]*2
                if j == 2:
                    txIn_bytes[j + 1] = convert_hex(txIn_fields[j])
            prev_txid, index, script_length, input_script, sequence = txIn_fields
            txIns.append(TxIn(prev_txid, index, script_length, input_script, sequence))
        return txIns, start_pos

    @staticmethod
    def parse_txOuts(num_txOuts, hex_data):
        txOut_bytes = [8, 1, -1]
        txOuts = []
        start_pos = 0
        for i in range(num_txOuts):
            txOut_fields = []
            for j in range(len(txOut_bytes)):
                txOut_fields.append(hex_data[start_pos:start_pos + txOut_bytes[j] * 2])
                start_pos = start_pos + txOut_bytes[j] * 2
                if j == 1:
                    txOut_bytes[j + 1] = convert_hex(txOut_fields[j])
            value, script_length, output_script = txOut_fields
            txOuts.append(TxOut(value, script_length, output_script))
        return txOuts, start_pos

# TODO before adding fields to objects, reverse endian and convert to decimal if necessary
# TODO other transaction testing - segwit?
# TODO coinbase transactions
# TODO varint implementation: https://bitcoin.stackexchange.com/questions/40451/how-does-the-variable-length-integer-work/58416