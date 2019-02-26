import os
import sys
import glob
import collections
import random
import json
import re

MaxIter = 30

def getInput():

    files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))

    data = []

    for f in files:

        class1, class2, fold, filename = f.split('/')[-4:]

        if "positive" in f:
            class1 = 1
        else:
            class1 = -1

        if "truthful" in f:
            class2 = 1
        else:
            class2 = -1

        fh = open(f, "r")
        review = fh.read()
        fh.close()
        data.append( (review,class1,class2) )
    print(len(data))
    return data


def tokenizeReview(review):
    review = review.strip("\n").lower()
    review = re.sub('[^a-zA-Z!1-9]+', ' ', review)
    stop_words = ["a", "about", "am", "at", "above", "after", "an", "and", "again", "all", "already", "any", "are",
                  "as",
                  "be",
                  "become", "before", "behind", "being", "below", "because", "but", "by",
                  "both", "can", "could", "come", "coming", "do", "did", "does", "doing", "during", "each", "for",
                  "from",
                  "further", "has", "had", "have", "having", "he", "him", "himself",
                  "herself", "he'd", "he's", "he'll", "her", "here", "here's", "how", "how's", "i", "i'd", "i'm",
                  "i'll",
                  "i've", "if", "into", "in", "is", "it", "it's", "its", "itself",
                  "inside", "let", "let's", "me", "mine", "more", "most", "my", "myself", "of", "on", "once", "only",
                  "one",
                  "oneself", "or", "our", "ourself", "ours", "out", "ought", "onto", "own", "put", "quite",
                  "over", "she", "she'd", "south", "some", "same", "she'll", "she's", "so", "should", "such", "then",
                  "than", "to",
                  "towards", "the", "that", "this", "that's", "there", "there's", "their", "they",
                  "they're", "them", "themselves", "themself", "these", "those", "they'd", "they'll", "they've", "too",
                  "through", "under", "up", "until", "unless", "very", "were",
                  "was", "which", "who", "whose", "who's", "whom", "where", "what", "what'll", "who'd", "why", "why'd",
                  "when's", "when", "where's", "what's", "where'll", "while", "with", "you", "you'd",
                  "yourself", "your", "yours", "you're", "we", "we're", "yourselves"]

    review = review.split(" ")

    tokens = collections.defaultdict(int)


    for word in review:

        if "!" in word:
            tokens["!"] += 1

        if word in stop_words:
            continue

        #word = word.rstrip(",./;:'!)]}").lstrip(",./;:'![{(")


        if not word.strip() == "":
            tokens[word] += 1

    return tokens


def createVanillaPerceptron(data, classIndex, weight):

    global  MaxIter
    b = 0
    iterationCount = 0
    updateCount = 0
    while(iterationCount < MaxIter and updateCount<2*len(data)):
        iterationCount += 1
        length = len(data)

        rand = list(range(length))
        random.shuffle(rand)

        for i in rand:
            review = data[i][0]
            y = data[i][classIndex]

            tokenList = tokenizeReview(review)

            a = 0
            for word in tokenList.keys():
                a += weight[word]*tokenList[word]
            a += b

            if y*a <= 0:
                for word in tokenList:
                    weight[word] += y*tokenList[word]
                b += y
                updateCount = 0
            else:
                updateCount += 1

    print("Iteration Count : " + str(iterationCount))

    return (weight,b)


def createAveragedPerceptron(data, classIndex, weight, cached_weight):

    global  MaxIter
    b = 0
    beta = 0
    c = 1

    iterationCount = 0
    updateCount = 0
    while (iterationCount < MaxIter and updateCount < 2 * len(data)):
        iterationCount += 1
        length = len(data)

        rand = list(range(length))
        random.shuffle(rand)

        for i in rand:
            review = data[i][0]
            y = data[i][classIndex]

            tokenList = tokenizeReview(review)

            a = 0
            for word in tokenList.keys():
                a += weight[word]*tokenList[word]
            a += b

            if y*a <= 0:
                for word in tokenList:
                    weight[word] += y*tokenList[word]
                    cached_weight[word] += y*c*tokenList[word]

                b += y
                beta += y*c

                updateCount = 0

            else:
                updateCount += 1

            c += 1

    for word in weight:
        weight[word] = weight[word] - (cached_weight[word]/c)

    print("Iteration Count : " + str(iterationCount))
    return weight, b - (beta/c)

def writeModel(filename, data):
    modelFile = open(filename, 'w')
    json.dump(data, modelFile, indent=5, ensure_ascii=False)
    modelFile.close()


if __name__ == "__main__":
    data = getInput()

    vanillaPerceptClass1 = createVanillaPerceptron(data, 1, collections.defaultdict(int))
    vanillaPerceptClass2 = createVanillaPerceptron(data, 2, collections.defaultdict(int))

    averagedPerceptClass1 = createAveragedPerceptron(data, 1, collections.defaultdict(int), collections.defaultdict(int))
    averagedPerceptClass2 = createAveragedPerceptron(data, 2, collections.defaultdict(int), collections.defaultdict(int))

    writeModel("vanillamodel.txt", [vanillaPerceptClass1,vanillaPerceptClass2])
    writeModel("averagedmodel.txt", [averagedPerceptClass1,averagedPerceptClass2])
