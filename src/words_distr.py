import pylab as pl
import numpy as np

path_to_data = "../data/"
with open(path_to_data + "word_frequency_porter_corpus_sum") as f:
    stats = f.readlines()
    words_in_corpus = np.zeros((len(stats),))
    papers_with_words = np.zeros((len(stats),))
    i = 0
    for line in stats:
        if i % 10000 == 0 and i > 0:
            print i
        split_line = line.split(" ")
        words_in_corpus[i] = int(split_line[len(split_line) - 2])
        papers_with_words[i] = int(split_line[len(split_line) - 1])
        i += 1
        
idx = np.arange(1,len(words_in_corpus) + 1)
print "Processed words in corpus data..."
sorted_words_in_corpus = np.sort(words_in_corpus)[::-1]
args_sorted_words_in_corpus = np.argsort(words_in_corpus)
words_in_corpus_labels = [str(i + 1) for i in args_sorted_words_in_corpus]
print "Processed papers with words data..."
sorted_papers_with_words = np.sort(papers_with_words)[::-1]
args_sorted_papers_with_words = np.argsort(papers_with_words)
papers_with_words_labels = [str(i + 1) for i in args_sorted_papers_with_words]

print "Plot words in corpus plot..."
pl.figure()
pl.bar(idx, sorted_words_in_corpus)
# pl.xticks(idx, words_in_corpus_labels)
pl.savefig(path_to_data + "words_in_corpus_distr.png", format="png")
pl.savefig(path_to_data + "words_in_corpus_distr.eps", format="eps")
# pl.show()
print "Plot papers with words plot..."
pl.figure()
pl.bar(idx, sorted_papers_with_words)
# pl.xticks(idx, papers_with_words_labels)
pl.savefig(path_to_data + "papers_with_words_distr.png", format="png")
pl.savefig(path_to_data + "papers_with_words_distr.eps", format="eps")
pl.show()
