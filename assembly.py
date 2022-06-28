import sys

reg_bin={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101',
        'R6':'110','FLAGS':'111'}



assemb_inst=sys.stdin.read()

lines=assemb_inst.split()
for i in lines:
    
    inst=i.split()
    
    for j in inst:
        print(j)

