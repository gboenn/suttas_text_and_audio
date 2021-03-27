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
                    res = nltk.word_tokenize(res[1]) # do we need nltk? only for tokenizing?
                    if (res):
                        res = res[0].rstrip(',.:!?\'\"”…-')
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
            self.s_n.new_search_nltk()
        self.s_n.create_histogram()
        self.s_n.analyze_histogram()
        self.string_caches.append(self.s_n.search_string_cache)
        self.histograms.append(self.s_n.result_histo)
        # print("found this many times in the suttas:")
        # print(self.s_n.found_suttas)
        # print("found in verses:")
        # print(self.s_n.found_verses)
        return (self.analyze_occurences())

    def analyze_occurences (self):
        d = word_frequencies(self.s_n.found_suttas)
        sfd = sort_freq_dict(d)
        return sfd

    def print_seach_lines(self):
        print("Text references found...")
        for k in self.s_n.search_lines:
            print(k)
            self.s_n.resolve_sutta_number (k, True)
            print("")

word_completion_list = []
def completion_search (directory_list, r, doc_thresh):
    w = Word_tree_nltk(directory_list, r)
    s_analysis = w.start_search()   
    looplen = len(w.string_caches)
    # the sutta references and number of occurence per sutta 
    if (len(s_analysis) > 0):
        # print("found this phrase...")
        for k in range(looplen):
            if (len(s_analysis) <= doc_thresh):
                print(w.string_caches[k])
                print("number of suttas:", (len(s_analysis)))
                print(s_analysis)
                word_completion_list.append(w.string_caches[k])
                word_completion_list.append(s_analysis)

    # print("composing search strings with completion...")
    new_search_strings = []
    for k in range(looplen):
        num_next_words = len(w.histograms[k])
        if (num_next_words > 0):
            for j in w.histograms[k]:
                new_branch = [] 
                old_str = w.string_caches[k][0]
                new_word = j[0].rstrip(',.:!?\'\"”…')
                if (new_word != ''):
                    old_str_split = old_str.split()
                    for n in old_str_split:
                        new_branch.append(n)
                    new_branch.append(new_word)
                    new_search_strings.append(new_branch)

    for k in new_search_strings:
        x = [" ".join(k)]
        completion_search(directory_list, x, doc_thresh)
    

def phrase_build_search ():
    usage_str = "Usage: python[3.7] text_analysis.py <search string> <document threshold>"
    if (len(sys.argv) < 3):
        print(usage_str)
        return
    search_words = sys.argv[1]
    doc_thresh = int(sys.argv[2]) #consider only matches < doc_thresh 

    if (doc_thresh < 1):
        print("<document threshold> must be at least 1")
        print(usage_str)
        return

    r =[]
    r.append(search_words)
    create_directory_cache()
    directory_list = "./sutta_files.txt"    
    completion_search(directory_list, r, doc_thresh)

    #print(word_completion_list)


def main():
    phrase_build_search ()
    

if __name__ == "__main__":
    main()