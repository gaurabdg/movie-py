import json
from preprocessing.txt_processor import txt_processor


def predict(indexedDirectory, query):
    '''
    Return a list of top results by tfidf cosine distance
    '''
    with open(indexedDirectory + "/stats.csv",'r') as f:
        index = json.loads(f.readline())
    tokenizer = txt_processor()
    queryList = tokenizer.tokenize(query)
    # print(index["Children of Men.txt"])

    results = []
    for p in index:
        score = 0.00000
        for q in queryList:
            score += index[p].get(q,0)
        #print(p[:-4] + "   :   " + str(score))
        if score != 0:
            results.append((p,score))

    #Showing movies only with tfidf score 0.5 of top score
    results.sort(key = lambda x:x[1],reverse=True)
    if len(results) == 0:
        return []
    _,s = results[0]
    ret = []
    for r in results:
        movie,score = r
        if s*0.2 > score:
            break
        print(movie[:-4])
        ret.append(movie)
    return ret

if __name__ == "__main__":
    query = input("Enter your query: ")
    predict("./clean_data", query)
