# prints immo to ecu communication with format, lines in test1 correspond to :
# white -> immo to ecu bytes
# green -> immo to ecu correct challenge response
# yellow -> ecu to immo bytes
# blue -> ecu to immo opcode
# red -> ecu to immo msg checkcsum

from termcolor import colored
tests = []  # int array
tests_strings = [] # str array
with open("k-line_sniff/test1") as f:
    for l in f:
        x = [int(i) for i in l.split(" ")]
        tests.append(x)

        x = [hex(int(i)) for i in l.split(" ")]
        tests_strings.append(x)

t1 = tests[1]
t1_strings = tests_strings[1]

# ecu puzzle bytes
pzl1 = 0
pzl2 = 0
pzl3 = 0

# immo sended bytes

immo1 = 0
immo2 = 0
immo3 = 0

c = 0
for i in range(4,len(t1)):
    checksum = sum(t1[i-4:i]) % 0x100
    if checksum == t1[i]:
        # colorize
        t1_strings[i-4] = colored(t1_strings[i-4], "yellow") # data 1
        t1_strings[i-3] = colored(t1_strings[i-3], "yellow") # data2
        t1_strings[i-2] = colored(t1_strings[i-2], "blue") # opcode
        t1_strings[i-1] = colored(t1_strings[i-1], "yellow") # data3
        t1_strings[i] = colored(t1_strings[i], "red") # checksum

        opcode = t1[i-2]
        if opcode == 0x43: # puzle send
            pzl1 = t1[i-4]
            pzl2 = t1[i-3]
            pzl3 = t1[i-1]
        elif opcode == 0x47: # colorize green correct challenge response
            if c == 0:
                if t1[i-5] == (( int ((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) / 0x1000 )) + 0x80):
                    t1_strings[i-5] = colored(t1_strings[i-5], "green")
            elif c == 1:
                if t1[i-5] == ((( int ((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) / 0x40 )) % 0x40 ) + 0x80):
                    t1_strings[i-5] = colored(t1_strings[i-5], "green")
            elif c == 2:
                if t1[i - 5] == (((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) % 0x40 ) + 0x80):
                    t1_strings[i - 5] = colored(t1_strings[i - 5], "green")
            c += 1


out1 = ( int ((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) / 0x1000 )) + 0x80
out2 = (( int ((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) / 0x40 )) % 0x40 ) + 0x80
out3 = ((( pzl1 * pzl2 ) + ( pzl1 * pzl3 ) + ( pzl2 * pzl3 )) % 0x40 ) + 0x80
print(hex(out1), end=" ")
print(hex(out2), end=" ")
print(hex(out3))

for s in t1_strings:
    print(s, end=" ")