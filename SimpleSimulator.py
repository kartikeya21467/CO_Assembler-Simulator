from matplotlib import pyplot as plt
import sys

inst_typ={"A":["10000","10001","10110","11010","11011","11100","00000","00001"],
          "B":["10010","11000","11001","00010"],
          "C":["10011","10111","11101","11110"],
          "D":["10100","10101"],
          "E":["11111","01100","01101","01111"],
          "F":["01010"]}

regs={"000":0,
      "001":0,
      "010":0,
      "011":0,
      "100":0,
      "101":0,
      "110":0,
      "111":0}



MEM=["0000000000000000"]*256

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

checker=0

def dec_ieee(n):
    global checker
    n = float(n)
    wh = int(n)
    len_bin = len(str(bin(wh)[2:]))
    if (len_bin>8):
        checker=1
        # print("Error ")
        #sys.stdout.write("Error @ line #"+str(j)+": float type cannot be represented in 8 bits"+'\n')
    else: 
        dec = float(n-wh)
        bin_wh = bin(wh)[2:]
        bi = str(bin_wh) + str(dec_bin(dec))
        exp = bin(len(str(bin(wh)[2:]))-1)[2:]
        exp = "0"*(3-len(exp))+exp
        ans = str(exp) + bi[1:]
        ans = ans[:8]
        if (ieee_dec(ans)!=n):
            checker=1
            # print("Error ")
            #sys.stdout.write("Error @ line #"+str(j)+": float type cannot be represented in 8 bits"+'\n')
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



sim_inst=sys.stdin.read()
lines=sim_inst.split("\n")
if(lines[-1]==''):
    lines=lines[:-1]
p=0

def initialize():
    global p
    for i in lines:
        
        op=i[:5]
        if op in inst_typ["A"]:
            un=i[5:7]
            reg1=i[7:10]
            reg2=i[10:13]
            reg3=i[13:16]
            t=[op,un,reg1,reg2,reg3]
            MEM[p]=t
            p+=1
            

        if op in inst_typ["B"]:
            reg1=i[5:8]
            imm=i[8:16]
            t=[op,reg1,imm]
            MEM[p]=t
            p+=1

        if op in inst_typ["C"]:
            un=i[5:10]
            reg1=i[10:13]
            reg2=i[13:16]
            t=[op,un,reg1,reg2]
            MEM[p]=t
            p+=1
        
        if op in inst_typ["D"]:
            reg1=i[5:8]
            mem=i[8:16]
            t=[op,reg1,mem]
            MEM[p]=t
            p+=1

        if op in inst_typ["E"]:
            un=i[5:8]
            mem=i[8:16]
            t=[op,un,mem]
            MEM[p]=t
            p+=1

        if op in inst_typ["F"]:
            un=i[5:16]
            t=[op,un]
            MEM[p]=t
            p+=1

def binarytodecimal(s):
    l=len(s)
    sum=0
    for i in range(l):
        sum+=int(s[i])*2**(l-1-i)

    return sum

def decimaltobinary(s):
    s1=""
    n=int(s)
    while n>0:
        s1+=str(n%2)
        n=n//2
    res=s1[::-1]
    return res

pc_temp=0
halted=False

orv=0

def execute(instruction,x,y,cycle):
    global pc_temp
    global halted
    global checker
    global orv
    op=instruction[0]
    if op==inst_typ["A"][0]:
        regs[instruction[4]]=regs[instruction[2]]+regs[instruction[3]]
        if (regs[instruction[4]]>65535 or regs[instruction[4]]<0):
            regs["111"]=8
            regs[instruction[4]]=regs[instruction[4]]%65535
            orv=1
        pc_temp+=1

    if op==inst_typ["A"][1]:
        regs[instruction[4]]=regs[instruction[2]]-regs[instruction[3]]
        if (regs[instruction[4]]>65535 or regs[instruction[4]]<0):
            regs["111"]=8
            regs[instruction[4]]=regs[instruction[4]]%65535
            orv=1
        pc_temp+=1

    if op==inst_typ["A"][2]:
        regs[instruction[4]]=regs[instruction[2]]*regs[instruction[3]]
        if (regs[instruction[4]]>65535 or regs[instruction[4]]<0):
            regs["111"]=8
            regs[instruction[4]]=regs[instruction[4]]%65535
            orv=1
        pc_temp+=1
    
    if op==inst_typ["A"][3]:
        regs[instruction[4]]=regs[instruction[2]]^regs[instruction[3]]
        pc_temp+=1
    
    if op==inst_typ["A"][4]:
        regs[instruction[4]]=regs[instruction[2]]|regs[instruction[3]]
        pc_temp+=1
    
    if op==inst_typ["A"][5]:
        regs[instruction[4]]=regs[instruction[2]]&regs[instruction[3]]
        pc_temp+=1

    if op==inst_typ["A"][6]:
        regs[instruction[4]]=regs[instruction[2]]+regs[instruction[3]]
        dec_ieee(regs[instruction[4]])
        if(checker==1):
            regs["111"]=8
            regs[instruction[4]]=252.0
            checker=0
            orv=1
        pc_temp+=1

    if op==inst_typ["A"][7]:
        regs[instruction[4]]=regs[instruction[2]]-regs[instruction[3]]
        dec_ieee(regs[instruction[4]])
        if(checker==1):
            regs["111"]=8
            regs[instruction[4]]=0
            checker=0
            orv=1
        pc_temp+=1
    
    if op==inst_typ["B"][0]:
        regs[instruction[1]]=binarytodecimal(instruction[2])
        pc_temp+=1
    
    if op==inst_typ["B"][1]:
        regs[instruction[1]]=regs[instruction[1]]>>binarytodecimal(instruction[2])
        pc_temp+=1
    
    if op==inst_typ["B"][2]:
        regs[instruction[1]]=regs[instruction[1]]<<binarytodecimal(instruction[2])
        pc_temp+=1

    if op==inst_typ["B"][3]:
        regs[instruction[1]]=ieee_dec(instruction[2])
        pc_temp+=1

    if op==inst_typ["C"][0]:
        regs[instruction[3]]=regs[instruction[2]]
        pc_temp+=1

    if op==inst_typ["C"][1]:
        regs["000"]=regs[instruction[2]]//regs[instruction[3]]
        regs["001"]=regs[instruction[2]]%regs[instruction[3]]
        pc_temp+=1
    
    if op==inst_typ["C"][2]:
        regs[instruction[3]]=~regs[instruction[2]]
        pc_temp+=1
    
    if op==inst_typ["C"][3]:
        if(regs[instruction[2]]<regs[instruction[3]]):
            regs["111"]=4
        if(regs[instruction[2]]>regs[instruction[3]]):
            regs["111"]=2
        if(regs[instruction[2]]==regs[instruction[3]]):
            regs["111"]=1
        pc_temp+=1
        orv=1
    
    if op==inst_typ["D"][0]:
        x.append(cycle)
        y.append(binarytodecimal(instruction[2]))
        regs[instruction[1]]=binarytodecimal(MEM[binarytodecimal(instruction[2])])
        pc_temp+=1

    
    if op==inst_typ["D"][1]:
        x.append(cycle)
        y.append(binarytodecimal(instruction[2]))
        t=decimaltobinary(regs[instruction[1]])
        a=16-len(t)
        MEM[binarytodecimal(instruction[2])]='0'*a+t
        pc_temp+=1

    if op==inst_typ["E"][0]:
        pc_temp=binarytodecimal(instruction[2])
        


    if op==inst_typ["E"][1]:
        if regs["111"]==4:
            pc_temp=binarytodecimal(instruction[2])
        else:
            pc_temp+=1
        
    
    if op==inst_typ["E"][2]:
        if regs["111"]==2:
            pc_temp=binarytodecimal(instruction[2])
        else:
            pc_temp+=1
        
    
    if op==inst_typ["E"][3]:
        if regs["111"]==1:
            pc_temp=binarytodecimal(instruction[2])
        else:
            pc_temp+=1
        
    
    if op==inst_typ["F"][0]:
        halted=True

    if(orv==0):
        regs["111"]=0
    orv=0

        
    return halted,pc_temp


initialize()
pc=0

x=[]
y=[]
cycle=0


while(not halted):
    x.append(cycle)
    y.append(pc)
    Instruction=MEM[pc]
    halted,new_pc=execute(Instruction,x,y,cycle)
    t=decimaltobinary(pc)
    a=8-len(t)
    s='0'*a+t
    sys.stdout.write(s+' ')
    # print(s,end=" ")
    for i in regs:
        if(type(regs[i])==float):
            t=dec_ieee(regs[i])
        else:
            t=decimaltobinary(regs[i])
        a=16-len(t)
        s='0'*a+t
        sys.stdout.write(s+' ')
        # print(s,end=" ")
    sys.stdout.write("\n")
    pc=new_pc
    cycle+=1

for i in MEM:
    
    if type(i)==list:
        s=''.join(i)
        sys.stdout.write(s+'\n')
    else:
        sys.stdout.write(i+'\n')

#plt.scatter(x,y)
#plt.xlabel("cycle")
#plt.ylabel("memory")
# plt.show()
