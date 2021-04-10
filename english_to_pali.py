import re
import sys
import nltk

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
    lookup_word(english_word, entries)

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
    open_dictionary(dict_path, pali)
    # translate_to_pali (pali)
    # translate_word_to_pali(pali)
    translate_word_from_pali(pali)
    return

if __name__ == "__main__":
    main()

