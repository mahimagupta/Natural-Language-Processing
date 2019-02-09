import math
import re
import glob
import os
import sys
import collections
import json
import re


# word_list =[]
# stop_words =["the", "so", "to", "too", "am", "lot", "not", "ask", "no", "as", "all", "more", "couldn't", "don't", "well", "very", "as", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "with","this","had","on","they","have","there","you","be","and","a","i","was","in","of","for","it","at","my","is","that","were","with", "you'd", "you'll", 'your', "you're", 'yours', 'yourself', 'yourselves', "you've", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "you"re", "you"ve", "you"ll", "you"d", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "she"s", "her", "hers", "herself", "it", "it"s", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "that"ll", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "don"t", "should", "should"ve", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't", "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "mustn", "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", "shouldn't", "wasn", "wasn't", "weren", "weren't", "won", "won't", "wouldn", "wouldn't"]
# for word in words:
#     if(word not in stop_words) and (not word.isdigit()):
#         word_list.append(word)
#         wordlist = " ".join(word_list)
# print(wordlist)

def processModel(naiveBayesModel):
    priorProbabilityDict={}
    wordDict={}
    priorProbabilityDict=naiveBayesModel[0]
    #print(priorProbabilityDict)
    wordDict=naiveBayesModel[1]
    extraDict=naiveBayesModel[2]
    return priorProbabilityDict,wordDict,extraDict
finalArray=[]


def printFunction(class1,class2,y):
    output=class1+" "+class2+" "+y
    return output

# def calculateWordProbability(data,wordDict,priorProbabilityDict):
#     positiveCount=0
#     negativeCount=0
#     deceptiveCount=0
#     truthfulCount=0
#     for word in data:
#         if word in wordDict["positive"]:
#             wordProb1=wordDict["positive"][word]+priorProbabilityDict["positive"]
#         else:
#             # continue Go to the next word
#         if word in wordDict["negative"]:
#             wordProb2 = wordDict["negative"][word]+priorProbabilityDict["negative"]
#         else:
#             wordProb2 = -99999
#         if max(wordProb1,wordProb2) == wordProb1:
#             positiveCount += 1
#         else:
#             negativeCount += 1
#         if word in wordDict["truthful"]:
#             wordProb3 = wordDict["truthful"][word]+priorProbabilityDict["truthful"]
#         else:
#             wordProb3 = -99999
#         if word in wordDict["deceptive"]:
#             wordProb4 = wordDict["deceptive"][word]+priorProbabilityDict["deceptive"]
#         else:
#             wordProb4 = -99999
#         if max(wordProb3,wordProb4)==wordProb3:
#             truthfulCount += 1
#         else:
#             deceptiveCount += 1
#
#
#     class1=""
#     class2=""
#     if max(positiveCount,negativeCount)==positiveCount:
#         class1="positive"
#     else:
#         class1="negative"
#     if max(deceptiveCount,truthfulCount)==truthfulCount:
#          class2="truthful"
#     else:
#         class2="deceptive"
#     # print(class1,class2)
#     return class1,class2
#
# countervalidate=0


def getProbability(words,wordDict,priorProb,extraDict):
    word_prob = priorProb
    # print(wordDict)
    # print(priorProb)
    #print(word_prob)
    for word in words:
        if wordDict.get(word, None) is not None:
            word_prob += wordDict[word]
        else:
            word_prob += extraDict

    return word_prob
  #print(word_prob)


def validateFunction(classtest1,classtest2,class1,class2):
    if (class1==classtest1) and (classtest2==class2):
        return True
    else:
        return False


priorProbabilityDict={}
wordDict={}
modelFile=open("nbmodel.txt",'r')
naiveBayesModel=json.load(modelFile)
priorProbabilityDict,wordDict, extraDict=processModel(naiveBayesModel)
files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
test_by_class = collections.defaultdict(list)

for f in files:
    class1, class2, fold, filename = f.split('/')[-4:]
    # if fold == 'fold1':
    test_by_class[class1+class2].append(f)
# print(test_by_class)

k = test_by_class.keys()
v = test_by_class.values()
counter=0
check=False

fh = open("nboutput.txt", 'w+')

for key in test_by_class.keys():
    for y in test_by_class[key]:

        words = []
        counter+=1
        classtest1, classtest2, fold, filename = y.split('/')[-4:]
        # if "negative" in classtest1:
        #     classtest1="negative"
        # else:
        #     classtest1="positive"
        #
        # if "truthful" in classtest2:
        #     classtest2="truthful"
        # else:
        #     classtest2="deceptive"

        # print(class1)
        # print(class2)
        fil = open(y,"r")
        data = fil.read()
        punctuations = [',', '.', '?', ';', '`', ':', '"', '\'', '~', '#', '/', '\\', '!', '...', '---', '(', ')', '-',
                        '<', '>', '$', '%']
        # for i in range(len(punctuations)):
        data = re.sub('[^a-zA-Z]+', ' ', data)

        data = data.lower()
        words = data.split()

        reviewProb = {}
        for key in priorProbabilityDict.keys():
            reviewProb[key] = getProbability(words, wordDict[key], priorProbabilityDict[key],extraDict[key])


        categories = []
        categories.append(reviewProb["positive"] + reviewProb["truthful"])
        categories.append(reviewProb["positive"] + reviewProb["deceptive"])
        categories.append(reviewProb["negative"] + reviewProb["truthful"])
        categories.append(reviewProb["negative"] + reviewProb["deceptive"])

        i = categories.index(max(categories))

        if (i == 0):
            class1 = "positive"
            class2="truthful"
        elif(i==1):
            class1 = "positive"
            class2 = "deceptive"
        elif(i==2):
            class1 = "negative"
            class2 = "truthful"
        else:
            class1 = "negative"
            class2 = "deceptive"


        #
        # if reviewProb["positive"] < reviewProb["negative"]:
        #     class1 = "negative"
        # if reviewProb["truthful"] < reviewProb["deceptive"]:
        #     class2 = "deceptive"



        answer = class2 + "\t" + class1 + "\t" + y + "\n"

        fh.write(answer)
fh.close()














