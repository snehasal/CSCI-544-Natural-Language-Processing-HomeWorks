import sys, string, json

trainData = sys.argv[-2]
labelData = sys.argv[-1]

# creating list of stopwords
def returnStopwords():
    with open("stopwords.txt") as f:
        stpwords = f.readlines()
    stopwords = [word.strip('\n') for word in stpwords]
    return stopwords
stopword = returnStopwords()

# processing labels files
labeldict = {}
with open(labelData, 'r') as labels:
    for i in labels:
        k = i.split(" ")
        labeldict[k[0].strip()] = {'v1': k[1].strip(), 'v2': k[2].strip()}
     
# create dict to store tokens
commonDict = dict()

#processing classes
def processLabels(label, tokenList):
    if ((labeldict.get(key)).get(label)) == 'positive':
        addToDict(tokenList, 0)
    if ((labeldict.get(key)).get(label)) == 'negative':
        addToDict(tokenList, 1)
    if ((labeldict.get(key)).get(label)) == 'truthful':
        addToDict(tokenList, 2)
    if ((labeldict.get(key)).get(label)) == 'deceptive':
        addToDict(tokenList, 3)

# addToDict: adding words to dictionary
def addToDict(tokenList,index):
    global cpos, cneg, cdef, ctru
    for token in tokenList:
        if (commonDict.has_key(token)):
            commonDict[token][index] = int(commonDict[token][index]) + int('1')
        else:
            commonDict[token] = [0,0,0,0]
            commonDict[token][index]= int(commonDict[token][index]) + int('1')

# processing the training data file
with open(trainData, 'r') as f:
    for line in f:
        key = line[:line.find(" ")]
        newline = " ".join(line.split()[1:-1])
        newline = newline.translate(None, string.punctuation).lower()
        tokenList = [word for word in newline.split() if ((word not in stopword)and (word.isalnum()))]
        tokenLst = ' '.join(tokenList)
        tokenLst = ''.join([i for i in tokenLst if not i.isdigit()]) #remove words which start or end with digits
        tokenLst=tokenLst.split()
        if (labeldict.has_key(key)):
            processLabels('v1', tokenLst)
            processLabels('v2', tokenLst)

# remove low frequency words
def removeLowFreqwords():
    for key,val in commonDict.items():
        if (sum(val)) <=1:
     		del commonDict[key]

removeLowFreqwords()

# add smoothing
def smoothing():
    for key,val in commonDict.items():
        for i in range(0,4):
            commonDict[key][i]+=1
smoothing()
      
newcpos =0
newctru=0
newcneg=0
newcdef=0

# calcuating count of classes
def countLabels():
    global newcneg,newcpos,newcdef,newctru
    for key, val in commonDict.items():
        newcpos += val[0]
        newcneg += val[1]
        newctru += val[2]
        newcdef += val[3]
countLabels()

# calculate probabilities
def calculateprob():
    for key, val in commonDict.items():
         commonDict[key][0] /= float(newcpos)
         commonDict[key][1] /= float(newcneg)
         commonDict[key][2] /= float(newctru)
         commonDict[key][3] /= float(newcdef)
calculateprob()

#calculating class priors
totalProb=newcpos+newcneg
totalProb2 = newcdef+newctru
classPrior={}
classPrior['positive']=newcpos/float(totalProb)
classPrior['negative']=newcneg/float(totalProb)
classPrior['truthful']=newctru/float(totalProb2)
classPrior['deceptive']=newcdef/float(totalProb2)

# write to a model
with open("nbmodel.txt", 'w') as f:
   f.write("Prior Class Probabilities"+'\n')
   for key, value in classPrior.items():
      f.write('%s:%s\n' % (key, value))
   for key, value in commonDict.items():
        f.write('%s:%s\n' % (key, value))