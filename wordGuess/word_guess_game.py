import sys
import pathlib
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from random import seed
from random import randint

def setfilepath(filepath):
        with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
            text = f.read()
        
        #tokenize text
        token_text = word_tokenize(text)
        token_text = [t.lower() for t in token_text if t.isalpha()]
        #lexical diversity
        unique = set(token_text)
        lex_div = len(unique) / len(token_text)
        lex_div = f"{lex_div:.2f}"
        print("The Lexical Diversity is : ", lex_div, "\n")
        

def processing(filepath):
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as file:
        raw_text = file.read()
    
    tokens = word_tokenize(raw_text)
    tokens = [t.lower() for t in tokens if t.isalpha()
    and t not in stopwords.words('english')
    and len(t) > 5]

    lemmatizer = WordNetLemmatizer()
    lemmatized = (lemmatizer.lemmatize(t) for t in tokens)
    unique_lemmas = set(lemmatized)
    #print(len(unique_lemmas))
    tags = nltk.pos_tag(unique_lemmas)
    print(tags[:20])

    nouns = [lemma for (lemma, pos) in tags if pos.startswith('N')]
    print("The number of tokens: ", len(tokens), "\n")
    print("The number of nouns in the lemmatized text: ", len(nouns), "\n")

    return nouns, tokens


def guessing_game(noun_list):
    points = 5
    seed(1234)
    rand_index = randint(0, len(noun_list))
    random_noun = noun_list[rand_index]
    #print underscores
    print("Welcome to the word guessing game!")
    for i in range(len(random_noun)):
        print('_', end=' ') #print a space after each underscore - not a newline
    #user input prompt``
    print("\n")
    print("Your task is to guess the word above, letter by letter.")
    print("You start with 5 points. For each incorrect guess you will lose a point.")
    print("You will also gain a point for each letter correctly guessed.")
    print("The game ends when you have no more points remaining, or if '!' is entered. Good luck!~")
    #keep guessing until we have the word or lose all points
    guessed = set()
    while set(random_noun) != guessed and points > 0:
        print("Please enter a letter.")
        
        #show game state
        game_state= ""
        for letter in random_noun:
            if letter in guessed:
                game_state += letter
            else:
                game_state += "_"

        guessed_letter = input("Letter: ")
        print(game_state)

        #check for exit case
        if guessed_letter == '!':
            print("Bye bye!")
            break

        #validate data entry
        if len(guessed_letter)!= 1 or not guessed_letter.isalpha():
            print("Invalid Input: Please enter in ONE LETTER.")
            continue
        if guessed_letter in random_noun:
            guessed.add(guessed_letter)
            points += 1
            print("Correct! Points: ", points)
            print(game_state)
        else:
            points -= 1
            print("Nope. Try again. Points: ", points)
            print(game_state)

        #prevent repeat guesses
        if guessed_letter in guessed:
            print("You've already tried that. Try a different letter.")
            continue

        #check if game has been won
        if set(random_noun) <= guessed:
            print("Nicely done. You've won!")
            print("Score: ", points)
            break
        elif points == 0:
            print("Too bad. You've run out of points. The word was :", random_noun)
            break

def main():
    # sysarg check
    print("Enter in filename ('anat19.txt') as sysarg to start the word guessing game. \n")
    if len(sys.argv) > 1:
        arg_input = sys.argv[1]
      #  print('Filepath: ', arg_input)
        setfilepath(arg_input)
    else:
        print('No sys.arg detected. Terminating.')
        sys.exit()

    nouns_list, tokens_list = processing(arg_input)

    # create the noun dictionary
    noun_dict = {nouns_list[i]: tokens_list[i] for i in range(len(nouns_list))}
    sorted_nouns = {k: v for k, v in sorted(noun_dict.items(), reverse = True)}
    common_nouns = [item[0] for item in Counter(sorted_nouns).most_common(50)]

    guessing_game(common_nouns)

if __name__ == "__main__":
    main()
