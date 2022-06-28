from audioop import add
import sys

reg_bin={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101',
        'R6':'110','FLAGS':'111'}

op_code={'add':'10000',
         'sub':'10001',
         'mov_imm':'10010',
         'mov_reg':'10011',
         'ld':'10100',
         'st':'10101',
         'mul':'10110',
         'div':'10111',
         'rs':'11000',
         'ls':'11001',
         'xor':'11010',
         'or':'11011',
         'and':'11100',
         'not':'11101',
         'cmp':'11110',
         'jmp':'11111',
         'jlt':'01100',
         'jgt':'01101',
         'je':'01111',
         'hlt':'01010'}

inst_type={'add':'A',
         'sub':'A',
         'mov_imm':'B',
         'mov_reg':'C',
         'ld':'D',
         'st':'D',
         'mul':'A',
         'div':'C',
         'rs':'B',
         'ls':'B',
         'xor':'A',
         'or':'A',
         'and':'A',
         'not':'C',
         'cmp':'C',
         'jmp':'E',
         'jlt':'E',
         'jgt':'E',
         'je':'E',
         'hlt':'F'}


def add_inst(inst):
    s='10000'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)



assemb_inst=sys.stdin.read()

lines=assemb_inst.split('\n')
lines=lines[:-1]

for i in lines:
    
    inst=i.split()
    # print(inst[0])
    # for j in inst:
    #     print(j)

    if(inst[0]=='add'):
        add_inst(inst)
