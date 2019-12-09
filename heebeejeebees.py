import decimal

ctx = decimal.Context()

ctx.prec = 20

x = 0.000499999

fee_to_print = format(ctx.create_decimal(repr(x)), 'f')

for i in range(len(fee_to_print)-2):

    # print(fee_to_print[i:i+3])
    if fee_to_print[i:i+3] == '999':
        fee_to_print = fee_to_print[:i]
        break

fee_to_print = fee_to_print[:len(fee_to_print)-1] + str(int(fee_to_print[-1]) + 1)
dec_point = fee_to_print.index('.')
while len(fee_to_print[dec_point:]) <= 8:
    fee_to_print = fee_to_print + '0'
print(fee_to_print)