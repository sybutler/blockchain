from utils import reverse_bytes, convert_hex
from op_codes import OP_CODES


class IO_Parser:
    opcodes = OP_CODES.opcodes

    @staticmethod
    def parse_input(input):
        sig_len = convert_hex(input[0:2])
        sig = input[2:2 + sig_len*2]
        pubkey_len = convert_hex(input[2 + sig_len*2:2 + sig_len*2 + 2])
        pubkey = input[sig_len*2 + 4:]
        return sig, pubkey

    @staticmethod
    def parse_output(output):
        before_ops = []
        output_script, pubkey_hash, op_dup = [-1, -1, False]
        try:
            num_bytes = len(output)/2
            for i in range(int(num_bytes)):
                before_ops.append(IO_Parser.opcodes[output[2*i:2*(i + 1)]])
        except:
            pos = 2*i
            pubkey_hash_len = convert_hex(output[pos:pos + 2])
            pubkey_hash = output[pos + 2: pos + 2 + 2*pubkey_hash_len]
            pos = int((pos + 2 + 2*pubkey_hash_len)/2)

            after_ops = []
            for i in range(pos, int(num_bytes)):
                after_ops.append(IO_Parser.opcodes[output[2*i:2*(i + 1)]])

            if 'OP_DUP' in before_ops:
                op_dup = True
            output_script = '\n'
            for i in range(len(before_ops)):
                output_script = output_script + before_ops[i] + '\n'
            output_script = output_script + pubkey_hash + '\n'
            for i in range(len(after_ops)):
                output_script = output_script + after_ops[i] + '\n'

        return output_script, pubkey_hash, op_dup



