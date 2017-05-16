import sys
from _collections import defaultdict
import time
import itertools

start_time = time.time()
transition = defaultdict(int)
emission = defaultdict(int)
tagcountemit = defaultdict(int)
tagcounttransit = defaultdict(int)
tagsofword = {}
allTags = set()

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            start = "<s>"
            tagcountemit[start] += 1
            tokens = line.strip().split(" ")
            for token in tokens:
                tagcounttransit[start] += 1
                word = token[:-3]
                tag = token[-2:]
                tagcountemit[tag] += 1
                t = (start, tag)
                transition[t] += 1
                allTags.add(start)
                allTags.add(tag)
                t1 = (word, tag)
                emission[t1] += 1
                if word not in tagsofword:
                    tagsofword[word] = set()
                tagsofword[word].add(tag)
                start = tag
    write()

# write to a model
def write():
    with open("hmmmodel.txt", 'w') as f:
        #count emission
        f.write("****************Emission Probabilities****************" + '\n')
        for key in emission:
            val= float((emission[key]) / (float(tagcountemit[str(key[1])])))
            f.write(str(key[0]) + " "+ str(key[1])+" "+str(val)+"\n")

        #count transition
        f.write("****************Transition Probabilities****************" + '\n')
        for i in itertools.combinations_with_replacement(allTags,2):
            if(i not in transition) and (i[1] != '<s>'):
                transition[i]=0
            if(tuple([i[1],i[0]]) not in transition) and (i[0] != '<s>'):
                transition[tuple([i[1],i[0]])]=0
        for key in transition:
            val=((transition[key]+1) / (float(len(tagcounttransit)-1) + tagcounttransit[str(key[0])]))
            f.write(str(key[0]) + " " + str(key[1])+ " " + str(val) +"\n")

        #Tags for each Word
        f.write("****************WordsTags****************" + '\n')
        for key, value in tagsofword.items():
            f.write(key + " " + ','.join([str(i) for i in value]) + "\n")

        #Count of Tags
        f.write("****************TagCount****************" + '\n')
        for key, value in tagcountemit.items():
            f.write(key + " " + str(value) + "\n")

if __name__ == "__main__":
     main()
     print("\n\n--- %s seconds ---" % (time.time() - start_time))