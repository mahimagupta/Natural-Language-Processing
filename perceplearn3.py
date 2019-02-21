import os
import sys
import glob
import collections
import math
import json
import re

from collections import Counter 
wordcount ={}

files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
test_by_class = collections.defaultdict(list)
train_by_class = collections.defaultdict(list)

for f in files:
    class1, class2, fold, filename = f.split('/')[-4:]
    if fold == 'fold1':
        test_by_class[class1+class2].append(f)
    else:
        train_by_class[class1 + class2].append(f)
    #print(f)

    # if "positive" in f:
    #
    #
    # if "negative" in f:
    #
    #
    #
    # if "truthful" in f:
    #
    #
    #
    # if "deceptive" in f:




a=train_by_class.keys()
b=train_by_class.values()
# print(a)
#print(b)
words=[]
class1 = ""
class2 = ""
for key in train_by_class.keys():
        # x = train_by_class[a]
    for y in train_by_class[key]:
        #totalsize += 1
            #totalsize = calculateTotalSize()
        class1, class2, fold, filename = y.split('/')[-4:]

        # class1 = class1.split("_")[0]
        # class2 = class2.split("_")[0]

        fil = open(y, "r")
        data = fil.read()
    # print(data)
        data = re.sub('[^a-zA-Z]+', ' ', data)
        data = data.lower()
        words_list = data.split()
        words =[]
        stop_words = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'this', 'to', 'was', 'were', 'will', 'with']
        for word in words_list:
            if (word not in stop_words):
                words.append(word)
            #print(words)
        for everyword in words:
            if word not in wordcount:
                wordcount[word] = 0
            wordcount[word] += 1
            print(wordcount)


# def activationFunction(feature, weights):
#     activation  = 0
#     for word in sorted(feature):
#         if word not in weights['Vanilla']:
#             weights['Vanilla'][word] = 0
#             weights['Average'][word] = 0
#             activation += 0
#
#         else:
#             activation += feature[word] * weights['Vanilla'][word]
#
#     return activation + weights['Vanilla']['bias']
#
#
# def vanillaUpdateWeights(feature, weights, label):
#     for word in feature:
#         weights[word] += label*feature[word]
#     weights['bias'] += label
#
#
# def averageUpdateWeights(feature, weights, label, avgCounter):
#     for word in feature:
#         weights[word] += label*feature[word]*avgCounter
#     weights['bias'] += label*avgCounter
#
#
# def averagePerceptron(weightsVan, weightsAvg, counter):
#     for word in weightsAvg:
#         weightsAvg[word] = weightsVan[word] - (weightsAvg[word]/counter)
#
#
# def trainPerceptron(sentFeatures, sentWords):
#     weights = {'TruthfulDeceptive': {'Vanilla': {'bias': 0}, 'Average': {'bias': 0}},
#                'PositiveNegative': {'Vanilla': {'bias': 0}, 'Average': {'bias': 0}}}
#     classes = {'Truthful': 1, 'Deceptive': -1, 'Positive': 1, 'Negative': -1}
#     label = {'TruthfulDeceptive': 1, 'PositiveNegative': 1}
#     avgCounter = 1
#     iterations = 20
#     z = 0
#     stopIterations = False
#
#     while (z < iterations):
#         for i in range(0, len(sentFeatures)):
#
#             label['TruthfulDeceptive'] = classes[sentWords[i][1]]
#             label['PositiveNegative'] = classes[sentWords[i][2]]
#
#             activation = activationFunction(sentFeatures[i], weights['TruthfulDeceptive'])
#             if label['TruthfulDeceptive'] * activation <= 0:
#                 vanillaUpdateWeights(sentFeatures[i], weights['TruthfulDeceptive']['Vanilla'], label['TruthfulDeceptive'])
#                 vanillaUpdateWeights(sentFeatures[i], weights['TTruthfulDeceptive']['Average'], label['TruthfulDeceptive'], avgCounter)
#
#             activation = activationFunction(sentFeatures[i], weights['PositiveNegative'])
#
#             if label['PositiveNegative'] * activation <= 0:
#                 vanillaUpdateWeights(sentFeatures[i], weights['PositiveNegative']['Vanilla'], label['PositiveNegative'])
#                 vanillaUpdateWeights(sentFeatures[i], weights['PositiveNegative']['Average'], label['PositiveNegative'], avgCounter)
#
#             avgCounter += 1
#
#         z += 1
#
#     averagePerceptron(weights['TruthfulDeceptive']['Vanilla'], weights['TruthfulDeceptive']['Average'], avgCounter)
#     averagePerceptron(weights['PositiveNegative']['Vanilla'], weights['PositiveNegative']['Average'], avgCounter)
#
#     writeToFile(weights)
#
#
# def writeToFileS(weights, writeFilePath):
#     pass
#
# def writeToFile(weights):
#     writeFilePath = 'vanillamodel.txt'
#     writeFile = open(writeFilePath, mode='w', encoding='UTF-8')
#     writeFile.write(json.dumps(weights['TruthfulDeceptive']['Vanilla']))
#     writeFile.write("\n")
#     writeFile.write(json.dumps(weights['PositiveNegative']['Vanilla']))
#     writeFile.write("\n")
#
#     writeFilePath = 'averagedmodel.txt'
#     writeFile = open(writeFilePath, mode='w', encoding='UTF-8')
#     writeFile.write(json.dumps(weights['TruthfulDeceptive']['Average']))
#     writeFile.write("\n")
#     writeFile.write(json.dumps(weights['PositiveNegative']['Average']))
#     writeFile.write("\n")
