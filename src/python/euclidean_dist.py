from nltk.stem.porter import PorterStemmer
import re
import collections

def euclidean_dist(input_text, ref_text, allowed_dict, banned_dict):

    st = PorterStemmer()
    
    input_text_list = re.split(', |\. |; | |\n', input_text)
    ref_text_list = re.split(', |\. |; | |\n', ref_text)
    input_text_list  = [st.stem(word) for word in input_text_list]
    ref_text_list  = [st.stem(word) for word in ref_text_list]  
    
    input_counter = collections.Counter(input_text_list)
    ref_counter = collections.Counter(ref_text_list)

    s = 0  
    input_vector = []
    ref_vector = []
    
    if bool(allowed_dict):
        allowed_words = allowed_dict.keys()
        for word in allowed_words:
            input_vector.append(input_counter[word])
            ref_vector.append(ref_counter[word])
    else:
        input_words = dict(input_counter.items()+ref_counter.items()).keys() 
        for word in input_words:
            if word not in banned_dict:
                input_vector.append(input_counter[word])
                ref_vector.append(ref_counter[word])
                        
    inp_norm = max(sum(input_vector), 1)
    ref_norm = max(sum(ref_vector), 1)

    for i in range(len(input_vector)):
        s += (input_vector[i] - ref_vector[i])**2
    dist = s**.5
        
    return dist

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = 'fat cats, cats; cats were sitting on the mat'
    ref_text = ''
    allowed_dict = {'fat':1, 'cat':2}
    banned_dict = {}    
    dist = euclidean_dist(input_text, ref_text, allowed_dict, banned_dict)
    print dist
