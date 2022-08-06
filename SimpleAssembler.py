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
         'hlt':'01010',
         'mov':'00000'}

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
         'hlt':'F',
         'addf':'A',
         'subf':'A',
         'movf':'B'}

mem_addr=[]
var_addr=[]
output=[]
flag_var=1
eflag=1
che=0
ls_str=0

def dec_bin(n):
    if (n == 0):
        return 0
    c=0
    bini=""
    while (c<5):
        d = n*2
        c+=1
        if (d>1):
            n=d-1
            bini += "1"
        elif (d<1):
            n=d
            bini += "0"
        elif (d==1):
            bini += "1"
            break
    if (len(bini)<5):
        bini += (6-len(bini))*"0"
    return bini

def bin_dec(n):
    j=1
    sum=0
    for i in n:
        sum += (2**(0-j))*int(i)
        j+=1
    return sum   

def dec_ieee(n):
    n = float(n)
    wh = int(n)
    len_bin = len(str(bin(wh)[2:]))
    dec = float(n-wh)
    bin_wh = bin(wh)[2:]
    bi = str(bin_wh) + str(dec_bin(dec))
    exp = bin(len(str(bin(wh)[2:]))-1)[2:]
    exp = "0"*(3-len(exp))+exp
    ans = str(exp) + bi[1:]
    
    if (ieee_dec(ans)!=n):

        sys.stdout.write("Error @ line #"+str(j)+": float type cannot be represented in 8 bits"+'\n')
    ans = ans[:8]
    return ans

def ieee_dec(ie):
    ie = str(ie)
    exp_bin = ie[:3]
    exp = int(exp_bin,2)
    wh_bin = "1"+ie[3:exp+3]
    if (len(wh_bin)<(exp+1)):
        wh_bin = wh_bin + ("0"*(exp+1-len(wh_bin)))
    wh = int(wh_bin,2)
    bin = ie[exp+3:]
    dec = wh+bin_dec(bin)
    return dec

def checkvar(line):
    global che
    i=0
    while (line[i][0:3] == 'var'):
        i+=1
    che = i

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
    # sys.stdout.write(s+'\n')
    output.append(s)

def sub_inst(inst):
    s='10001'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # print(s)
    # sys.stdout.write(s+'\n')
    output.append(s)

def mov_reg_inst(inst):
    s='10011'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def mov_imm_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)

    s='10010'
    s=s+reg_bin[inst[1]]+'0'*a+t
    # sys.stdout.write(s+'\n')
    output.append(s)

def movf_imm_inst(inst):
    global flag_var
    s = '00010'
    n = float(inst[2][1:])
    if (len(str(dec_bin(n)))>8):
        sys.stdout.write("Error @ line #"+str(j)+": float type cannot be represented in 8 bits"+'\n')
        flag_var=0
    else:
        print(dec_ieee(n))
        s=s+reg_bin[inst[1]]+dec_ieee(n)
        output.append(s)

def addf_inst(inst):
    s='00000'
    s=s+"00"+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # print(s)
    # sys.stdout.write(s+'\n')
    output.append(s)

def subf_inst(inst):
    s='00001'
    s=s+"00"+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # print(s)
    # sys.stdout.write(s+'\n')
    output.append(s)


def ld_inst(inst):
    global flag_var
    try:
        s='10100'
        for i in mem_addr:
            if(i[0]=='var'):
                if(i[1]==inst[2]):
                    a=i[-1]
        s=s+reg_bin[inst[1]]+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined variable")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined variable"+'\n')
        flag_var=0


def st_inst(inst):
    global flag_var
    try:
        s='10101'
        for i in mem_addr:
            if(i[0]=='var'):
                if(i[1]==inst[2]):
                    a=i[-1]
        s=s+reg_bin[inst[1]]+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined variable")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined variable"+'\n')
        flag_var=0



def mul_inst(inst):
    s='10110'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def div_inst(inst):
    s='10111'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def rs_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11000'
    s=s+reg_bin[inst[1]]+'0'*a+t
    # sys.stdout.write(s+'\n')
    output.append(s)

def ls_inst(inst):
    t=decimaltobinary(inst[2][1:])
    a=8-len(t)
    s='11001'
    s=s+reg_bin[inst[1]]+'0'*a+t
    # sys.stdout.write(s+'\n')
    output.append(s)

def xor_inst(inst):
    s='11010'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def or_inst(inst):
    s='11011'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def and_inst(inst):
    s='11100'
    s=s+'00'+reg_bin[inst[1]]+reg_bin[inst[2]]+reg_bin[inst[3]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def not_inst(inst):
    s='11101'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def cmp_inst(inst):
    s='11110'
    s=s+'00000'+reg_bin[inst[1]]+reg_bin[inst[2]]
    # sys.stdout.write(s+'\n')
    output.append(s)

def jmp_inst(inst):
    global flag_var
    try:
        s='11111'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined Label")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined Label"+'\n')
        
        flag_var=0

def jlt_inst(inst):
    global flag_var
    try:
        s='01100'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined Label")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined Label"+'\n')
        
        flag_var=0

def jgt_inst(inst):
    global flag_var
    try:
        s='01101'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined Label")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined Label"+'\n')
        
        flag_var=0

def je_inst(inst):
    global flag_var
    try:
        s='01111'
        for i in mem_addr:
            if(i[0][-1]==':'):
                if(i[0][:-1]==inst[1]):
                    a=i[-1]
        s=s+'000'+a
        # sys.stdout.write(s+'\n')
        output.append(s)
    except UnboundLocalError:
        # print("Error @ line #",j,": Undefined Label")
        sys.stdout.write("Error @ line #"+str(j)+": Undefined Label"+'\n')
        
        flag_var=0


def hlt_inst(inst):
    s='01010'
    s=s+'0'*11
    # sys.stdout.write(s+'\n')
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
    # print("Error: Memory Limit Exceeded")
    sys.stdout.write("Error: Memory Limit Exceeded"+'\n')
    eflag=0

j=0

def func_caller(inst):
    global flag_var
    global eflag
    try:
        if ('FLAGS' in inst):
            if (inst[0]=='mov' and inst[1]=='FLAGS' and inst[2] in reg_bin):
                pass
            else:
                # print("Error @ line #",j,": Incorrect use of FLAGS")
                sys.stdout.write("Error @ line #"+str(j)+": Incorrect use of FLAGS"+'\n')
                eflag=0
                
        if (inst[0] == 'var' and j>che):
            # print("Error @ line #",j,": Incorrect var declaration")
            sys.stdout.write("Error @ line #"+str(j)+": Incorrect var declaration"+'\n')
            eflag=0

        if(inst[0]=='add'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            add_inst(inst)

        elif(inst[0]=='addf'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            addf_inst(inst)

        elif(inst[0]=='sub'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            sub_inst(inst)

        elif(inst[0]=='subf'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            subf_inst(inst)

        elif(inst[0]=='mov'):
            if(inst[2][0]=='$'):
                # if(inst[1] not in reg_bin):
                #     # print("Error @ line #",j,": Invalid Register")
                #     sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                #     eflag=0
                #     return
                # elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0):
                #     # print("Error @ line #",j,": Imm value not in range")
                #     sys.stdout.write("Error @ line #"+str(j)+": Imm value not in range"+'\n')
                #     eflag=0
                try:
                    if(inst[1] not in reg_bin):
                        # print("Error @ line #",j,": Invalid Register")
                        sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                        eflag=0
                        return
                    if (inst[2][0] != '$'):
                        sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm"+'\n')
                        eflag=0
                    elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0 or (float(inst[2][1:]) - int(float(inst[2][1:]))) != 0 ):
                        # print("Error @ line #",j,": Imm value not in range")
                        sys.stdout.write("Error @ line #"+str(j)+": Imm value not in range"+'\n')
                        eflag=0
                    mov_imm_inst(inst)
                except ValueError:
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm value"+'\n')
                    eflag = 0

                # mov_imm_inst(inst)
            else:
                if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                    # print("Error @ line #",j,": Invalid Register")
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Register or Invalid Imm"+'\n')
                    eflag=0
                    return
                mov_reg_inst(inst)

        elif(inst[0]=='movf'):
                try:
                    if(inst[1] not in reg_bin):
                        sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                        eflag=0
                        return
                    if (inst[2][0] != '$'):
                        sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm"+'\n')
                        eflag=0
                    movf_imm_inst(inst)
                except ValueError:
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm value"+'\n')
                    eflag = 0
        
        elif(inst[0]=='ld'):
            if(inst[1] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            ld_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='st'):
            if(inst[1] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            st_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='mul'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            mul_inst(inst)

        elif(inst[0]=='div'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            div_inst(inst)

        elif(inst[0]=='rs'):
            # if(inst[1] not in reg_bin):
            #     # print("Error @ line #",j,": Invalid Register")
            #     sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
            #     eflag=0
            #     return
            # elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0):
            #     # print("Error @ line #",j,": Imm value not in range")
            #     sys.stdout.write("Error @ line #"+str(j)+": Imm value not in range"+'\n')
            #     eflag=0
            # rs_inst(inst)
            try:
                if(inst[1] not in reg_bin):
                    # print("Error @ line #",j,": Invalid Register")
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                    eflag=0
                    return
                if (inst[2][0] != '$'):
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm"+'\n')
                    eflag=0
                elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0 or (float(inst[2][1:]) - int(float(inst[2][1:]))) != 0 ):
                    # print("Error @ line #",j,": Imm value not in range")
                    sys.stdout.write("Error @ line #"+str(j)+": Imm value not in range"+'\n')
                    eflag=0
                ls_inst(inst)
            except ValueError:
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm value"+'\n')
                eflag = 0

        elif(inst[0]=='ls'):
            try:
                if(inst[1] not in reg_bin):
                    # print("Error @ line #",j,": Invalid Register")
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                    eflag=0
                    return
                if (inst[2][0] != '$'):
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm"+'\n')
                    eflag=0
                elif (int(inst[2][1:]) > 255 or int(inst[2][1:]) < 0 or (float(inst[2][1:]) - int(float(inst[2][1:]))) != 0 ):
                    # print("Error @ line #",j,": Imm value not in range")
                    sys.stdout.write("Error @ line #"+str(j)+": Imm value not in range"+'\n')
                    eflag=0
                ls_inst(inst)
            except ValueError:
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Imm value"+'\n')
                eflag = 0

        elif(inst[0]=='xor'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            xor_inst(inst)

        elif(inst[0]=='or'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            or_inst(inst)

        elif(inst[0]=='and'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin or inst[3] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            and_inst(inst)

        elif(inst[0]=='not'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            not_inst(inst)

        elif(inst[0]=='cmp'):
            if(inst[1] not in reg_bin or inst[2] not in reg_bin):
                # print("Error @ line #",j,": Invalid Register")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid Register"+'\n')
                eflag=0
                return
            cmp_inst(inst)

        elif(inst[0]=='jmp'):
            jmp_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='jgt'):
            jgt_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='jlt'):
            jlt_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='je'):
            je_inst(inst)
            if(flag_var==0):
                flag_var=1
                eflag=0

        elif(inst[0]=='hlt'):
            if(j==len(lines)):
                hlt_inst(inst)
            else:
                # print("Error @ line #",j,": Invalid hlt position")
                sys.stdout.write("Error @ line #"+str(j)+": Invalid hlt position"+'\n')
                eflag=0
        # elif(inst[0][-1]==':'):
        #     func_caller(inst[1:])
        elif(inst[0] not in op_code):
            if(inst[0]!='var'):
                if(inst[0][-1]==':'):
                    if(inst[1] in op_code):

                        func_caller(inst[1:])
                    else:
                        # print("Error @ line #",j,": Invalid label use")
                        sys.stdout.write("Error @ line #"+str(j)+": Invalid label use"+'\n')
                        eflag=0
                        
                else:
                    # print("Error @ line #",j,": Invalid instruction")
                    sys.stdout.write("Error @ line #"+str(j)+": Invalid instruction"+'\n')
                    eflag=0

    except IndexError:
        # print("Error @ line #",j,": Missing argument")
        sys.stdout.write("Error @ line #"+str(j)+": Missing argument"+'\n')
        eflag=0
        
    except KeyError:
        # print("Error @ line #",j,": Invalid argument")
        sys.stdout.write("Error @ line #"+str(j)+": Invalid argument"+'\n')
        eflag=0

len_lines=len(lines)
# print(len_lines)

# for i in range(len_lines-1):
#     if lines[i]=='':
#         continue
    

#     inst=lines[i].split()
    
#     func_caller(inst)

checkvar(lines)

# lines=lines[:-1]
len_lines=len(lines)

# print(lines)

if(lines[-1]==''):
    lines=lines[:-1]

# print(lines)

len_lines=len(lines)

for i in lines:
    j+=1
    if i=='':
        continue
    inst=i.split()

    func_caller(inst)


if(lines!=['']):
    ll = lines[-1].split()
    if(lines[-1]!='hlt'):
        if (ll[1]=='hlt' and ll[0][-1:]==':'):
            pass
        else:
            sys.stdout.write("Error: No hlt function at end"+'\n')
            eflag=0
else:
    # print("Error: No Instruction")
    sys.stdout.write("Error: No Instruction"+'\n')

if(eflag==1):
    
    for i in output:
        # print(i)
        sys.stdout.write(i+'\n')