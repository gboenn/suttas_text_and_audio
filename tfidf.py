#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_completion import *
import nltk
import itertools
from math import log
import sqlite3



sutta_dict_path = './sutta_dictionary.json'

class Sutta_search_tfidf(Sutta_search):
    all_words_dict = dict()
    num_docs = 20
    num_total_suttas = 3976

    def __init__(self, cached_directories):
        super().__init__(cached_directories)

    def build_dictionary(self, N=20):
        self.num_docs = N
        counter = 0
        f = open(self.cached_directories, "r")
        all_lines = []
        for x in f:
            counter += 1
            if (counter == self.num_docs):
                break
            sfile = x.rstrip("\n")            
            s = open(sfile, "r")
            for line in s:
                line = re.split("\": \"",line) #line.split(':')[1]
                if (len(line) > 1):
                    ln = line[1].rstrip("\n")
                    ln = ln.rstrip("\",").lower()
                    all_lines.append(nltk.word_tokenize(ln))
      
        res_list = []
        for k in all_lines:
            res_list = list(itertools.chain(res_list, k))
        
        # print(res_list)

        self.all_words_dict = word_frequencies(res_list)
        # print(self.all_words_dict)
        return counter

    def serialize_dict(self):
        f = open(sutta_dict_path, "w")
        f.write(json.dumps(self.all_words_dict, sort_keys=True, indent=4))

    def open_serial_dict(self):
        with open(sutta_dict_path) as json_file:
            self.all_words_dict = json.load(json_file)
            
    def print_key_sutta_dict(self, term):
        for x in self.all_words_dict:
            if (x == term):
                print("%s: %s" % (x, self.all_words_dict[x]))
    
    def idf (self, doc_matches):
        return (log(self.num_total_suttas/(1+doc_matches)))

def load_a_sutta (susnum, dirlist):
    sus = Sutta_search(dirlist)
    sus.set_search_string(susnum)
    sus.new_search()
    return sus.search_lines
    # build_a_dict (sus.search_lines)
    # print("search_lines: ", sus.search_lines)
    # fline = sus.search_lines[0].rstrip("\\n")

def build_a_dict (sutta_strings):
    all_lines = []
    for fline in sutta_strings:
        fline = re.findall(r'"(.*?)"', fline)
        all_lines.append(fline[1].lower())
           
    sutta_one_string = ''.join(all_lines)

    sutta_tokens = nltk.word_tokenize(sutta_one_string)

    return word_frequencies(sutta_tokens)
    
def count_words (sutta_dict):
    word_count = 0
    for x in sutta_dict:
        if (x != ',' or x != '‘' or x != '“' or x != '.' or x != '?' or x != '’' or x != '”'):
            # print(sutta_dict[x]) 
            word_count += sutta_dict[x]
    return word_count

def sutta_tfidf ():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] tfidf.py <search string>")
        return
    search_words = sys.argv[1]
    conn = sqlite3.connect('suttas.db')
    c = conn.cursor()

    r =[]
    r.append(search_words)
    create_directory_cache()
    directory_list = "./sutta_files.txt"
    sst = Sutta_search_tfidf(directory_list)
    w = Word_tree_nltk(directory_list, r)
    s_analysis = w.start_search()    
    print(s_analysis)
    looplen = len(w.string_caches)
    if (len(s_analysis) > 0):
        for k in range(looplen):
            if (len(s_analysis)):
                # print(w.string_caches[k])
                print("document matches:", (len(s_analysis)))

    idf = sst.idf(len(s_analysis))
    print("inverse document frequency (idf) of", search_words, "=", idf)

    search_words = search_words.lower()
    sql_cmd_1 = "INSERT INTO word (word, idf) \n"
    sql_cmd_2 = "SELECT '"+search_words+"', '"+str(idf)+"' \n"
    sql_cmd_3 = "WHERE NOT EXISTS (SELECT * FROM word WHERE word = '"+search_words+"') "
    # print (sql_cmd_1 + sql_cmd_2 + sql_cmd_3) 
    c.execute(sql_cmd_1 + sql_cmd_2 + sql_cmd_3)
    conn.commit()
    c.execute("SELECT id FROM word WHERE word = '"+search_words+"'")
    word_id = c.fetchone()[0]
    # print(word_id)

    for sta in s_analysis:
        print("-------------------------")
        sunum = sta[1] + ":"
        sulines = load_a_sutta(sunum, directory_list)
        # print(sulines)
        sutta_tokens_dict = build_a_dict(sulines)
        sutta_word_count = count_words(sutta_tokens_dict)
        occ = sutta_tokens_dict.get(search_words)
        if occ:
            term_freq = sutta_tokens_dict[search_words] / sutta_word_count
            print("sutta", sta[1], "has", sutta_word_count, "words")

            sql_cmd_1 = "INSERT INTO sutta (number,description,word_count) \n"
            sql_cmd_2 = "SELECT '"+sta[1]+"', 'empty', '"+str(sutta_word_count)+"' \n"
            sql_cmd_3 = "WHERE NOT EXISTS (SELECT * FROM sutta WHERE number = '"+sta[1]+"') "
            # print (sql_cmd_1 + sql_cmd_2 + sql_cmd_3) 
            c.execute(sql_cmd_1 + sql_cmd_2 + sql_cmd_3)
            conn.commit()

            # print(json.dumps(sutta_tokens_dict, sort_keys=True, indent=4))
            print ("term matches of", search_words, "in", sta[1], "=", sutta_tokens_dict[search_words])
            print ("term frequency (tf) of", search_words, "in", sta[1], "=", term_freq)
            tf_idf =  term_freq * idf
            print ("tf-idf of", search_words, "in", sta[1], "=", tf_idf)
            
            c.execute("SELECT id FROM sutta WHERE number = '"+sta[1]+"'")
            sutta_id = c.fetchone()[0]
            # print(sutta_id)

            sql_cmd_1 = "INSERT INTO tfidf (sutta,word,matches,tf,tfidf) \n"
            sql_cmd_2 = "VALUES ('"+str(sutta_id)+"', '"+str(word_id)+"', '"+str(occ)+"', '"+str(term_freq)+"', '"+str(tf_idf)+"')"
            
            print (sql_cmd_1 + sql_cmd_2) 
            c.execute(sql_cmd_1 + sql_cmd_2)
            conn.commit()


        else:
            print("term not found in", sta[1])

    conn.close()

def words_to_tfidf (directory_list, search_words):
    # if (len(sys.argv) < 2):
    #     print("Usage: python[3.7] tfidf.py <search string>")
    #     return
    # search_words = sys.argv[1]
    r =[]
    r.append(search_words)
    create_directory_cache()
    # directory_list = "./sutta_files.txt"
    sst = Sutta_search_tfidf(directory_list)
    w = Word_tree_nltk(directory_list, r)
    s_analysis = w.start_search()    
    print(s_analysis)
    if (len(s_analysis) < 1):
        print(search_words, "not found")
        return
    looplen = len(w.string_caches)
    if (len(s_analysis) > 0):
        for k in range(looplen):
            if (len(s_analysis)):
                # print(w.string_caches[k])
                print("document matches:", (len(s_analysis)))

    idf = sst.idf(len(s_analysis))
    print("inverse document frequency (idf) of", search_words, "=", idf)

    search_words = search_words.lower()
    # print(s_analysis)
 
    sunum = s_analysis[0][1] + ":"
    sulines = load_a_sutta(sunum, directory_list)
    # print(sulines)
    sutta_tokens_dict = build_a_dict(sulines)
    sutta_word_count = count_words(sutta_tokens_dict)
    sutta_term_count = sutta_tokens_dict.get(search_words)
    if (sutta_term_count != None):
        term_freq = sutta_term_count / sutta_word_count
        print("sutta", s_analysis[0][1], "has", sutta_word_count, "words")
        # print(json.dumps(sutta_tokens_dict, sort_keys=True, indent=4))
        print ("term matches of", search_words, "in", s_analysis[0][1], "=", sutta_term_count)
        print ("term frequency (tf) of", search_words, "in", s_analysis[0][1], "=", term_freq)
        tf_idf =  term_freq * idf
        print ("tf-idf of", search_words, "in", s_analysis[0][1], "=", tf_idf)
    

def file_of_words_to_idf ():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] tfidf.py <file>")
        return
    file_with_words = sys.argv[1]
    directory_list = "./sutta_files.txt"
    f = open(file_with_words, "r")
    for x in f:
        x = x.rstrip('\n')
        print(x)
        words_to_tfidf (directory_list, x)



def main():
    
    sutta_tfidf ()

    # file_of_words_to_idf ()
    

if __name__ == "__main__":
    main()