from hellinger_dist import hellinger_dist
from euclidean_dist import euclidean_dist
from hamming_similarity import hamming_similarity

def choose_reference(input_text, ref_list, metrics, read_from_file):

    allowed_dict = {}
    
    if read_from_file:
        f = open('../data/dict.txt', 'r')
        line_list = f.readlines()
        for line in line_list:
            word = line.strip()
            allowed_dict[word] = 1   
        f.close()
        
    dist_list = []
    min_dist = 100  
    max_sim = 0
    idx = 100
    
    if metrics == 'hellinger':
        for ref_text in ref_list:
            dist = hellinger_dist(input_text, ref_text, allowed_dict, {})
            dist += 0.2*hellinger_dist(input_text, ref_text, {}, {})
            dist_list.append(dist)
            if dist < min_dist:
                idx = len(dist_list)-1
                min_dist = dist
    
    if metrics == 'euclidean':
        for ref_text in ref_list:
            dist = euclidean_dist(input_text, ref_text, allowed_dict, {})
            dist += 0.2*euclidean_dist(input_text, ref_text, {}, {})
            dist_list.append(dist)
            if dist < min_dist:
                idx = len(dist_list)-1
                min_dist = dist
    
    if metrics == 'hamming':
        for ref_text in ref_list:
            dist = hamming_similarity(input_text, ref_text, allowed_dict, {})
            dist += 0.1*hamming_similarity(input_text, ref_text, {}, {})
            dist_list.append(dist)
            if dist > max_sim:
                idx = len(dist_list)-1
                max_sim = dist
                
    return idx
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = 'fat cats, cats; cats were sitting on the protein mat'
    ref_list = ['fat cat', 'protein', 'fat cats, cats; cats were sitting on the mat', 'bat']
    allowed_dict = {}
    idx = choose_reference(input_text, ref_list, 'hamming', True)
    print idx


