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
labels={}
output =[]
global eflag
eflag = 1
global flag_var
flag_var=0

def checkvar(line):
    i=0
    while (line[i][0:3] == 'var'):
        i+=1
    return i

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
    # print(s)
    output.append(s)

def sub_inst(inst):
    s='10001'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # print(s)
    output.append(s)

def mov_reg_inst(inst):
    s='10011'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    output.append(s)

def mov_imm_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)

    s='10010'
    s=s+reg_bin[inst[1]]+'0'*a+t
    output.append(s)

def ld_inst(inst,n):
    global flag_var
    try:
        s='10100'
        for i in mem_addr:
            if(i[0]=='var'):
                if(i[1]==inst[2]):
                    a=i[-1]
        s=s+reg_bin[inst[1]]+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined variable")
        flag_var+=1

def st_inst(inst,n):
    global flag_var
    try:
        s='10101'
        for i in mem_addr:
            if(i[0]=='var'):
                if(i[1]==inst[2]):
                    a=i[-1]
        s=s+reg_bin[inst[1]]+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined variable")
        flag_var+=1


def mul_inst(inst):
    s='10110'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    output.append(s)

def div_inst(inst):
    s='10111'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    output.append(s)

def rs_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11000'
    s=s+reg_bin[inst[1]]+'0'*a+t
    output.append(s)

def ls_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11001'
    s=s+reg_bin[inst[1]]+'0'*a+t
    output.append(s)

def xor_inst(inst):
    s='11010'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    output.append(s)

def or_inst(inst):
    s='11011'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    output.append(s)

def and_inst(inst):
    s='11100'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    output.append(s)

def not_inst(inst):
    s='11101'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    output.append(s)

def cmp_inst(inst):
    s='11110'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    output.append(s)

def jmp_inst(inst,n):
    global flag_var
    try:
        s='11111'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined Label")
        
        flag_var+=1

def jlt_inst(inst,n):
    global flag_var
    try:
        s='01100'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined Label")
        flag_var+=1

def jgt_inst(inst,n):
    global flag_var
    try:
        s='01101'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined Label")
        flag_var+=1

def je_inst(inst,n):
    global flag_var
    try:
        s='01111'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        output.append(s)
    except UnboundLocalError:
        print("Error @ line #",n,": Undefined Label")
        flag_var+=1

def hlt_inst(inst):
    s='01010'
    s=s+'0'*11
    output.append(s)




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

if(len(mem_addr)>256):
    print("Error: Memory limit exceeded")
    eflag=0

def func_caller (inst,i,che):
    global flag_var
    global eflag
    try:
        if ('FLAGS' in inst):
            if (inst[0]=='mov' and inst[2]=='FLAGS'):
                pass
            else:
                print("Error @ line #",i,": Incorrect use of FLAGS")
                eflag=0
        if (inst[0] == 'var' and i>che):
            print("Error @ line #",i,": Incorrect var declaration")
            eflag=0

        if(inst[0]=='add'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            add_inst(inst)

        elif(inst[0]=='sub'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            sub_inst(inst)

        elif(inst[0]=='mov'):
            
            if(inst[2][0]=='$'):
                if(inst[1] not in reg_bin):
                    print("Error @ line #",i,": Invalid Register")
                    eflag=0
                elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0):
                    print("Error @ line #",i,": Imm value not in range")
                    eflag=0
                mov_imm_inst(inst)
            else:
                if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                    print("Error @ line #",i,": Invalid Register")
                    eflag=0
                mov_reg_inst(inst)

        elif(inst[0]=='ld'):
            if(inst[1] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            ld_inst(inst,i)
            if(flag_var!=0):
                flag_var=0
                eflag=0
            

        elif(inst[0]=='st'):
            if(inst[1] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            st_inst(inst,i)
            if(flag_var!=0):
                flag_var=0
                eflag=0

        elif(inst[0]=='mul'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            mul_inst(inst)

        elif(inst[0]=='div'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            div_inst(inst)

        elif(inst[0]=='rs'):
            if(inst[1] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0):
                print("Error @ line #",i,": Imm value not in range")
                eflag=0
            rs_inst(inst)

        elif(inst[0]=='ls'):
            if(inst[1] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0):
                print("Error @ line #",i,": Imm value not in range")
                eflag=0
            ls_inst(inst)

        elif(inst[0]=='xor'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            xor_inst(inst)

        elif(inst[0]=='or'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            or_inst(inst)

        elif(inst[0]=='and'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            and_inst(inst)

        elif(inst[0]=='not'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            not_inst(inst)
        elif(inst[0]=='cmp'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                print("Error @ line #",i,": Invalid Register")
                eflag=0
            cmp_inst(inst)

        elif(inst[0]=='jmp'):
            jmp_inst(inst,i)
            if(flag_var!=0):
                flag_var=0
                eflag=0

        elif(inst[0]=='jgt'):
            jgt_inst(inst,i)
            if(flag_var!=0):
                flag_var=0
                eflag=0

        elif(inst[0]=='jlt'):
            jlt_inst(inst,i)
            if(flag_var!=0):
                flag_var=0
                eflag=0

        elif(inst[0]=='je'):
            je_inst(inst,i)
            
            if(flag_var!=0):
                flag_var=0
                eflag=0

        elif(inst[0]=='hlt' and (i-1)==last_index):
            hlt_inst(inst)

        elif(inst[0]=='var'):
            lsit=[0,0]
            lsit[0]=inst[1];
            var_addr.append(lsit)

        elif(inst[0] not in op_code):
            if(inst[0]!='var'):
                if(inst[0][-1]==':'):
                    
                    func_caller(inst[1:],i,che)
                else:
                    print("Error @ line #",i,": Invalid instruction")
                    eflag=0
    except IndexError:
        print("Error @ line #",i,": Missing argument")
        eflag=0
    except KeyError:
        print("Error @ line #",i,": Invalid argument")
        eflag=0
    

che = checkvar(lines)

last_index = len(lines)-2

for i in range (last_index+1):
    if lines[i]=='':
        continue

    inst=lines[i].split()
    
    func_caller(inst,i+1,che)

if (lines[last_index] != "hlt"):
    print("Error: No Halt function at end")
    eflag = 0



if (eflag == 1):
    for i in output:
        
        print(i)

