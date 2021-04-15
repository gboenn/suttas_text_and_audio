#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import sqlite3

def query_tfidf ():
    if (len(sys.argv) < 2):
        print("Usage: python[3.7] query_sutta_db.py <search string>")
        return

    search_words = sys.argv[1]
    conn = sqlite3.connect('suttas.db')
    c = conn.cursor()

    search_words = search_words.lower()
    # SELECT "_rowid_",* FROM "main"."word" WHERE "word" LIKE '%root%' ESCAPE '\' ORDER BY "_rowid_" ASC LIMIT 0, 49999;
    sql_cmd_1 = "SELECT \"_rowid_\",* FROM \"main\".\"word\" WHERE \"word\" LIKE '"+search_words+"' ESCAPE \'\\' ORDER BY \"_rowid_\" ASC LIMIT 0, 49999;"
    # print (sql_cmd_1) 
    c.execute(sql_cmd_1)
    result = c.fetchall()
    # print(result)
    if (result == []):
        print("No results found. Please change the term you're looking for.")
        conn.close()
        return

    word_id = str(result[0][-1])
    # print(word_id)
    sql_cmd_1 = "SELECT \"_rowid_\",* FROM \"main\".\"tfidf\" WHERE \"word\" LIKE '"+word_id+"' ORDER BY \"tfidf\" DESC LIMIT 0, 100;"
    # print (sql_cmd_1) 
    c.execute(sql_cmd_1)
    result = c.fetchall()
    # print(result)

    # base='https://suttacentral.net/'

    res_str = "Sutta: \tmatches: \tTF: \tTF-IDF: "
    print(res_str)
    for k in result:
        # print (k)
        sutta_id = str(k[1])
        sql_cmd_1 = "SELECT \"_rowid_\",* FROM \"main\".\"sutta\" WHERE \"id\" LIKE '"+sutta_id+"' ESCAPE \'\\' ORDER BY \"_rowid_\" ASC LIMIT 0, 49999;"
        # print (sql_cmd_1) 
        c.execute(sql_cmd_1)
        result2 = c.fetchone()
        # print(result2)
        # sc_url = base + result2[1] + '/en/sujato'
        res_str = result2[1] + "\t" + str(k[3]) + "\t" + str(k[4]) + "\t" + str(k[5])
        print(res_str)

    conn.close()

def main():
    
    query_tfidf ()

    # file_of_words_to_idf ()
    

if __name__ == "__main__":
    main()