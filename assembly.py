import sys

assemb_inst=sys.stdin.read()

lines=assemb_inst.split()
for i in lines:
    
    inst=i.split()
    if(inst[-1]=='R0'):
        print("Yes")
    # for j in inst:
    #     print(j)
