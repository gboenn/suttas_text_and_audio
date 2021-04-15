#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
# import nltk

dict_path = "./dictionary/pe2_Pali_English_Dictionary_extract_DPR_2018.js"
dict_path_long = "./dictionary/pe4_Pali_English_Declension_Dict_@DPR_2018.js"
# pali = []

def translate_word_from_pali(entries):
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] english_to_pali.py <pali word>")
        return
    pali_word = sys.argv[1]
    lookup_pali(pali_word, entries)

def translate_word_to_pali(entries):
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] english_to_pali.py <english word>")
        return
    english_word = sys.argv[1]
    result = []
    lookup_word_to_file(english_word, entries, result)
    print(result)
    with open("./pali_lookup_return.txt", 'w') as f:
        for k in result:
            f.write(k+'\n')

def translate_to_pali(entries):
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] english_to_pali.py <filename>")
        return
    english_word_list = sys.argv[1]
    f = open(english_word_list, "r");
    for x in f:
        x = x.rstrip("\n")
        lookup_word(x, entries)

def lookup_word(w, entries):
    w = w.lower()
    rw = " "+w+"\\b"
    print("==================")
    print("Looking up:", w)
    for p in entries:
        s = p.lower()
        if re.search(rw, s):
            print(w, p)

def lookup_word_to_file(w, entries, ret_array):
    w = w.lower()
    rw = " "+w+"\\b"
    print("==================")
    print("Looking up:", w)
    for p in entries:
        s = p.lower()
        if re.search(rw, s):
            print(w, p)
            ret_array.append(p)

def lookup_pali(w, entries):
    w = w.lower()
    # rw = "'"+w+"'"
    rw = w
    print("==================")
    print("Looking up:", w)
    for p in entries:
        s = p.lower()
        if re.search(rw, s):
            print(w, p)

def open_dictionary(path, entries):
    f = open(path, "r")
    for x in f:
        x = x.rstrip("\n")
        entries.append(x)

def main():
    pali = []
    # if "UTF-8" in sys.stdout.encoding:
    #     print("can print diacritics.")
    # else:
    #     print("can't print Pali special chars.")
    open_dictionary(dict_path_long, pali)
    # translate_to_pali (pali)
    #translate_word_to_pali(pali)
    translate_word_from_pali(pali)
    
    return

if __name__ == "__main__":
    main()

