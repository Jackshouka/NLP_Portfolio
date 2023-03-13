import requests
import os
import nltk
import string
import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from nltk.tokenize import sent_tokenize

def nab_links():
    url = 'https://www.dustloop.com/w/GGACR'
    #first we'll get links just within the dustloop url and focus on something else later.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dl_links = soup.find_all('a')
    #purpose is to have knowledge base on characters: thus we make a list of chars for scraper to use
    characters = ['A.B.A', 'Anji', 'Axl', 'Baiken', 'Bridget', 'Chipp', 'Dizzy', 
                  'Eddie', 'Faust', 'I-No', 'Jam', 'Johnny', 'Justice', 'Kliff', 
                  'Ky', 'May', 'Millia', 'Order-Sol','Potemkin', 'Robo-Ky', 'Slayer', 
                  'Sol', 'Testament', 'Venom', 'Zappa']
    characters_links = []
    outside_links = []
    
    for link in dl_links:
        #outside dustloop site
        href = link.get('href') #below is the condition to filter out character specfic pages.

        if href.startswith('https://'):
            outside_links.append(href)

        #character pages (within /w/GGACR)
        if '/w/GGACR/' not in href:
            continue
        #check if link ends w/ char name, which would direct to a char page
        for character in characters:
            if href.endswith(character):
                characters_links.append(href)

    scrape(characters_links, 'scraped_characters')
    scrape(outside_links, 'scraped_external')

    clean('scraped_characters', 'clean_characters')
    clean('scraped_external', 'clean_external')

    preprocess('clean_characters', 'char_processed')
    preprocess('clean_external', 'ext_processed')

    print("TF for Chararacter Directory: ")
    tf_calc('char_processed')
    char_scores = tf_calc('char_processed')

    print("TF for External Directory: ")
    tf_calc('ext_processed')
    ext_scores = tf_calc('ext_processed')

    #pickle both ext and char tf scores for knowledge base
    with open("char_know.pickle", 'wb') as f:
        pickle.dump(char_scores, f)
    with open("ext_know.pickle", 'wb') as f:
        pickle.dump(ext_scores, f)
    

def scrape(links, folder):
    for link in links:
        full_link = urljoin('https://www.dustloop.com', link)  #mash url skeleton with ending bit(characters in ggac+r)
        response = requests.get(full_link)
        if response.status_code == 200:  # check if the request was successful - had a lot of trouble with this earlier.
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            filename = os.path.join(folder, link.replace('/', '_')+ '.txt')
            with open(filename, 'w', encoding = 'utf-8') as f:
                f.write(text)
        else:
            print(f"Error {response.status_code} while scraping {full_link}")

def clean(scraped_folder, dest_folder):
    nltk.download('punkt')
    for filename in os.listdir(scraped_folder):
         with open(os.path.join(scraped_folder, filename), 'r', encoding ='utf-8') as f:
                text = f.read()
                text = text.replace('\t', ' ').replace('\n', ' ')
                sentences = sent_tokenize(text)
                clean_text = ' '.join(sentences)
                with open(os.path.join(dest_folder, filename), 'w', encoding ='utf-8') as out:
                    out.write(clean_text)

def preprocess(orig_folder, final_folder):
    #create a second preprocessing folder to make tf-idf calcs later.
    for filename in os.listdir(orig_folder):
        with open(os.path.join(orig_folder, filename), 'r', encoding='utf-8') as f:
            stop_words = set(stopwords.words('english'))
            text = f.read()
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            #get rid of stopwords, punctuation and make all lowercase
            processed = []
            words = word_tokenize(text)
            for word in words:
                if word not in stop_words:
                    processed.append(word)           
            processed_text = ' '.join(processed)
            with open(os.path.join(final_folder, filename), 'w', encoding = 'utf-8') as out:
                out.write(processed_text)
        
def tf_calc(corpus):
    tf_scores = {}
    for file in os.listdir(corpus):
        with open(os.path.join(corpus, file), 'r', encoding='utf-8') as f:
            text = f.read()
            tokens = word_tokenize(text)
            tokens = [t for t in tokens if t not in stopwords.words('english')]
            # Calculate term frequency
            tf_dict = {}
            for token in tokens:
                if token in tf_dict:
                    tf_dict[token] += 1
                else:
                    tf_dict[token] = 1
            for token in tf_dict:
                tf_dict[token] = tf_dict[token] / len(tokens)
            # Add term frequencies to overall dictionary
            for token, score in tf_dict.items():
                if token in tf_scores:
                    tf_scores[token] += score
                else:
                    tf_scores[token] = score
    sorted_tf = sorted(tf_scores.items(), key=lambda x: x[1], reverse=True)
    for token, score in sorted_tf[:25]:
        print(f"{token}: {score}")
    return tf_scores    

def main():
    nab_links()

if __name__ == "__main__":
    main()
