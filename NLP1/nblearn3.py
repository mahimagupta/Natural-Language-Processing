import os
import sys
import glob
import collections
import math
import json
import re

files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
test_by_class = collections.defaultdict(list)
train_by_class = collections.defaultdict(list)


wordDict = {}
classDict = {"negative": {}, "truthful": {}, "positive": {}, "deceptive": {}}
totalsize = 0

def makeClassDict(words, class1, class2):

    for word in words:

        if classDict[class1].get(word,None) == None:
            classDict[class1][word] = 2
        else:
            classDict[class1][word] += 1


        if classDict[class2].get(word,None) == None:
            classDict[class2][word] = 2
        else:
            classDict[class2][word] += 1

        # if "negative" in class1:
        #     if word not in classDict["negative"]:
        #         classDict["negative"][word] = 1
        #     else:
        #         classDict["negative"][word] += 1
        # else:
        #     if word not in classDict["positive"]:
        #         classDict["positive"][word] = 1
        #     else:
        #         classDict["positive"][word] += 1
        # if "truthful" in class2:
        #     if word not in classDict["truthful"]:
        #         classDict["truthful"][word] = 1
        #     else:
        #         classDict["truthful"][word] += 1
        # else:
        #     if word not in classDict["deceptive"]:
        #         classDict["deceptive"][word] = 1
        #     else:
        #         classDict["deceptive"][word] += 1

    return classDict


def calculatePriorProbability(priorDict,totalSize):
    priorProbabilityDict = {}

    for key in priorDict.keys():
        # classProb = 0.0
        classLength = 0
        for value in priorDict[key]:
            classLength += (priorDict[key][value])
        classProb = math.log(float(classLength) / totalSize)
        priorProbabilityDict[key] = classProb

    return priorProbabilityDict


def calculateClassSize(classDict,key):
    classSize = 0
    for val in classDict[key]:
        classSize += classDict[key][val]
    # print(key)
    #print(classSize)
    return classSize

def calculateTotalClassSize(classDict,key):

    classSize = len(classDict[key])
    # print(key)
    print(classSize)
    return classSize

def makeDict(words,class1,class2):
    for word in words:
        if word not in wordDict.keys():
            wordDict[word] = [class1,class2]

    return wordDict
priorDict={"negative":{},"truthful": {}, "positive":{}, "deceptive":{}}


def makePriorDict(y,class1,class2):

    priorDict[class1][y] = 1
    priorDict[class2][y] = 1

    return priorDict

for f in files:
    class1, class2, fold, filename = f.split('/')[-4:]
    # if fold == 'fold1':
    #     test_by_class[class1+class2].append(f)
    # else:
    train_by_class[class1+class2].append(f)

a=train_by_class.keys()
b=train_by_class.values()
    #print(a)#print(b)
    #print(train_by_class)
words=[]
class1 = ""
class2 = ""
for key in train_by_class.keys():

        # x = train_by_class[a]
    for y in train_by_class[key]:
        totalsize += 1
            #totalsize = calculateTotalSize()
        class1, class2, fold, filename = y.split('/')[-4:]

        class1 = class1.split("_")[0]
        class2 = class2.split("_")[0]

        priorDict=makePriorDict(y,class1,class2)
            # print(priorDict)
            #  print(class2)
        fil = open(y, "r")
        data = fil.read()
    # print(data)
        #punctuations = [',', '.', '?', ';', '`', ':', '"', '\'', '~', '#', '/', '\\', '!', '...', '---', '(', ')', '-', '<', '>', '$', '%']
        # for i in range(len(punctuations)):
        data = re.sub('[^a-zA-Z]+', ' ', data)
        data = data.lower()
        words_list = data.split()
        words =[]
        stop_words = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'this', 'to', 'was', 'were', 'will', 'with']
        for word in words_list:
            if (word not in stop_words):
                words.append(word)
        # words = " ".join(words)


        classDict = makeClassDict(words, class1, class2)


priorProbabilityDict = calculatePriorProbability(priorDict, totalsize)
# print(priorProbabilityDict)


classSize = 0
totalClassSize=0
extraDict={}
wordProbDict = {"negative": {}, "truthful": {}, "positive": {}, "deceptive": {}}
for key in classDict.keys():
    classSize=calculateClassSize(classDict, key)#total value of class
    totalClassSize = calculateTotalClassSize(classDict,key)#uniquewords
    #print(classSize)
    for val in classDict[key]:
        numerator = classDict[key][val]
        #print(numerator)
        wordProbDict[key][val] = math.log(float(numerator/(classSize+totalClassSize)))
        constantValue=math.log(float(1.0/classSize+totalClassSize))
        extraDict[key]=constantValue


naiveBayesModel=[priorProbabilityDict,wordProbDict,extraDict]
modelFile = open("nbmodel.txt",'w+')
json.dump(naiveBayesModel,modelFile,indent=5,ensure_ascii=False)
modelFile.close()
# print(wordProbDict)

