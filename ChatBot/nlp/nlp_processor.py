import spacy
from spacy import displacy
import nltk
from nltk.stem import WordNetLemmatizer
from api.gpt_api import GPTAPI
from process_petition import *



#TODO:
# - Si la pregunta té dos adjectius o més dels que contemplem s'ha de processar diferent que si només en té un
#   o conté dos camps o més per els quals classifiquem les ciutats
# - Guardar el context de la ciutat per a les preguntes que ho requereixin
# - Canviar dataset perque només hi tingui els tipus de cultura que contemplem
# - API
# - Bucle de preguntes i suggeriments

# what is the weather like in Barcelona and when is the best time to visit
#                          after gpt api:
# what is the weather like in Barcelona ; when is the best time to visit

class NLPProcessor:
    city_context = None

    def __init__(self):
        self.gpt_api = GPTAPI()
        self.process_petition = ProcessPetition()
        self.lemmatizer = WordNetLemmatizer()

    def process(self, user_question, city_context):
        self.city_context = city_context

        words, tags, nouns, verbs, adverbs, adjectives, user_question = self.tokenize_and_lemmatize(user_question)

        self.handle_general_questions(nouns, verbs, adjectives, adverbs, words, tags, user_question)
        return False

    def tokenize_and_lemmatize(self, user_question):
        words = nltk.word_tokenize(user_question)
        tags = nltk.pos_tag(words)

        nouns = [token for token, pos in tags if pos.startswith('N')]
        verbs = [token for token, pos in tags if pos.startswith('V')]
        adverbs = [token for token, pos in tags if pos.startswith('W')]
        adjectives = [token for token, pos in tags if pos.startswith('J')]

        # Lemmatize
        verbs_lemm = [self.lemmatizer.lemmatize(verb, pos="v") for verb in verbs]
        nouns_lemm = [self.lemmatizer.lemmatize(noun, pos="n") for noun in nouns]
        adjectives_lemm = [self.lemmatizer.lemmatize(adjective, pos="a") for adjective in adjectives]
        adverbs_lemm = [self.lemmatizer.lemmatize(adverb, pos="r") for adverb in adverbs]

        return words, tags, nouns_lemm, verbs_lemm, adverbs_lemm, adjectives_lemm, user_question

    def handle_general_questions(self, nouns, verbs, adjectives, adverbs, words, tags, user_question):
        print(user_question)
        if self.handle_specific_nouns(nouns, adjectives, verbs, adverbs, words, user_question):
            return
        if self.handle_specific_verbs(verbs, adverbs, user_question):
            return
        if self.handle_adjectives(adjectives, nouns, adverbs, user_question, verbs):
            return
        if self.handle_adverbs(adverbs, nouns, verbs, adjectives, words, tags, user_question):
            return
        print(self.gpt_api.not_understood_response())

    def handle_specific_nouns(self, nouns, adjectives, verbs, adverbs, words, user_question):
        print(nouns)
        if 'weather' in nouns:
            self.process_petition.show_climate_information(user_question, self.city_context)
        elif any(term in nouns for term in ['cuisine', 'food']) or 'eat' in verbs or 'drink' in verbs:
            self.process_petition.show_cuisine_information(user_question, self.city_context, verbs, adverbs, adjectives)
        elif 'attractions' in nouns or 'activities' in nouns:
            self.process_petition.show_tourist_attractions(user_question, adjectives, adverbs, self.city_context, verbs)
        elif 'language' in nouns:
            self.process_petition.show_language_information(user_question, self.city_context)
        elif 'currency' in nouns:
            self.process_petition.show_currency_information(nouns, user_question, self.city_context)
        elif 'restaurant' in nouns:
            self.process_petition.show_restaurant_information(user_question, self.city_context, adjectives)
        elif any(term in nouns for term in ['hotel', 'stay', 'sleep']):
            self.process_petition.show_hotel_information(self.city_context)
        elif any(term in nouns for term in ['travel', 'flight', 'plane']) or 'get there' in ' '.join(words):
            self.process_petition.show_flight_information(adverbs, nouns, user_question, self.city_context)
        elif 'transport' in nouns or 'get around' in ' '.join(words):
            self.process_petition.show_transport_information(adverbs, user_question, self.city_context)
        elif 'culture' in nouns:
            self.process_petition.show_city_culture_information(nouns, adverbs, user_question, self.city_context, verbs)
        elif 'tourism' in nouns:
            self.process_petition.search_tourism_type(user_question, self.city_context, verbs)
        elif any(term in nouns for term in ['beach', 'city', 'mountain']):
            # Extreure el tipus de lloc
            place_type = None
            for noun in nouns:
                if noun in ['beach', 'city', 'mountain']:
                    place_type = noun
                    break

            self.process_petition.show_type_recommendations(adverbs, place_type, user_question, verbs)
        else:
            return False
        return True

    def handle_adjectives(self, adjectives, nouns, adverbs, user_question, verbs):
        if any(term in adjectives for term in
               ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']):

            # Extreure el tipus de cultura
            culture_type = None
            for adj in adjectives:
                if adj in ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']:
                    culture_type = adj
                    break

            self.process_petition.show_culture_recommendations(adverbs, culture_type, user_question, verbs)
        elif any(term in adjectives for term in
           ['mild', 'cold', 'warm']):

            # Extreure el tipus de cultura
            weather_type = None
            for weather in adjectives:
                if weather in ['mild', 'cold', 'warm']:
                    weather_type = weather
                    break

            self.process_petition.show_weather_recommendations(nouns, adverbs, weather_type, user_question, verbs)
        elif any(term in adjectives for term in ['low', 'high', 'moderate']):

            range_type = None
            for price in adjectives:
                if price in ['low', 'high', 'moderate']:
                    range_type = price
                    break

            self.process_petition.cost_adjective(adverbs, user_question, verbs, range_type)
        elif 'expensive' in adjectives:
            self.process_petition.show_cost_of_living(adverbs, user_question, self.city_context)
        else:
            return False
        return True

    def handle_specific_verbs(self, verbs, adverbs, user_question):
        if 'pay' in verbs:
            if 'how' in adverbs:
                self.process_petition.show_currency_information(adverbs, user_question, self.city_context)
            else:
                print(self.gpt_api.not_understood_response())
        else:
            return False
        return True

    def handle_adverbs(self, adverbs, nouns, verbs, adjectives, words, tags, user_question):
        if 'what' in adverbs or 'which' in adverbs:
            self.handle_what_which_questions(nouns, verbs, user_question, adverbs, adjectives)
        elif 'where' in adverbs:
            self.handle_where_questions(words, tags, user_question)
        elif 'when' in adverbs:
            self.handle_when_questions(words, user_question)
        elif 'why' in adverbs:
            self.handle_why_questions(words, user_question)
        else:
            return False
        return True

    def handle_what_which_questions(self, nouns, verbs, user_question, adverbs, adjectives):
        if 'climate' in nouns:
            self.process_petition.show_climate_information(user_question, self.city_context)
        elif any(term in nouns for term in ['eat', 'cuisine', 'food', 'restaurant', 'drink', 'beverage', 'dish', 'meal']):
            self.process_petition.show_cuisine_information(user_question, self.city_context, verbs, adverbs, adjectives)
        elif 'language' in nouns:
            self.process_petition.show_language_information(nouns, user_question, self.city_context)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_where_questions(self, words, tags, user_question):
        if "food" in words or "cuisine" in words:
            self.process_petition.show_food_recommendations(user_question, self.city_context)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_when_questions(self, words, user_question):
        if 'visit' in words or 'go' in words:
            self.process_petition.show_best_times_to_visit(user_question, self.city_context)
        else:
            print(self.gpt_api.not_understood_response())

    def handle_why_questions(self, words, user_question):
        if 'visit' in words or 'go' in words:
            self.process_petition.show_reasons_to_visit_certain_places(user_question, self.city_context)
        else:
            print(self.gpt_api.not_understood_response())


