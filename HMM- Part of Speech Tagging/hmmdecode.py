import sys
import math
from _collections import defaultdict
import time
from collections import OrderedDict

start_time = time.time()
transition = defaultdict(int)
emission = defaultdict(int)
tagcountemit = defaultdict(int)
tagsofword = {}
listoftags=[]

def store(line,c):
    token = line.strip("\n").split(" ")
    if(c==1):
        t = (token[0], token[1])
        emission[t] = float(token[2])
    elif(c==2):
        t = (token[0], token[1])
        transition[t] =float(token[2])
    elif (c==3):
        tagsofword[token[0]] = set()
        for i in token[1].split(","):
            tagsofword[token[0]].add(i)
    elif(c==4):
        tagcountemit[token[0]] = float(token[1])

def writetoFile1(bp, prevtag, index, line,ans):
    f1 = open("hmmoutput.txt", 'a')
    k = index
    for i in range(k):
        if (index==0):
            break
        listoftags.append(bp[index][prevtag])
        index-=1
        prevtag = bp[index+1][prevtag]
    if (index ==0):
        listoftags.reverse()
        lines = []
        lines = line.split(" ")
        x=len(lines)
        tempans=""
        for i in range(0, x):
            tempans=tempans+" "+lines[i].rstrip()+ "/" + str(listoftags[i])
        f1.write(tempans.lstrip().rstrip())
        f1.write('\n')
        f1.close()

def findlasttag(bp, pw,line,ans):
    lasttag = max(pw, key=lambda k: pw[k])
    listoftags.append(lasttag[1])
    ans.append(lasttag[0]+"/"+lasttag[1])
    writetoFile1(bp,lasttag[1],lasttag[2],line,ans)

def Viterbi():
    with open(sys.argv[1]) as f:
        for line in f:
            previousword = {}
            backpointer = dict()
            ans = []
            index=0
            tokens = line.strip().split(" ")
            start='<s>'
            counter=0
            for observation in tokens:
                tmplist={}
                if(counter==0):
                    if (observation in tagsofword):
                        for currtag in tagsofword[observation]:
                            t = (start, currtag)
                            tprob = transition[t]
                            t1=(observation,currtag)
                            probval = math.log(float(tprob),10) + math.log(float(emission[t1]),10)
                            previousword[tuple([observation,currtag,index])]=probval
                    else:
                        for k in transition:
                            if k[0] == '<s>' and k[1]!= '<s>':
                                previousword[tuple([observation, k[1], index])] = math.log(transition[k],10)
                else:
                    if observation in tagsofword:
                        tempD={}
                        temp1=''
                        temp2 = ''
                        for currtag in tagsofword[observation]:
                            max = -float("inf")
                            for k in previousword:
                                t = (k[1], currtag)
                                tprob = transition[t]
                                t1 = (observation, currtag)
                                probval = (math.log(float(tprob),10)) + math.log(float(emission[t1]),10)+ float(previousword[k])
                                if(probval>max):
                                    max = probval
                                    temp1 = currtag
                                    temp2 = k
                            tempD[tuple([observation, temp1, index])] = max
                            tmplist[temp1]=temp2[1]
                    else:
                        tempdict={}
                        tempD = {}
                        for k1 in previousword:
                            for keys in transition:
                                if k1[1] == keys[0]:
                                    val2 = math.log(transition[keys],10) + float(previousword[k1])
                                    tempdict[tuple([keys[0],keys[1],index])]=val2

                        tempdictsorted = OrderedDict(sorted(tempdict.items(), key=lambda x: x[1],reverse=True)) #desc sort
                        tempdict2={}
                        tagdict={}
                        for k in tempdictsorted:
                            if(k[1] not in tagdict):
                                tempdict2[k]=tempdictsorted[k]
                            tagdict[k[1]] = 1

                        for k1 in tempdict2:
                            tempD[tuple([observation, k1[1], index])] = tempdict2[k1]
                            tmplist[k1[1]] = k1[0]
                counter+=1
                backpointer[index]=tmplist
                if counter>1:
                    previousword=tempD
                index += 1
            findlasttag(backpointer, previousword,line,ans)

def main():
    count = 0
    with open("hmmmodel.txt") as f:
        for line in f:
            if(line.startswith("****************Emission Probabilities****************")):
                count=1
            elif(line.startswith("****************Transition Probabilities****************")):
                count=2
            elif (line.startswith("****************WordsTags****************")):
                count=3
            elif (line.startswith("****************TagCount****************")):
                count=4
            else:
               store(line,count)
        Viterbi()

if __name__ == "__main__":
     main()
     print("\n\n--- %s seconds ---" % (time.time() - start_time))