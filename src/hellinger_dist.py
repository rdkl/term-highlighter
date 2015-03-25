from nltk.stem.lancaster import LancasterStemmer
import re
import collections
import numpy as np

def hellinger_dist(input_text, ref_text, allowed_dict, banned_dict):

    st = LancasterStemmer()
    
    input_text_list = re.split(', |\. |; | |\n', input_text)
    ref_text_list = re.split(', |\. |; | |\n', ref_text)
    input_text_list  = [st.stem(word) for word in input_text_list]
    ref_text_list  = [st.stem(word) for word in ref_text_list]  
    
    input_counter = collections.Counter(input_text_list)
    ref_counter = collections.Counter(ref_text_list)

    s = 0  
    input_vector = []
    ref_vector = []
    inp_norm = 0
    ref_norm = 0
    
    if bool(allowed_dict):
        allowed_words = allowed_dict.keys()
        for word in allowed_words:
            input_vector.append(input_counter[word])
            ref_vector.append(ref_counter[word])
            inp_norm += input_counter[word]
            ref_norm += ref_counter[word]
    else:
        input_words = input_counter.keys() 
        for word in input_words:
            if word not in banned_dict:
                input_vector.append(input_counter[word])
                ref_vector.append(ref_counter[word])
                inp_norm += input_counter[word]
                ref_norm += ref_counter[word]
                        
    for i in range(len(input_vector)):
        s += ((input_vector[i]/float(inp_norm))**.5 - (ref_vector[i]/float(ref_norm))**.5)**2
    dist = (0.5*s)**.5
        
    return dist

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = 'fat cats cats cats were sitting on the mat'
    ref_text = 'fat bat'
    allowed_dict = {'fat':1, 'cat':2, 'bat':3, 'rat':6}
    banned_dict = {}    
    dist = hellinger_dist(input_text, ref_text, allowed_dict, banned_dict)
    print dist