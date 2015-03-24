from nltk.stem.lancaster import LancasterStemmer
import re
import collections

def banned_words_hamming(inputText, refText, bannedDict):

    st = LancasterStemmer()
    
    inputTextList = re.split(', |\. |; | |\n', inputText)
    refTextList = re.split(', |\. |; | |\n', refText)
    inputTextList  = [st.stem(word) for word in inputTextList]
    refTextList  = [st.stem(word) for word in refTextList]
    
    inputCounter = collections.Counter(inputTextList)
    refCounter = collections.Counter(refTextList)
    inputWords = inputCounter.keys()    
    
    dist = 0
    
    for word in inputWords:
        if word not in bannedDict:
            dist += (refCounter[word] > 0)
        
    return dist

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    inputText = 'fat cats cats cats were sitting on the mat'
    refText = 'fat bat cat'
    bannedDict = {'fat':1, 'rat':6}
    dist = banned_words_hamming(inputText, refText, bannedDict)
    print dist