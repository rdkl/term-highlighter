from nltk.stem.lancaster import LancasterStemmer
import re
import collections

def hamming_similarity(input_text, ref_text, allowed_dict, banned_dict):

    st = LancasterStemmer()
    
    input_text_list = re.split(', |\. |; | |\n', input_text)
    ref_text_list = re.split(', |\. |; | |\n', ref_text)
    input_text_list  = [st.stem(word) for word in input_text_list]
    ref_text_list  = [st.stem(word) for word in ref_text_list]
    
    input_counter = collections.Counter(input_text_list)
    ref_counter = collections.Counter(ref_text_list)

    sim = 0    

    if bool(allowed_dict):
        allowed_words = allowed_dict.keys()
        for word in allowed_words:
            sim += ((input_counter[word] > 0) & (ref_counter[word] > 0))
            sim += ((input_counter[word] == 0) & (ref_counter[word] == 0))
    else:
        input_words = input_counter.keys() 
        for word in input_words:
            if word not in banned_dict:
                sim += (ref_counter[word] > 0)
        
    return sim

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = 'fat cats cats cats were sitting on the mat'
    ref_text = 'fat bat'
    allowed_dict = {'fat':1, 'cat':2, 'bat':3, 'rat':6}
    banned_dict = {}    
    sim = hamming_similarity(input_text, ref_text, allowed_dict)
    print sim