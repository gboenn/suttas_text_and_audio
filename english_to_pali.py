import re
import sys
import nltk

dict_path = "./dictionary/pe2_Pali_English_Dictionary_extract_DPR_2018.js"
pali = []

def translate_word_to_pali():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] english_to_pali.py <word>")
        return
    english_word = sys.argv[1]
    lookup_word(english_word)

def translate_to_pali():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] english_to_pali.py <filename>")
        return
    english_word_list = sys.argv[1]
    f = open(english_word_list, "r");
    for x in f:
        x = x.rstrip("\n")
        lookup_word(x)

def lookup_word(w):
    w = w.lower()
    rw = " "+w+"\\b"
    print("==================")
    print("Looking up:", w)
    for p in pali:
        s = p.lower()
        if re.search(rw, s):
            print(w, p)

def open_dictionary(path):
    f = open(dict_path, "r");
    for x in f:
        x = x.rstrip("\n")
        pali.append(x)    

def main():
    open_dictionary(dict_path)
    # translate_to_pali ()
    translate_word_to_pali()
    return

if __name__ == "__main__":
    main()

