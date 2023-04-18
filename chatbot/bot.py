import sqlite3
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ner_model = spacy.load("en_core_web_sm")

response_templates = {
    "introduction": "Hi! I'm dustloop's chatbot helper. Ask me about Guilty Gear Strive characters and their moves! (In this prototype version, I only support Sol and Ky's movesets, with more to come in the future!)",
    "move_info": "{move_name}: {description}",
    "frame_data": "{move_name} has {startup} startup frames, {active} active frames, {recovery} recovery frames, and is {on_block} frames on block.",
    "not_found": "Sorry, I couldn't find anything on that in my knowledge base. Please, try another query."
}

class Bot:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.vectorizer, self.tfidf_matrix = self.preprocess_db()
        #this way we remember what a user has to say thru-out a convo.
        self.context = {
            "character_name": None,
            "move_name": None,
        }

    def preprocess_db(self):
        #get moves and db info
        moves = self.get_move_data()
        #concatenate move names + move descriptions
        corpus = [f"{move['name']} {move['description']}" for move in moves]
        #tf-idf matrix stuff
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        return vectorizer, tfidf_matrix
        
    def get_move_data(self):
        #query know. base
        cursor = self.connection.cursor()
        cursor.execute("SELECT moves.name, moves.description FROM moves")
        move_data = [{'name': row[0], 'description': row[1]} for row in cursor.fetchall()]
        return move_data
        
    def get_frames(self, character_name, move_name):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT characters.name, moves.name, frame_data.startup, frame_data.active, frame_data.recovery, frame_data.on_block, frame_data.on_hit
        FROM frame_data
        JOIN moves ON frame_data.move_id = moves.id
        JOIN characters ON moves.character_id = characters.id
        WHERE characters.name = ? AND moves.name = ?
        """, (character_name, move_name))
        result = cursor.fetchone()
        return result
        
    def get_move_info(self, character_name, move_name):
        cursor = self.connection.cursor()
        cursor.exectue("""
            SELECT moves.name, moves.description
            FROM moves
            JOIN characters ON moves.character_id = characters.id
            WHERE characters.name = ? AND moves.name = ?
            """, (character_name, move_name))
        result = cursor.fetchone()
        if result:
            move_info = {"name": result[0], "description": result[1]}
            return move_info
        return None
        
    def respond(self, input):
        #process user input
        tokens = word_tokenize(input)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        #NER extraction from user input
        entities = self.extract_entities(" ".join(filtered_tokens))
        self.process_entities(entities)
        
        character_name = self.context["character_name"]
        move_name = self.context["move_name"]

        if character_name and move_name:
            response = self.generate_response()
        else:
            #find best match:
            input_vector = self.vectorizer.transform([" ".join(filtered_tokens)])
            best_match = self.find_best_match(input_vector)
            response = self.generate_response(best_match_index = best_match)

        return response
        
    def generate_response(self, best_match_index = None):
        character_name = self.context["character_name"]
        move_name = self.context["move_name"]

        if character_name and move_name:
            frame_data = self.get_frames(character_name, move_name)
            move_info = self.get_move_info(character_name, move_name)
            if frame_data and move_info:
                response = response_templates["move_info"].format(
                    move_name = move_info["name"],
                    description = move_info["description"]
                ) + "\n" + response_templates["frame_data"].format(
                    character_name = frame_data[0],
                    move_name=frame_data[1],
                    startup=frame_data[2],
                    active=frame_data[3],
                    recovery=frame_data[4],
                    on_block=frame_data[5],
                )
            else:
                response = response_templates["not_found"]
        elif best_match_index is not None:
            response = self.lookup_data(best_match_index)
        elif not character_name and not move_name:
            response = response_templates["introduction"]
       # else:
        #    if best_match is not None:
         #       best_matching_move = self.get_move_data()[best_match]
          #      response = f"{best_matching_move['name']}: {best_matching_move['description']}"
           # else:
            #    response = "Please provide a character and move name for more information."

        return response

    def process_entities(self, entities):
        if "PERSON" in entities:
            self.context["character_name"] = entities["PERSON"]
        if "MOVE" in entities:
            self.context["move_name"] = entities["MOVE"]
        response = self.generate_response()
        return response
        
    def extract_entities(self, text):
        doc = ner_model(text)
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text 

        return entities
        
    def find_best_match(self, input_vector):
        cosine_similarities = cosine_similarity(input_vector, self.tfidf_matrix)
        best_match = cosine_similarities.argmax()
        return best_match
        
    def lookup_data(self, move_index):
        move = self.get_move_data()[move_index]
        response = f"{move['name']}: {move['description']}"
        return response

    def close(self):
        self.connection.close()
