import xml.etree.ElementTree as ET
import os
from bs4 import BeautifulSoup
import nltk
import string
import time

def write_pure_text(string_list, filename):
    path_to_data = "../data/fix_test_papers/"
    f = open(path_to_data + filename + "_fix", "w")
    for line in string_list:
        print >>f, line.text.encode('utf8')
    f.close()

if __name__ == "__main__":
    papers = []
    # path_to_data = "../data/test_papers/"
    path_to_data = "../data/articles/"
    stop_list = ['(', ')', 'p', '@', '%']
    letter = string.ascii_lowercase
    # stemmer = nltk.stem.SnowballStemmer("english")
    stemmer = nltk.stem.porter.PorterStemmer()
    for (dirpath, dirnames, filenames) in os.walk(path_to_data):
        papers.extend(filenames)
        break
    words_in_corpus = {}
    papers_with_words = {}
    stem_words = {}
    n_paper = 0
    
    for p in papers:
        # t1 = time.time()
        if n_paper % 100 == 0:
            print "Processed", n_paper, "papers"
        n_paper += 1
        # print "Extract words from file", papers[i]
        words_in_current_paper = set()
        f = open(path_to_data + p, "r")
        soup = BeautifulSoup(f)
        text = soup.find_all("p")
        for string in text:
            if "/" in string.text:
                fix_text = ' '.join(string.text.split("/"))
            else:
                fix_text = string.text
            
            token_string = nltk.word_tokenize(fix_text)
            words_and_pos = nltk.pos_tag(token_string)
            for w in words_and_pos:
                if len(w[0]) < 3:
                    continue                   
                if w[1] == "NN":
                    stem_word = stemmer.stem(w[0])
                    is_word = True
                    for l in stem_word:
                        if l not in letter: # "." in string.text:
                            is_word = False
                            break
                    
                    if words_in_corpus.get(stem_word) is None and is_word:
                        words_in_corpus[stem_word] = 0
                    if papers_with_words.get(stem_word) is None and is_word:
                        papers_with_words[stem_word] = 0
                    if stem_words.get(stem_word) is None and is_word:
                        stem_words[stem_word] = set()
                    
                    if is_word:
                        stem_words[stem_word].add(w[0].encode("utf8"))
                        words_in_corpus[stem_word] += 1
                        if stem_word not in words_in_current_paper:
                            papers_with_words[stem_word] += 1
                            words_in_current_paper.add(stem_word)
                                            
        # write_pure_text(text, papers[i]) 
        f.close()
        # t2 = time.time()
        # print "One paper processed in", t2 - t1
        
    print "Save words frequencies in the file..."
    with open("../data/word_frequency_porter_corpus_100", "w") as f:
        '''
        First column - stem words
        Second column - number words in all corpus
        Third column - number of papers with corresponding word
        '''
        for key in words_in_corpus:
            print >>f, key.encode("utf8"), '(' + ' '.join(stem_words[key]) + ')', str(words_in_corpus[key]), str(papers_with_words[key])
        print "Save words frequencies in the file... Done"
