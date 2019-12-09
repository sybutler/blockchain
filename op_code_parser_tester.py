import re
with open("op_codes_fixed.txt", 'a') as g:
    with open("op_codes_test.txt", 'r+') as f:
        for i in range(132):
            line = f.readline()
            # print(line)
            if line is not '':
                line = re.split(" |\n|,|x", line)
                if len(line) > 2:
                    new_line = "\'" + line[3] + '\'' + ":" + line[0] + ",\n"
                    print(new_line)
                    g.write(new_line)