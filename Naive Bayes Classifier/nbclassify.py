import sys, string,json,math,os

pathname = sys.argv[-1]

# creating list of stopwords
def returnStopwords():
    with open("stopwords.txt") as f:
        stpwords = f.readlines()
    stopwords = [word.strip('\n') for word in stpwords]
    return stopwords
stopword = returnStopwords()

#reading from nbmodel.txt
commonDict = dict()
classPrior = dict()
count = 0
with open("nbmodel.txt") as raw_data:
    for item in raw_data:
        if ':' in item:
            key,value = item.split(':', 1)
            if(count<=4):
                classPrior[key] = value.strip(' ')
            else:
                value= value.strip('[').replace(']','')
                commonDict[key] =[(x.strip(' ')) for x in value.split(',')]
        count += 1

scorepos =0
scoreneg =0
scoretru =0
scoredec =0

f1=open("nboutput.txt",'w')

# processing the training data file
def doClassification(file_path):
    global scorepos,scoreneg,scoretru,scoredec
    with open(file_path, 'r') as f:
        for line in f:
            key = line[:line.find(" ")]
            newline = " ".join(line.split()[1:])
            newline = newline.translate(None, string.punctuation).lower()
            tokenList = [word for word in newline.split() if word not in stopword]
            tokenLst = ' '.join(tokenList)
            tokenLst = ''.join([i for i in tokenLst if not i.isdigit()]) #remove words which start or end with digits
            tokenLst = tokenLst.split()
            scorepos = 0
            scoredec = 0
            scoretru = 0
            scoreneg = 0
            for token in tokenLst:
                if (commonDict.has_key(token)):
                    scorepos += math.log(float(commonDict[token][0]))
                    scoreneg += math.log(float (commonDict[token][1]))
                    scoretru += math.log(float(commonDict[token][2]))
                    scoredec += math.log(float( commonDict[token][3]))
            scorepos += math.log(float(classPrior['positive']))
            scoreneg += math.log(float(classPrior['negative']))
            scoretru += math.log(float(classPrior['truthful']))
            scoredec += math.log(float(classPrior['deceptive']))
            label1 = "truthful" if (scoretru > scoredec) else "deceptive"
            label2 = "positive" if (scorepos > scoreneg) else "negative"
            f1.write(key.strip()+" "+label1.strip()+" "+label2.strip())
            f1.write('\n')
doClassification(pathname)


