

if __name__ == "__main__":
    path_to_data = "../data/"
    stem_words = {}
    words_in_corpus = {}
    papers_with_words = {}
    with open(path_to_data + "word_frequency_porter_corpus") as f:
        for line in f.readlines():
            parts = line.split(" ")
            key = parts[0]
            print "Key is", key
            init_words = set()
            for i in xrange(1, len(parts) - 2):
                if "(" in parts[i] and ")" in parts[i]:
                    init_words.add(parts[i][1:len(parts[i]) - 1])
                    break
                if "(" in parts[i]:
                    init_words.add(parts[i][1:])
                elif ")" in parts[i]:
                    init_words.add(parts[i][:len(parts[i]) - 1])
                else:
                    init_words.add(parts[i])
                
            freq_in_corpus = int(parts[len(parts) - 2])
            num_papers = int(parts[len(parts) - 1])
            if words_in_corpus.get(key) is None:
                words_in_corpus[key] = freq_in_corpus
            else:
                words_in_corpus[key] += freq_in_corpus
            if papers_with_words.get(key) is None:
                papers_with_words[key] = num_papers
            else:
                papers_with_words[key] += num_papers
            if stem_words.get(key) is None:
                stem_words[key] = init_words
            else:
                stem_words[key] = set((list(stem_words[key])) + list(init_words))
                
    with open(path_to_data + "word_frequency_porter_corpus_sum", "w") as f:
        for key in words_in_corpus:
            print >>f, key.encode("utf8"), '(' + ' '.join(stem_words[key]) + ')', str(words_in_corpus[key]), str(papers_with_words[key])
        print "Save words frequencies in the file... Done"
