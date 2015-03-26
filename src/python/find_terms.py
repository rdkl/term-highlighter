from multiprocessing import Pool
import wikipedia
import time 

import gevent.threadpool as tp

#-----------------------------------------------------------------------------
def remove_non_ascii_characters(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

#-----------------------------------------------------------------------------
def get_expected_pages_names(args):
    (term, number_of_results) = args
    result = (term, wikipedia.search(term, number_of_results))
    return result

#-----------------------------------------------------------------------------
def get_one_summary(args):
    (term, article, max_sentences) = args
    try:
        summary = wikipedia.summary(article, max_sentences)
    except:
        summary = ""
    return (remove_non_ascii_characters(summary), article, term)

#-----------------------------------------------------------------------------
def find_terms(terms, 
               number_of_results, 
               get_best_summary_index, 
               show_time = False):
    max_sentences = 10
    if show_time:
        start_time = time.time()
    
    hints = {}
    
    #p = Pool(8)
    p = tp.ThreadPool(8)
    tasks = ((term, number_of_results) for term in terms)
    search_results = dict(p.map(get_expected_pages_names, tasks))
    if show_time:
        print "Time: %.2f" % (time.time() - start_time)
    
    donwload_tasks = ((term, article, max_sentences) 
                      for term in search_results
                      for article in search_results[term])
    
    summaries_and_terms = p.map(get_one_summary, donwload_tasks)
    if show_time:
        print "Time: %.2f" % (time.time() - start_time)
    
    summaries = {}
    articles = {}
    for summary, article_name, term in summaries_and_terms:
        if len(summary) == 0:
            continue
        
        if term in summaries:
            summaries[term] += [summary]
            articles[term] += [article_name]
        else:
            summaries[term] = [summary]
            articles[term] = [article_name]
    
    if show_time:
        print "Time: %.2f" % (time.time() - start_time)
    
    for term in summaries:
        index = get_best_summary_index(summaries[term])
        hints[term] = [articles[term][index], summaries[term][index]]
    return hints
    
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    start_time = time.time()
    
    def get_summary(summaries):
        return 0
    
    hints = find_terms(["neuron", "serine", "lysis", "mitosis", 
                        "redox", "cyst", "ligase"], 5, get_summary)
    for term in hints:
        print "-" * 80
        print term
        print hints[term][0]
        print hints[term][1]
        print "-" * 80 + "\n\n"

    print "Time: %.2f" % (time.time() - start_time)