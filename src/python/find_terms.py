from multiprocessing import Pool
import wikipedia
import time 


#-----------------------------------------------------------------------------
def get_expected_pages_names(args):
    (term, number_of_results) = args
    return (term, wikipedia.search(term, number_of_results))

#-----------------------------------------------------------------------------
def get_one_summary(args):
    (term, article, max_sentences) = args
    try:
        summary = wikipedia.summary(article, max_sentences)
    except:
        summary = ""
    return (summary, term)

#-----------------------------------------------------------------------------
def find_terms(terms, number_of_results, get_best_summary):
    max_sentences = 10
    
    hints = {}
    
    p = Pool(20)
    tasks = ((term, number_of_results) for term in terms)
    search_results = dict(p.map(get_expected_pages_names, tasks))
    
    donwload_tasks = ((term, article, max_sentences) 
                      for term in search_results
                      for article in search_results[term])
    
    summaries_and_terms = p.map(get_one_summary, donwload_tasks)
    
    summaries = {}
    
    for summary, term in summaries_and_terms:
        if len(summary) == 0:
            continue
        
        if term in summaries:
            summaries[term] += [summary]
        else:
            summaries[term] = [summary]
            
    for term in summaries:
        hints[term] = get_best_summary(summaries[term])

    return hints
    
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    start_time = time.time()
    
    def get_summary(summaries):
        return summaries[0]
    
    hints = find_terms(["neuron", "serine", "lysis"], 4, get_summary)
    for term in hints:
        print "-" * 80
        print term
        print hints[term]
        print "-" * 80 + "\n\n"

    print "Time: %.2f" % (time.time() - start_time)