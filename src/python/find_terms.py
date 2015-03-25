import wikipedia

def find_terms(terms, results, get_best_summary):
    max_sentences = 10
    
    hints = {}
    for term in terms:
        search_results = wikipedia.search(term, results)
        summaries = []
        for article in search_results:
            print term, article
            try:
                summaries += [wikipedia.summary(article, max_sentences)]
            except:
                pass
        
        summary = get_best_summary(summaries)
        if len(summary) > 0:
            hints[term] = summary
        
    return hints
    
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    def get_summary(summaries):
        return summaries[0]
    
    hints = find_terms(["neuron", "serine", "lysis"], 8, get_summary)
    for term in hints:
        print "-" * 80
        print term
        print hints[term]
        print "-" * 80 + "\n\n"
