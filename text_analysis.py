import os
import re

path = "./bilara-data-published/translation/en/sujato/sutta";

r = ["was staying at ", "was staying near "]
# r = ["Venerable "]
# r = ["Mahāpajāpatī"]
# r = ["nun named"]
# r = ["suffering"]
# r = [" light. "]
# r = ["heart full of"]
# r = [" happiness of"]
# r = ["right efforts"]
# r = ["mindfulness of"]
# r = ["five "]
matches = []
histo = []
def grep_suttas (regex_string):
    f = open("sutta_files.txt", "r");
    for x in f:
        sfile = x.rstrip("\n")
        s = open(sfile, "r")
        for line in s:
            if re.search(regex_string, line):
                line.rstrip("\n")
                print (line)
                res = re.split(regex_string, line)
                res = res[1].split()
                res = res[0].rstrip(',.:!?\'\"”')
                # res_2 = res_1.rstrip('.')
                # res = res_2.rstrip(':')
                print(res)
                matches.append(res)

def histo_words ():
    matches.sort()
    temp = []
    for w in matches:
        if (temp.count(w) == 0):
            p = []
            p.append(w)
            p.append(matches.count(w))
            histo.append(p)
            temp.append(w)

for k in r:
    print("searching for: ", k)
    grep_suttas(k)

histo_words()

total = 0
sorted_histo = []
for k in histo:
    sorted_histo.append ([k[0], k[1]])
    total += k[1]

print(total, "matches")
result_histo = sorted(sorted_histo, key=lambda x: x[1], reverse=True)
for k in result_histo: 
    print (k[0], "," , k[1], ",")

