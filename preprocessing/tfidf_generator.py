from nltk.corpus import stopwords
from txt_processor import txt_processor
import os
import math
import json

stopwords = [i for i in stopwords.words("english")]

'''
Returns document level statistics
'''
def docFreqCount(documentPath):
    fileText = open(documentPath).read()
    tokenizer = txt_processor()
    tokens = tokenizer.tokenize(fileText)
    tokens = [i for i in tokens if i not in stopwords]
    counts = dict()
    for t in tokens:
        counts[t] = counts.get(t,0) + 1
    return (len(tokens),counts)

'''
Generates tf-idf-vectors for directory full of documents
Saved in stats.csv in the same directory
'''

def tf_idf_vectors(directory):
    vectors = dict()
    wordDocumentCount = dict()
    if os.path.isdir(directory):
        allFiles = os.listdir(directory)
        files = []
        ## print(allFiles[0][-4:])
        for f in allFiles:
            if f[-4:] == ".txt":
                files.append(f)
        numDocs = len(files)
        for f in files:
            docLen,tokens = docFreqCount(os.path.join(directory,f))
            for t in tokens:
                wordDocumentCount[t] = 1 + wordDocumentCount.get(t,0)
            vectors[f] = tokens

        for f in files:
            tokens = vectors[f]
            for t in tokens:
                vectors[f][t] = 100000 * vectors[f][t] * math.log(numDocs/wordDocumentCount[t],10) / docLen

        with open(os.path.join(directory, "stats.csv"), 'w') as f:
            f.write(json.dumps(vectors))

    else:
        raise ValueError("Arg is not the path of a directory")

if __name__ == "__main__":
    tf_idf_vectors("../clean_data")
