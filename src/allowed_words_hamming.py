from nltk.stem.lancaster import LancasterStemmer
import re
import collections

def allowed_words_hamming(inputText, refText, allowedDict):

    st = LancasterStemmer()
    
    inputTextList = re.split(', |\. |; | |\n', inputText)
    refTextList = re.split(', |\. |; | |\n', refText)
    inputTextList  = [st.stem(word) for word in inputTextList]
    refTextList  = [st.stem(word) for word in refTextList]
    
    inputCounter = collections.Counter(inputTextList)
    refCounter = collections.Counter(refTextList)
    
    allowedWords = allowedDict.keys()
    
    dist = 0
    
    for word in allowedWords:
        dist += ((inputCounter[word] > 0) & (refCounter[word] > 0))
        dist += ((inputCounter[word] == 0) & (refCounter[word] == 0))
        
    return dist

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    inputText = 'fat cats cats cats were sitting on the mat'
    refText = 'fat bat'
    allowedDict = {'fat':1, 'cat':2, 'bat':3, 'rat':6}
    dist = allowed_words_hamming(inputText, refText, allowedDict)
    print dist