import os
import re

path = "./bilara-data-published/translation/en/sujato/sutta";

class Sutta_search:
    def __init__(self, cached_directories):
        self.search_string = []
        self.search_string_cache = []
        self.cached_directories = cached_directories
        self.search_matches = []
        self.search_lines = []
        self.search_histo = []
        self.result_histo = []
        self.total_matches = 0

    def set_search_string(self, new_search_string):
        self.search_string = new_search_string
        self.search_string_cache.append(new_search_string)

    def clear_arrays(self):
        #print(self.search_lines)
        self.search_string_cache = []
        self.search_matches = []
        self.search_lines = []
        self.search_histo = []
        self.result_histo = []
        self.total_matches = 0

    def new_search(self):
        f = open(self.cached_directories, "r");
        for x in f:
            sfile = x.rstrip("\n")
            s = open(sfile, "r")
            for line in s:
                if re.search(self.search_string, line):
                    line.rstrip("\n")
                    # print (line)
                    self.search_lines.append(line)
                    res = re.split(self.search_string, line)
                    res = res[1].split()
                    res = res[0].rstrip(',.:!?\'\"”')
                    #print(res)
                    self.search_matches.append(res)

    def search_cached_lines(self):
        temp = []
        self.search_matches = []
        s = self.search_lines
        for line in s:
            if re.search(self.search_string, line):
                line.rstrip("\n")
                # print (line)
                temp.append(line)
                res = re.split(self.search_string, line)
                res = res[1].split()
                #res = res[0].rstrip(',.:!?\'\"”')
                #print(res)
                self.search_matches.append(res[0])
        self.search_lines = temp
        
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



# r = ["was staying at ", "was staying near "]
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

    def continue_search(self):
        histo1 = self.s.result_histo
        histo1_len = len(histo1)
        num_trees = 10
        if (num_trees > histo1_len):
            num_trees = histo1_len

        for k in range(num_trees):
            # print(histo1[k][0])
            r2 = self.r[0] + " " + histo1[k][0]
            self.s.clear_arrays()
            self.s.set_search_string(r2)
            self.s.new_search()
            self.s.create_histogram()
            self.s.analyze_histogram()
            self.string_caches.append(self.s.search_string_cache)
            self.histograms.append(self.s.result_histo)

def main():
    directory_list = "./sutta_files.txt"
    r = ["noble truth"]
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
    r = ["seven factors"]
    w = Word_tree(directory_list, r)
    w.start_search()
    w.continue_search()
    looplen = len(w.string_caches)
    for k in range(looplen):
        print(w.string_caches[k])
        print(w.histograms[k])

    print("searching...searching...searching...")
    
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

def main_old():
    string_caches = []
    histograms = []
    directory_list = "./sutta_files.txt"
    # r = ["was staying near"]
    # r = ["Venerable"]
    # r = ["There are"]
    # r = ["serenity of the"]
    # r = ["right effort,"]
    # r = ["Venerable Ānanda"]
    # r = ["noble truth"]
    r = ["suffering"]
    s = Sutta_search(directory_list)
    for k in r:
        s.set_search_string(k)
        s.new_search()
    s.create_histogram()
    s.analyze_histogram()
    string_caches.append(s.search_string_cache)
    histograms.append(s.result_histo)
    
    histo1 = s.result_histo
    histo1_len = len(histo1)
    num_trees = 10
    if (num_trees > histo1_len):
        num_trees = histo1_len

    for k in range(num_trees):
        # print(histo1[k][0])
        r2 = r[0] + " " + histo1[k][0]
        s.clear_arrays()
        s.set_search_string(r2)
        s.new_search()
        s.create_histogram()
        s.analyze_histogram()
        string_caches.append(s.search_string_cache)
        histograms.append(s.result_histo)


    # for i in range(1):
    #     r[0] += " " + s.result_histo[0][0] 
    #     print("searching:", r)

    looplen = len(string_caches)
    for k in range(looplen):
        print(string_caches[k])
        print(histograms[k])

if __name__ == "__main__":
    main()
