

import sys, json
filename = sys.argv[1]
output_file = "hmmmodel.txt"
emit = {}
transition = {}
context = {}



O = []
def ap_incr(arr, item):
    arr[item] = arr.get(item, 0) + 1
    
def smooth(context, transition):
    for tag in context:
        for secondTag in context:
            key_exist = transition.has_key(previous+" "+tag)
            twiceOrOnce = (1 if key_exist else 2) + 1 # Since we want to add 2 or 3
            for i in range(1, twiceOrOnce+1):
                ap_incr(transition, tag+" "+secondTag)
                ap_incr(context, tag)
            
with open(filename, mode='r+') as fp:
    for line in fp:
        previous = "<s>" # Make the sentence start
        ap_incr(context, previous)
        wordtags = line.strip(' \t\n\r').split(" ")
        for wordtag in wordtags:
            word, tag = wordtag.rsplit("/", 1)
            ap_incr(transition, previous+" "+tag) # Count the transition
            ap_incr(context, tag) # Count the context
            ap_incr(emit, tag+" "+word) # Count the emission
            previous = tag
            ap_incr(transition, previous+" </s>")
            # Print the transition probabilities
    cnt = 0
    
    smooth(context, transition)
    for key, value in transition.iteritems():
        cnt += 1
        previous, word = key.split(" ")
        v = float(value) / context[previous]
        if v > 1: print("WTF MAHI!!", value, context[previous])
        O.append(('T', key, v))
    
    for key, value in emit.iteritems():
        previous, word = key.split(" ")
        v = float(value) / context[previous]
        if v > 1: print("WTF MAHI!!", value, context[previous])
        O.append(('E', key, v))

with open(output_file, mode='w+') as fp:
    fp.write(json.dumps(O))



# get_ipython().system(u' cat hmmmodel.txt')





