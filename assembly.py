
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

mem_addr=[]
var_addr=[]

def decimaltobinary(s):
    s1=""
    n=int(s)
    while n>0:
        s1+=str(n%2)
        n=n//2
    res=s1[::-1]
    return res

def add_inst(inst):
    s='10000'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def sub_inst(inst):
    s='10001'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def mov_reg_inst(inst):
    s='10011'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    print(s)

def mov_imm_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)

    s='10010'
    s=s+reg_bin[inst[1]]+'0'*a+t
    print(s)

def ld_inst(inst):
    s='10100'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[2]):
                a=i[-1]
    s=s+reg_bin[inst[1]]+a
    print(s)

def st_inst(inst):
    s='10101'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[2]):
                a=i[-1]
    s=s+reg_bin[inst[1]]+a
    print(s)


def mul_inst(inst):
    s='10110'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def div_inst(inst):
    s='10111'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    print(s)

def rs_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11000'
    s=s+reg_bin[inst[1]]+'0'*a+t
    print(s)

def ls_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11001'
    s=s+reg_bin[inst[1]]+'0'*a+t
    print(s)

def xor_inst(inst):
    s='11010'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def or_inst(inst):
    s='11011'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def and_inst(inst):
    s='11100'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    print(s)

def not_inst(inst):
    s='11101'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    print(s)

def cmp_inst(inst):
    s='11110'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    print(s)

def jmp_inst(inst):
    s='11111'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[1]):
                a=i[-1]
    s=s+'000'+a
    print(s)

def jlt_inst(inst):
    s='01100'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[1]):
                a=i[-1]
    s=s+'000'+a
    print(s)

def jgt_inst(inst):
    s='01101'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[1]):
                a=i[-1]
    s=s+'000'+a
    print(s)

def je_inst(inst):
    s='01111'
    for i in mem_addr:
        if(i[0]=='var'):
            if(i[1]==inst[1]):
                a=i[-1]
    s=s+'000'+a
    print(s)

def hlt_inst(inst):
    s='01010'
    s=s+'0'*11
    print(s)




assemb_inst=sys.stdin.read()

lines=assemb_inst.split('\n')

adr=-1

vars=[]

for i in lines:
    if i=='':
        continue
    
    ins=i.split()
    if ins[0]=='var':
        vars.append(i)
        
        continue
    
    adr+=1
    t=decimaltobinary(str(adr))
    a='0'*(8-len(t))+decimaltobinary(str(adr))
    
    temp_l=[]
    for j in ins:
        temp_l.append(j)
    temp_l.append(a)
    mem_addr.append(temp_l)

for i in vars:
    adr+=1
    t=decimaltobinary(str(adr))
    a='0'*(8-len(t))+decimaltobinary(str(adr))
    
    ins=i.split()

    temp_l=[]
    for j in ins:
        temp_l.append(j)
    temp_l.append(a)
    mem_addr.append(temp_l)

# print(mem_addr)

for i in lines:
    if i=='':
        continue
    
    # adr+=1
    # t=decimaltobinary(str(adr))
    # a='0'*8-len(t)+decimaltobinary(str(adr))
    
    # temp_l=[i,a]
    # mem_addr.append(temp_l)

    inst=i.split()
    # print(inst[0])
    # for j in inst:
    #     print(j)

    if(inst[0]=='add'):
        add_inst(inst)
    elif(inst[0]=='sub'):
        sub_inst(inst)
    elif(inst[0]=='mov' and inst[2] in reg_bin):
        mov_reg_inst(inst)
    elif(inst[0]=='mov' and inst[2][0]=='$'):
        mov_imm_inst(inst)
    elif(inst[0]=='ld'):
        ld_inst(inst)
    elif(inst[0]=='st'):
        st_inst(inst)
    elif(inst[0]=='mul'):
        mul_inst(inst)
    elif(inst[0]=='div'):
        div_inst(inst)
    elif(inst[0]=='rs'):
        rs_inst(inst)
    elif(inst[0]=='xor'):
        xor_inst(inst)
    elif(inst[0]=='or'):
        or_inst(inst)
    elif(inst[0]=='and'):
        and_inst(inst)
    elif(inst[0]=='not'):
        not_inst(inst)
    elif(inst[0]=='cmp'):
        cmp_inst(inst)
    elif(inst[0]=='jmp'):
        jmp_inst(inst)
    elif(inst[0]=='jgt'):
        jgt_inst(inst)
    elif(inst[0]=='jlt'):
        jlt_inst(inst)
    elif(inst[0]=='je'):
        je_inst(inst)
    elif(inst[0]=='hlt'):
        hlt_inst(inst)