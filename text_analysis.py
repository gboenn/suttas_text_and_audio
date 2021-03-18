import os
import re
import sys
from pathlib import Path
import json
import glob

# for general use:
# change this to the full path to where bilara-data-published has been installed
bilara_path = "./bilara-data-published/translation/en/sujato/sutta";
pali_path = "./bilara-data-published/root/pli/ms/sutta"

pali_file_label = "_root-pli-ms.json"
sujato_file_label = "_translation-en-sujato.json"

def create_directory_cache():

    sutta_dirs = Path("./sutta_files.txt")
    if sutta_dirs.is_file():
        return

    original_stdout = sys.stdout 
    fname = []
    for root, d_names, f_names in os.walk(bilara_path):
        for f in f_names:
            p = os.path.join(root, f)
            x = re.search(".*json$", p)
            if x:
                fname.append(p)
    fname.sort()

    with open("./sutta_files.txt", 'w') as f:
        sys.stdout = f 
        for d in fname:
            print(d)
        sys.stdout = original_stdout 

def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

class Sutta_search:
    nik = ["an", "sn", "dhp"]

    def __init__(self, cached_directories):
        self.search_string = []
        self.search_string_cache = []
        self.cached_directories = cached_directories
        self.search_matches = []
        self.search_lines = []
        self.search_histo = []
        self.result_histo = []
        self.found_suttas = []
        self.found_verses = []
        self.total_matches = 0

    def set_search_string(self, new_search_string):
        self.search_string = new_search_string
        self.search_string_cache.append(new_search_string)

    def clear_arrays(self):
        #print(self.search_lines)
        self.search_string_cache = []
        self.search_matches = []
        # self.search_lines = []
        self.search_histo = []
        self.result_histo = []
        self.found_suttas = []
        self.found_verses = []
        self.total_matches = 0

    def resolve_sutta_number (self, line, prints=False):
        sutta_number = re.split("\": \"",line)[0]
        sutta_number = sutta_number.lstrip(" \"")
        sutta_main_number = re.split(":",sutta_number)
        sutta_number = sutta_main_number[0]
        verse_number = sutta_main_number[1]
        if (prints):
            for bask in self.nik: # resolving Pali for an, sn, and dhp 
                if (re.search(bask, sutta_number)):
#                    print(sutta_number)
                    dir_list = sutta_number.split('.')
                    #print(dir_list)
                    basket = bask
                    dir_an = pali_path + '/' + basket + '/' + dir_list[0]
                    if (bask == "dhp"):
                        basket = "kn"
                        dir_an = pali_path + '/' + basket
                    #print(dir_an)
                    if (Path(dir_an).is_dir()):
                        dir_file = dir_an + '/' + sutta_number + pali_file_label
                        #print(dir_file)
                        if (Path(dir_file).is_file() == False):
                            s_number = '0'
                            s_nik = dir_list[0]
                            if (len(dir_list) > 1):
                                s_number = dir_list[1].split('-')[0]
                                #print(dir_list[1].split('-'), s_number)
                            else:
                                r = re.compile("([a-zA-Z]+)([0-9]+)")
                                m = r.match(sutta_number)
                                # print(m.group(2))
                                s_number = m.group(2)
                                s_nik = m.group(1)
                                # print(s_number)
                            number = int(s_number)
                            while(number > 0): 
                                number -= 1
                                new_number = str(number)
                                if (len(dir_list) > 1):
                                    dir_file = dir_an + '/' + s_nik + '.' + new_number + '*'
                                else:
                                    dir_file = dir_an + '/' + s_nik + '/' + s_nik + new_number + '-*'
                                    #print(dir_file)
                                dir_matches = glob.glob(dir_file)
                                # print(dir_matches)
                                if (dir_matches == []):
                                    continue
                                else:
                                    #print(dir_matches[0])
                                    self.print_pali_verse(sutta_number, verse_number, dir_matches[0])
                                    break
                    else:
                        print("Error finding Pali text")
            self.print_pali_verse(sutta_number, verse_number)
            return
        self.found_suttas.append(sutta_number)
        self.found_verses.append(verse_number)
    
    def new_search(self):
        f = open(self.cached_directories, "r");
        for x in f:
            sfile = x.rstrip("\n")            
            s = open(sfile, "r")
            for line in s:
                if re.search(self.search_string, line):
                    line.rstrip("\n")
                    self.search_lines.append(line)
                    self.resolve_sutta_number (line)
                    res = re.split(self.search_string, line)
                    
                    # res_1 = res[1].split()
                    # keep punctuation?
                    # res = re.findall(r"[\w']+|[.,!?;]", res[0])[0]
                    # res_2 = res_1[0].rstrip(',.:!?\'\"”')
                    # print(res)
                    # possible backwards search - needs separate array
                    # bres = res[0].split()
                    # bres_1 = bres[-1]
                    # print(bres_1)
                    # self.search_matches.append(bres_1)
                    
                    res = res[1].split()
                    if (res):
                        res = res[0].rstrip(',.:!?\'\"”…')
                        self.search_matches.append(res)

    def search_cached_lines(self):
        temp = []
        self.search_matches = []
        s = self.search_lines
        for line in s:
            if re.search(self.search_string, line):
                line.rstrip("\n")
                temp.append(line)
                res = re.split(self.search_string, line)
                res = res[1].split()
                #res = res[0].rstrip(',.:!?\'\"”')
                if (res):
                    res = res[0].rstrip(',.:!?\'\"”…')
                    self.search_matches.append(res)
        self.search_lines = temp
        
    def print_pali_verse(self, sutta_number, verse_number, sutta_path="empty"):
        if (sutta_path == "empty"):
            f = open(self.cached_directories, "r");
            for x in f:
                sfile = x.rstrip("\n")
                snum = '\/'+sutta_number+'_'
                if (re.search(snum, sfile)):
                    #print(sutta_number, verse_number)
                    fpart = re.split(snum, sfile)[0]
                    #print(fpart)
                    fpart2 = re.split("sutta", fpart)[1] + '/'
                    #print(fpart2)
                    pali_file = pali_path + fpart2 + sutta_number + pali_file_label
                    # print (pali_file)
                    with open(pali_file) as json_file:
                        loaded_json = json.load(json_file)
                        for x in loaded_json:
                            verse = sutta_number + ":" + verse_number
                            if (x == verse):
                                print("%s: %s" % (x, loaded_json[x]))
        else:
            with open(sutta_path) as json_file:
                loaded_json = json.load(json_file)
                for x in loaded_json:
                    verse = sutta_number + ":" + verse_number
                    if (x == verse):
                        print("%s: %s" % (x, loaded_json[x]))

                
    def create_histogram(self):
        self.search_histo = []
        self.search_matches.sort()
        temp = []
        for w in self.search_matches:
            if (temp.count(w) == 0):
                p = []
                p.append(w)
                p.append(self.search_matches.count(w))
                self.search_histo.append(p)
                temp.append(w)
    
    def analyze_histogram(self):
        self.total_matches = 0
        self.result_histo = []
        sorted_histo = []
        for k in self.search_histo:
            sorted_histo.append ([k[0], k[1]])
            self.total_matches += k[1]

        # print(self.total_matches, "matches for ", self.search_string_cache)
        self.result_histo = sorted(sorted_histo, key=lambda x: x[1], reverse=True)
        # for k in self.result_histo: 
        #     print (k[0], "," , k[1], ",")

    def get_next_word(self, rank):
        return self.result_histo[rank]


class Word_tree:
    def __init__(self, cached_directories, search_string_array):
        self.string_caches = []
        self.histograms = []
        self.directory_list = cached_directories        
        self.r = search_string_array
        self.s = Sutta_search(self.directory_list)

    def reset_search(self):
        self.string_caches = []
        self.histograms = []
        self.s.clear_arrays()

    def start_new_search(self, search_string_array):
        self.reset_search()
        self.r = search_string_array
        
    def start_search(self):
        for k in self.r:
            self.s.set_search_string(k)
            self.s.new_search()
        self.s.create_histogram()
        self.s.analyze_histogram()
        self.string_caches.append(self.s.search_string_cache)
        self.histograms.append(self.s.result_histo)
        self.print_seach_lines()
        print("found in the suttas:")
        print(self.s.found_suttas)
        print("found in verses:")
        print(self.s.found_verses)
        self.analyze_occurences()

    def analyze_occurences (self):
        d = wordListToFreqDict(self.s.found_suttas)
        # print (d)
        sfd = sortFreqDict(d)
        if (len(sfd) > 2):
            print ("The three most frequent occurences are in:")
            print (sfd[0], sfd[1], sfd[3])
        else:
            print (sfd)

    def print_seach_lines(self):
        print("Text references found...")
        for k in self.s.search_lines:
            print(k)
            self.s.resolve_sutta_number (k, True)
            print("")
            
    def continue_search(self):
        histo1 = self.s.result_histo
        histo1_len = len(histo1)
        num_trees = 9999
        if (num_trees > histo1_len):
            num_trees = histo1_len

        for k in range(num_trees):
            if (histo1[k][0] == ''):
                continue
            r2 = self.r[0] + " " + histo1[k][0]
            r2 = r2.rstrip(')')
            print("continue searching for: ", r2)
            self.s.clear_arrays()
            self.s.set_search_string(r2)
            self.s.new_search()
            # self.s.search_cached_lines()
            self.s.create_histogram()
            self.s.analyze_histogram()
            self.string_caches.append(self.s.search_string_cache)
            self.histograms.append(self.s.result_histo)
            print("found in the suttas:")
            print(self.s.found_suttas)
            print("found in verses:")
            print(self.s.found_verses)
            self.analyze_occurences()
            
def simple_search ():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] text_analysis.py <search string>")
        return
    search_words = sys.argv[1]
    r =[]
    r.append(search_words)
    create_directory_cache()
    directory_list = "./sutta_files.txt"
    w = Word_tree(directory_list, r)
    w.start_search()    
    looplen = len(w.string_caches)
    print("words and their number of occurences in context...")
    for k in range(looplen):
        print(w.string_caches[k])
        print(w.histograms[k])

def main():
    
    simple_search ()
    return    

    # r.append("noble truth")
    # r.append("Venerable")
    # r.append("Mahāpajāpatī")
    # r = ["noble truth"]
    # r = ["Venerable"]
    # r = ["Mahāpajāpatī"]
    # r = ["nun"]
    # r = ["suffering"]
    # r = ["impermanence"]
    # r = ["love"]
    # r = ["Buddha"]
    # r = ["Bodhi"]
    # r = ["rebirth"]
    # r = ["three "]
    # r = ["happiness"]
    # r = ["eye contact"]
    # r = ["consciousness"]
    # r = ["name and form"]
    # r = ["was staying near"]
    # r = ["there are these"]
    # r = ["seven factors"]

    if (False):
        print("composing search strings with completion...")
        
        new_search_strings = []
        for k in range(looplen-1):
            k+=1
            num_next_words = len(w.histograms[k])
            if (num_next_words > 0):
                for j in w.histograms[k]:
                    old_str = w.string_caches[k][0]
                    connect_str = " "
                    if re.search("\s+$", old_str):
                        old_str = old_str.rstrip() 
                    if re.search("\s.$", old_str):
                        connect_str = ""
                    nstr = old_str + connect_str + j[0]
                    new_search_strings.append(nstr)
                    print (nstr)
    
    # example for printing pali verses;
    # s = Sutta_search(directory_list)
    # s.print_pali_verse("mn130", "1.1")

if __name__ == "__main__":
    main()
