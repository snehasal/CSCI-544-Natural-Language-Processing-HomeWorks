import sys,math,os,io,pprint
from itertools import izip
from _collections import defaultdict

# read files
def main():
    candfile=[]
    candfile.append(sys.argv[1])
    arg2 = sys.argv[2]
    reffile=[]
    if os.path.isdir(arg2):
         for root, dirs, files in os.walk(arg2):
            for x in files:
                reffile.append(os.path.join(root, x))
    else:
        reffile.append(arg2)
    CalculatePN(candfile,reffile)

# calculate pn
def CalculatePN(candfile, reffile):
    c = 0
    r = 0
    pn = 0
    for temp in range(1,5):
        den = 0
        num=0
        candclip = []
        candfile1 = [io.open(fname, 'r', encoding='utf-8') for fname in candfile]
        reffile1 = [io.open(fname, 'r', encoding='utf-8') for fname in reffile]
        for x in izip(*candfile1):
            candclip.append(CalculateNGram(x[0], temp))

        for can in range(0, len(candclip)):
            den+=sum(candclip[can].values())

        flag=0;
        for x in izip(*reffile1):
            refclip = {}
            for i1 in range(0, len(reffile1)):
                refclip[i1]=(CalculateNGram(x[i1], temp))

            if (temp == 1):
                tempref2=sum(refclip[0].values())
                tempcand=sum(candclip[flag].values())
                c=den
                for val in range(0,len(refclip)):
                    tempref1= sum(refclip[val].values())
                    if(math.fabs(tempcand-tempref1)<=tempref2):
                        tempref2=math.fabs(tempcand-tempref1)
                        tempref3=tempref1
                r+= tempref3

            for t in candclip[flag]:
                val=0
                for val1 in range(0, len(refclip)):
                    if t in refclip[val1]:
                        val = max(val, refclip[val1][t])
                num += min(val, candclip[flag][t])
            flag += 1
        print num,den
        pn += math.log(float(num) / den) / 4
    CalculateBP(c,r,pn)

#calculate n-gram
def CalculateNGram(x,n):
    tempdict=defaultdict(int)
    input = x.split()
    for i in range(len(input) - n + 1):
        g = ' '.join(input[i:i + n])
        tempdict[g] += 1
    return tempdict

# calculate Bp
def CalculateBP(c, r, pn):
    if c > r:
        BP = 1
    else:
        BP = math.exp(1 - float(r) / c)
    print BP
    CalculateBLEUScore(BP, pn)

# calculate BLUE
def CalculateBLEUScore(BP, pn):
    BLEUScore = BP * math.exp(pn)
    print BLEUScore
    writetoFile(BLEUScore)

# write to output
def writetoFile(BLEUScore):
    f = open('bleu_out.txt', 'w')
    f.write(str(BLEUScore))
    f.close()

if __name__ == "__main__":
    main()