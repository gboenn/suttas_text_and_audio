from text_analysis import *

def main():
    # simple_search ()
    create_directory_cache()
    directory_list = "./sutta_files.txt"
    f = open("test_strings.txt", "r");
    counter = 0
    for x in f:
        x = x.rstrip("\n") 
        if (x == ''):
            continue
        print("START search #", counter, "for:" , x)
        counter += 1
        r =[]
        r.append(x)
        w = Word_tree(directory_list, r)
        w.start_search()
        looplen = len(w.string_caches)
        print("words and their number of occurences in context...")
        for k in range(looplen):
            print(w.string_caches[k])
            print(w.histograms[k])

if __name__ == "__main__":
    main()