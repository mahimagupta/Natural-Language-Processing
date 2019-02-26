import json
import re
import collections
import os
import glob
import sys

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
def getInput(filename):

    modelFile = open(filename, 'r')
    model = json.load(modelFile)
    modelFile.close()
    return model

def classify(tokens, model):

    y = 0
    for word in tokens:
        if model[0].get(word, None) == None:
            continue
        y += tokens[word] * model[0][word]

    y += model[1]

    if y <= 0:
        return -1
    return 1

def getReviews():
    files = glob.glob(os.path.join(sys.argv[2], '*/*/*/*.txt'))

    data = []

    for f in files:

        # if not "/fold1/" in f:
        #     continue

        fh = open(f,"r")
        data.append( (tokenizeReview(fh.read()), f) )
        fh.close()

    return data

def getClassName(classtype, classValue):
    if classtype == "class2":
        if classValue == 1:
            return "truthful"
        else :
            return "deceptive"
    else :
        if classValue == 1:
            return "positive"
        else:
            return "negative"



def processReviews(reviews, class1Model, class2Model, filename):

    fh = open(filename,"w")

    for review in reviews:
        class1Result = classify(review[0], class1Model)
        class2Result = classify(review[0], class2Model)

        result = getClassName("class2", class2Result) +" "+ getClassName("class1", class1Result)+"\t" + review[1]+"\n"
        fh.write(result)
    fh.close()

if __name__ == "__main__":

    reviews = getReviews()

    model = getInput(sys.argv[1])
    class1Model = model[0]
    class2Model = model[1]
    processReviews(reviews, class1Model, class2Model, "percepoutput.txt")

