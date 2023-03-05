import pickle
from nltk import word_tokenize
from nltk.util import ngrams

def createDicts(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    #remove newlines
    text.replace('\n', ' ')
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens if t.isalpha()]
    #create bigrams/ unigrams
    bigrams = list(ngrams(tokens, 2))
    unigrams = list(ngrams(tokens, 1))
    #create bigram/unigram dicts
    uni_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bi_dict = {b:bigrams.count(b) for b in set(bigrams)}

    return uni_dict, bi_dict, unigrams, bigrams


def main():
    #set paths to respective lang files
    english = 'data/LangId.train.English'
    french = 'data/LangId.train.French'
    italian = 'data/LangId.train.Italian'

    en_uni_dict, en_bi_dict, en_uni, en_bi = createDicts(english)
    fr_uni_dict, fr_bi_dict, fr_uni, fr_bi = createDicts(french)
    it_uni_dict, it_bi_dict, it_uni, it_bi = createDicts(italian)

    #make some pickles
    with open('english_uni_dict.pkl', 'wb') as h:
        pickle.dump(en_uni_dict, h)
    with open('english_bi_dict.pkl', 'wb') as h:
        pickle.dump(en_bi_dict, h)
    with open('french_uni_dict.pkl', 'wb') as h:
        pickle.dump(fr_uni_dict, h)
    with open('french_bi_dict.pkl', 'wb') as h:
        pickle.dump(fr_bi_dict, h)
    with open('italian_uni_dict.pkl', 'wb') as h:
        pickle.dump(it_uni_dict, h)
    with open('italian_bi_dict.pkl', 'wb') as h:
        pickle.dump(it_bi_dict, h)

    #pickle out the regular ngrams
    with open ('english_uni.pkl', 'wb') as h:
        pickle.dump(en_uni, h)
    with open ('english_bi.pkl', 'wb') as h:
        pickle.dump(en_bi, h)
    with open ('french_uni.pkl', 'wb') as h:
        pickle.dump(fr_uni, h)
    with open ('french_bi.pkl', 'wb') as h:
        pickle.dump(fr_bi, h)
    with open ('italian_uni.pkl', 'wb') as h:
        pickle.dump(it_uni, h)
    with open ('italian_bi.pkl', 'wb') as h:
        pickle.dump(it_bi, h)


if __name__ == '__main__':
    main()
