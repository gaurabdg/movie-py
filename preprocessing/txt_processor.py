from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import ngrams
import string, os, math


class txt_processor:
    def __init__(self):
        self.tokens = []
        self.stopwords = [str(w) for w in stopwords.words("english")]

    def tokenize(self,txt):
        tokens = word_tokenize(txt)
        tokens = [i for i in tokens if i not in string.punctuation]
        tokens = [word for word in tokens if len(word)>1 and word.isalpha()] #removing isn't, can't, doesn't etc.
        tokens = [word.lower() for word in tokens]
        #tokens = self.stem(tokens)
        #tokens = tokens + self.ngram_tokenize(2,txt)
        #tokens = tokens + self.ngram_tokenize(3,txt)
        #tokens = tokens + self.ngram_tokenize(4,txt)
        return tokens

    def ngram_tokenize(self,n,tokens):
        # if n is 1:
        #     unigram = [' '.join(i) for i in ngrams(tokens,1)]
        #     return unigram
        if n is 2:
            bigram = [' '.join(i) for i in ngrams(tokens,2)]
            return bigram
        elif n is 3:
            trigram = [' '.join(i) for i in ngrams(tokens,3)]
            return trigram
        elif n is 4:
            quadgram = [' '.join(i) for i in ngrams(tokens,4)]
            return quadgram
        else:
            return None

    def stem(self, tk):
        stemmed_words = []
        stemmer = PorterStemmer()
        for i in tk:
            stemmed_words.append(stemmer.stem(i))
        return stemmed_words

if __name__ == "__main__":
    tp = txt_processor()
    file_content = open("The Shawshank Redemption.txt").read()
    tk = tp.tokenize(file_content)
    print(tk)