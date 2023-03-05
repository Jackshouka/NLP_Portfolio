import pickle
from nltk import word_tokenize
from nltk.util import ngrams

def compute_prob(text, uni, bi, N, V):
    #N=training data token, V=unique token
    uni_test = word_tokenize(text)
    bi_test = list(ngrams(uni_test, 2))
    #using laplace smoothing
    p_laplace = 1
    
    for bigram in bi_test:
        n = bi[bigram] if bigram in bi else 0
        d = uni[bigram[0]] if bigram in uni else 0

        p_laplace = p_laplace * ((n + 1) / (d + V))

    print("Probability (via laplace smoothing) is: ", p_laplace, "% \n")

def main():
    #load in pickles
    with open('english_uni_dict.pkl', 'rb') as h:
        en_pikl_uni_dict = pickle.load(h)
    with open('english_bi_dict.pkl', 'rb') as h:
        en_pikl_bi_dict = pickle.load(h)
    with open('french_uni_dict.pkl', 'rb') as h:
        fr_pikl_uni_dict = pickle.load(h)
    with open('french_bi_dict.pkl', 'rb') as h:
        fr_pikl_bi_dict = pickle.load(h)
    with open('italian_uni_dict.pkl', 'rb') as h:
        it_pikl_uni_dict = pickle.load(h)
    with open('italian_bi_dict.pkl', 'rb') as h:
        it_pikl_bi_dict = pickle.load(h)

    with open('english_uni.pkl', 'rb') as h:
        en_pikl_uni = pickle.load(h)
    with open('english_bi.pkl', 'rb') as h:
        en_pikl_bi = pickle.load(h)
    with open('french_uni.pkl', 'rb') as h:
        fr_pikl_uni = pickle.load(h)
    with open('french_bi.pkl', 'rb') as h:
        fr_pikl_bi = pickle.load(h)
    with open('italian_uni.pkl', 'rb') as h:
        it_pikl_uni = pickle.load(h)
    with open('italian_bi.pkl', 'rb') as h:
        it_pikl_bi = pickle.load(h)

    N_eng = len(en_pikl_uni)
    N_fr = len(fr_pikl_uni)
    N_it = len(it_pikl_uni)
    V_eng = len(en_pikl_uni_dict)
    V_fr = len(fr_pikl_uni_dict)
    V_it = len(fr_pikl_uni_dict)
    
    test_text = 'data/LangId.test'
    #loop line by line to get probability

    with open(test_text, 'r') as file:
        for line in file:
            prob_en = compute_prob(test_text, en_pikl_uni, en_pikl_bi, N_eng, V_eng)
            prob_fr = compute_prob(test_text, fr_pikl_uni, fr_pikl_bi, N_fr, V_fr)
            prob_it = compute_prob(test_text, it_pikl_uni, it_pikl_bi, N_it, V_it)
            #select highest prob and write to file.
            most_probable = max(prob_en, prob_fr, prob_it)
            with open('results.txt', 'w') as f:
                if most_probable == prob_en:
                    f.write("English")
                elif most_probable == prob_fr:
                    f.write("French")
                elif most_probable == prob_it:
                    f.write("Italian")

    #compare with .sol doc
    predict = 'results.txt'
    solution = 'LangId.sol'
    correct = 0
    incorrect = 0
    incorrect_lines = []

    with open(predict, 'r') as f1, open(solution, 'r') as f2:
        for line_pred, line_sol in zip(f1, f2):
            if line_pred.strip() != line_sol.strip():
                incorrect += 1
                incorrect_lines.append(incorrect)
            else:
                correct += 1
    
    #final results.
    acc = correct / (correct + incorrect)
    print("Accuracy: ", acc, "\n")
    print("Line numbers where incorrect: ", incorrect_lines)

if __name__ == '__main__':
    main()