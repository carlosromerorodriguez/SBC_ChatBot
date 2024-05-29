import nltk
from nltk.stem import WordNetLemmatizer
from api.gpt_api import GPTAPI
from process_petition import *

# Descargar los recursos de nltk necesarios
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

#TODO:
# - Si la pregunta té dos adjectius o més dels que contemplem s'ha de processar diferent que si només en té un
#   o conté dos camps o més per els quals classifiquem les ciutats
# - Guardar el context de la ciutat per a les preguntes que ho requereixin
# - Canviar dataset perque només hi tingui els tipus de cultura que contemplem
# - API
# - Bucle de preguntes i suggeriments

class NLPProcessor:
    city_context = None

    def __init__(self):
        self.gpt_api = GPTAPI()
        self.process_petition = ProcessPetition()

    def process(self, user_question):
        words, tags, nouns, verbs, adverbs, adjectives = self.tokenize_and_lemmatize(user_question)

        self.handle_general_questions(nouns, verbs, adjectives, adverbs, words, tags)
        return False

    def tokenize_and_lemmatize(self, user_question):
        words = nltk.word_tokenize(user_question.lower())
        tags = nltk.pos_tag(words)

        nouns = [token for token, pos in tags if pos.startswith('N')]
        verbs = [token for token, pos in tags if pos.startswith('V')]
        adverbs = [token for token, pos in tags if pos.startswith('W')]
        adjectives = [token for token, pos in tags if pos.startswith('J')]

        verbs_lemme = [WordNetLemmatizer().lemmatize(verb, pos="v") for verb in verbs]
        nouns_lemme = [WordNetLemmatizer().lemmatize(noun, pos="n") for noun in nouns]
        adjectives_lemme = [WordNetLemmatizer().lemmatize(adjective, pos="a") for adjective in adjectives]
        adverbs_lemme = [WordNetLemmatizer().lemmatize(adverb, pos="r") for adverb in adverbs]

        return words, tags, nouns_lemme, verbs_lemme, adverbs_lemme, adjectives_lemme

    def handle_general_questions(self, nouns, verbs, adjectives, adverbs, words, tags):
        if self.handle_specific_nouns(nouns, adjectives, verbs, adverbs, words):
            return
        if self.handle_adjectives(adjectives, nouns, adverbs):
            return
        if self.handle_adverbs(adverbs, nouns, verbs, adjectives, words, tags):
            return
        print(self.gpt_api.not_understood_response())

    def handle_specific_nouns(self, nouns, adjectives, verbs, adverbs, words):
        if 'weather' in nouns:
            print("Weather")
            self.process_petition.show_climate_information(nouns)
        elif any(term in nouns for term in ['eat', 'cuisine', 'food']):
            self.process_petition.show_cuisine_information(nouns + adjectives)
        elif any(term in verbs for term in ['see', 'visit']) or 'attractions' in nouns:
            self.process_petition.show_tourist_attractions(nouns)
        elif 'language' in nouns:
            self.process_petition.show_language_information(nouns)
        elif 'currency' in nouns:
            self.process_petition.show_currency_information(nouns)
        elif 'restaurant' in nouns:
            self.process_petition.show_restaurant_information(nouns)
        elif any(term in nouns for term in ['hotel', 'stay', 'sleep']):
            self.process_petition.show_hotel_information(nouns)
        elif any(term in nouns for term in ['travel', 'flight', 'plane']) or 'get there' in ' '.join(words):
            self.process_petition.show_flight_information(adverbs, nouns)
        elif 'transport' in nouns or 'get around' in ' '.join(words):
            self.process_petition.show_transport_information(adverbs, nouns)
        elif 'culture' in nouns:
            self.process_petition.show_city_culture_information(nouns)
        elif 'tourism' in nouns:
            self.process_petition.search_tourism_type(nouns)
        elif any(term in nouns for term in ['beach', 'city', 'mountain']):
            # Extreure el tipus de lloc
            place_type = None
            for noun in nouns:
                if noun in ['beach', 'city', 'mountain']:
                    place_type = noun
                    break

            self.process_petition.show_type_recommendations(place_type)
        else:
            return False
        return True

    def handle_adjectives(self, adjectives, nouns, adverbs):
        if any(term in adjectives for term in
               ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']):

            # Extreure el tipus de cultura
            culture_type = None
            for adj in adjectives:
                if adj in ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']:
                    culture_type = adj
                    break

            self.process_petition.show_culture_recommendations(nouns, adverbs, culture_type)
        elif 'expensive' in adjectives:
            self.process_petition.show_cost_of_living(adverbs)
        else:
            return False
        return True

    def handle_adverbs(self, adverbs, nouns, verbs, adjectives, words, tags):
        if 'what' in adverbs or 'which' in adverbs:
            self.handle_what_which_questions(nouns, verbs, adjectives)
        elif 'where' in adverbs:
            self.handle_where_questions(words, tags)
        elif 'when' in adverbs:
            self.handle_when_questions(words, nouns)
        elif 'why' in adverbs:
            self.handle_why_questions(words, nouns)
        elif 'how' in adverbs:
            self.handle_how_questions(words, tags, adjectives)
        else:
            return False
        return True

    def handle_what_which_questions(self, nouns, verbs, adjectives):
        if 'climate' in nouns:
            print("Climate")
            self.process_petition.show_climate_information(nouns)
        elif any(term in nouns for term in ['eat', 'cuisine', 'food', 'restaurant', 'drink', 'beverage', 'dish', 'meal']):
            self.process_petition.show_cuisine_information(nouns + adjectives)
        elif any(term in verbs for term in ['see', 'visit']) or 'attractions' in nouns:
            self.process_petition.show_tourist_attractions(nouns)
        elif 'language' in nouns:
            self.process_petition.show_language_information(nouns)
        elif 'currency' in nouns:
            self.process_petition.show_currency_information(nouns)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_where_questions(self, words, tags):
        if "cultural" in words:
            self.process_petition.show_cultural_recommendations()
        elif "food" in words or "cuisine" in words:
            self.process_petition.show_food_recommendations()
        elif "beach" in words:
            self.process_petition.show_beach_recommendations()
        elif "historical" in words:
            city_name = self.extract_city_name(tags)
            self.process_petition.show_historical_recommendations(city_name)
        else:
            print("Can you specify what kind of places or experiences you're interested in?")

    def handle_when_questions(self, words, nouns):
        if 'visit' in words or 'go' in words:
            self.process_petition.show_best_times_to_visit(nouns)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_why_questions(self, words, nouns):
        if 'visit' in words or 'go' in words:
            self.process_petition.show_reasons_to_visit_certain_places(nouns)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_how_questions(self, words, tags, adjectives):
        print(self.gpt_api.not_understood_response())

    def extract_city_name(self, tags):
        city_name = None
        for i, (token, tag) in enumerate(tags):
            if token == 'in' and i + 1 < len(tags):
                city_name = tags[i + 1][0]
                break
        return city_name
