from text_analysis import *
import nltk


class Sutta_search_nltk(Sutta_search):
    def __init__(self, cached_directories):
        super().__init__(cached_directories)

    def new_search_nltk(self):
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
                    
                    # possible backwards search - needs separate array
                    # bres = res[0].split()
                    # bres_1 = bres[-1]
                    # print(bres_1)
                    # self.search_matches.append(bres_1)
                    
                    res = res[1].split()
                    if (res):
                        res = res[0].rstrip(',.:!?\'\"”…')
                        self.search_matches.append(res)

class Word_tree_nltk(Word_tree):
    def __init__(self, cached_directories, search_string_array):
        self.string_caches = []
        self.histograms = []
        self.directory_list = cached_directories        
        self.r = search_string_array
        self.s_n = Sutta_search_nltk(self.directory_list)

    def reset_search(self):
        self.string_caches = []
        self.histograms = []
        self.s_n.clear_arrays()

    def start_new_search(self, search_string_array):
        self.reset_search()
        self.r = search_string_array
    
    def start_search(self):
        for k in self.r:
            self.s_n.set_search_string(k)
            self.s_n.new_search()
        self.s_n.create_histogram()
        self.s_n.analyze_histogram()
        self.string_caches.append(self.s_n.search_string_cache)
        self.histograms.append(self.s_n.result_histo)
        self.print_seach_lines()
        print("found this many times in the suttas:")
        # print(self.s.found_suttas)
        # print("found in verses:")
        # print(self.s.found_verses)
        self.analyze_occurences()
        return self.s_n.found_suttas, self.s_n.found_verses

    def analyze_occurences (self):
        d = word_frequencies(self.s_n.found_suttas)
        sfd = sort_freq_dict(d)
        len_sfd = len(sfd)
        if (len_sfd > 2 and len_sfd < 11):
            print ("The most frequent occurences are in:")
            print (sfd[0], sfd[1], sfd[2])
        else:
            print (sfd)
        return sfd

    def print_seach_lines(self):
        print("Text references found...")
        for k in self.s_n.search_lines:
            print(k)
            self.s_n.resolve_sutta_number (k, True)
            print("")

# tag parts of speech using nltk
def phrase_build_search ():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] text_analysis.py <search string>")
        return
    search_words = sys.argv[1]
    r =[]
    r.append(search_words)
    create_directory_cache()
    directory_list = "./sutta_files.txt"
    w = Word_tree_nltk(directory_list, r)
    w.start_search()    
    looplen = len(w.string_caches)
    print("words and their number of occurences in context...")
    for k in range(looplen):
        print(w.string_caches[k])
        print(w.histograms[k])

    print("composing search strings with completion...")
    new_search_strings = []
    for k in range(looplen):
        num_next_words = len(w.histograms[k])
        if (num_next_words > 0):
            for j in w.histograms[k]:
                new_branch = [] 
                old_str = w.string_caches[k][0]
                if (j[0] != ''):
                    new_branch.append(old_str)
                    new_branch.append(j[0])
                    new_search_strings.append(new_branch)

    print (new_search_strings)
    for k in new_search_strings:
        tagged = nltk.pos_tag(k)
        print(k, tagged)

def main():
    # experiment with tagging pos
    # requires import ntlk
    phrase_build_search ()
    

if __name__ == "__main__":
    main()