
import sys, json, math
import pickle

reload(sys)
sys.setdefaultencoding('utf8')
filename = sys.argv[1]
model_file = "hmmmodel.txt"
output_file = "hmmoutput.txt"
transition = {}
emission = {}
possible_tags = {}
output_lines = []


O = []
with open(model_file, mode='r+') as fp:
    O = json.load(fp, encoding="utf-8")
    
for type, _ctx, prob in O:
    context, word = _ctx.split(" ")
    print word
    possible_tags[context] = 1 
    if type == "T":
        transition[_ctx] = prob
    else:
        emission[_ctx] = prob


with open(filename, mode='r+') as fp:
    for line in fp:
        words = line.split(" ")
        I = len(words)
        best_score = {}
        best_edge = {}
        best_score["0 <s>"] = 0 # Start with <s>
        best_edge["0 <s>"] = None
        for i in range(0, I):
            for prev in possible_tags.keys():
                for next in possible_tags.keys():
                    if not ((str(i)+" "+prev) in best_score and (prev+" "+next) in transition):
                        continue
                        
                    pt = transition[prev+" "+next]+1
                    pe = emission.get(next+" "+words[i], 0)+1
                    score = best_score[str(i)+" "+prev] - math.log(pt) - math.log(pe)
                    key = str(i+1)+" "+next
                    if key not in best_score or best_score[key] > score:
                        best_score[key] = score
                        best_edge[key] = str(i)+" "+prev
        # Finally, do the same for </s>
        for prev in possible_tags.keys():
            next = "</s>"
            if not ((str(i)+" "+prev) in best_score and (prev+" "+next) in transition):
                continue
            pt = transition[prev+" "+next]+1
            pe = emission.get(next+" "+words[i], 0)+1
            score = best_score[str(i)+" "+prev] - math.log(pt) - math.log(pe)
            key = str(i+1)+" "+next
            if key not in best_score or best_score[key] > score:
                best_score[key] = score
                best_edge[key] = str(i)+" "+prev
        tags = []
        if I == 1:
            output_lines.append("")
            continue
        next_edge = best_edge[str(I)+" </s>"]
        while next_edge != "0 <s>":
            position, tag = next_edge.split(" ")
            tags.append(tag)
#             print("Next Edge:", next_edge, "appended tag:", tag)
            next_edge = best_edge[next_edge]
        tags.reverse()
#         print ",".join(tags)
        out = map(lambda (w,t): "/".join([w,t]), zip(words, tags))
        output_lines.append(" ".join(out))
        print output_lines[-1]

with open('output_file', 'wb') as fp:
    pickle.dump(output_lines[-1], fp)



