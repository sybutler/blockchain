from urllib.request import urlopen
from bs4 import BeautifulSoup
from utils import reverse_bytes, convert_hex
from transaction_fields import Transaction
from transaction_fields import TxIn
from transaction_fields import TxOut
import hashlib
from hashlib import sha256
import binascii

class TransactionParser:

    @staticmethod
    # hex_data is entire block hash *minus* block header hash
    def parse_all_block_transactions(hex_data, num_transactions):
        transactions = []

        for i in range(num_transactions):
            transaction, updated_starting_point = TransactionParser.parse_transaction(hex_data)
            transactions.append(transaction)
            transaction.print_tx()
            print('==============')
            hex_data = hex_data[updated_starting_point:]

        return transactions



    @staticmethod
    def parse_transaction(hex_data):
        transaction_bytes = [4, 1, -1, 1, -2, 4]
        fields = ['version', 'input count', 'txIns',
                  'output count', 'txOuts', 'timelock']
        start_pos = 0
        field_vals = dict()
        for i in range(len(fields)):
            if fields[i] is 'input count' or fields[i] is 'output count':
                field_vals[fields[i]] = hex_data[start_pos:start_pos + transaction_bytes[i] * 2]
                start_pos = start_pos + transaction_bytes[i] * 2
                if convert_hex(field_vals[fields[i]]) == 253:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 4])
                    start_pos = start_pos + 4
                elif convert_hex(field_vals[fields[i]]) == 254:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 8])
                    start_pos = start_pos + 8
                elif convert_hex(field_vals[fields[i]]) == 255:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 16])
                    start_pos = start_pos + 16

            elif fields[i] is 'txIns':
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
                           field_vals['timelock']), start_pos

    @staticmethod
    def parse_transactions_for_indexed_output(hex_data, index):

        transaction_bytes = [4, 1, -1, 1, -2, 4]
        fields = ['version', 'input count', 'txIns',
                  'output count', 'txOuts', 'timelock']
        start_pos = 0
        field_vals = dict()
        for i in range(len(fields)):

            if fields[i] is 'input count' or fields[i] is 'output count':
                field_vals[fields[i]] = hex_data[start_pos:start_pos + transaction_bytes[i] * 2]
                start_pos = start_pos + transaction_bytes[i] * 2
                if convert_hex(field_vals[fields[i]]) == 253:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 4])
                    start_pos = start_pos + 4
                elif convert_hex(field_vals[fields[i]]) == 254:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 8])
                    start_pos = start_pos + 8
                elif convert_hex(field_vals[fields[i]]) == 255:
                    field_vals[fields[i]] = reverse_bytes(hex_data[start_pos:start_pos + 16])
                    start_pos = start_pos + 16

            elif fields[i] is 'txIns':
                txIns, offset = TransactionParser.parse_txIns_dummy(convert_hex(field_vals['input count']),
                                                                    hex_data[start_pos:])
                field_vals[fields[i]] = txIns
                start_pos = start_pos + offset
            elif fields[i] is 'txOuts':
                txOuts, offset = TransactionParser.parse_txOuts(convert_hex(field_vals['output count']),
                                                                hex_data[start_pos:])
                field_vals[fields[i]] = txOuts
                # print(txOuts)
                start_pos = start_pos + offset
            else:
                field_vals[fields[i]] = hex_data[start_pos:start_pos + transaction_bytes[i] * 2]
                start_pos = start_pos + transaction_bytes[i] * 2

        return txOuts[int(index)].value

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
            if prev_txid == '0000000000000000000000000000000000000000000000000000000000000000':  # coinbase
                txIns.append(TxIn(prev_txid, index, script_length, input_script, sequence, -1))  # -1 put in for value in coinbase
            else:
                value = TransactionParser.get_TxIn_value(prev_txid, index)
                txIns.append(TxIn(prev_txid, index, script_length, input_script, sequence, value))
        return txIns, start_pos

    @staticmethod
    def parse_txIns_dummy(num_txIns, hex_data):
        txIn_bytes = [32, 4, 1, -1, 4]
        txIns = []
        start_pos = 0
        for i in range(num_txIns):
            txIn_fields = []
            for j in range(len(txIn_bytes)):
                txIn_fields.append(hex_data[start_pos:start_pos + txIn_bytes[j] * 2])
                start_pos = start_pos + txIn_bytes[j] * 2
                if j == 2:
                    txIn_bytes[j + 1] = convert_hex(txIn_fields[j])
            prev_txid, index, script_length, input_script, sequence = txIn_fields
            txIns.append(TxIn(prev_txid, index, script_length, input_script, sequence, 0))
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
            value = convert_hex(reverse_bytes(value)) / 100000000
            txOuts.append(TxOut(value, script_length, output_script))
        return txOuts, start_pos

    @staticmethod
    def get_address(pubkey):
        pk = binascii.hexlify(bytes(pubkey, 'utf-8'))
        h = hashlib.new('ripemd160')
        adr = h.update(sha256(pk).digest()).hexdigest()
        adr = '00' + adr
        return adr

    @staticmethod
    def get_TxIn_value(hash_, index):

        index = convert_hex((reverse_bytes(index)))
        hash_ = reverse_bytes(hash_)


        url = 'https://blockchain.info/rawtx/' + hash_ + '?format=hex'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        raw_hex = soup.get_text()


        return TransactionParser.parse_transactions_for_indexed_output(raw_hex, index)

