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

    def __init__(self, preprocessor, _process_petition):
        self.gpt_api = GPTAPI()
        self.process_petition = _process_petition
        self.lemmatizer = WordNetLemmatizer()
        self.preprocessor = preprocessor


    async def process(self, user_question, city_context, context , chat_id):
        self.city_context = city_context

        words, tags, nouns, verbs, adverbs, adjectives, user_question = self.tokenize_and_lemmatize(user_question)

        await self.handle_general_questions(nouns, verbs, adjectives, adverbs, words, tags, user_question, context, chat_id)
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

    async def handle_general_questions(self, nouns, verbs, adjectives, adverbs, words, tags, user_question, context, chat_id):
        print(user_question)
        if await self.handle_specific_nouns(nouns, adjectives, verbs, adverbs, words, user_question, context, chat_id):
            return
        if await self.handle_specific_verbs(verbs, adverbs, user_question, context, chat_id):
            return
        if await self.handle_adjectives(adjectives, nouns, adverbs, user_question, verbs, context, chat_id):
            return
        if await self.handle_adverbs(adverbs, nouns, verbs, adjectives, words, tags, user_question, context, chat_id):
            return
        print(self.gpt_api.not_understood_response())

    async def handle_specific_nouns(self, nouns, adjectives, verbs, adverbs, words, user_question, context, chat_id):
        print(nouns)
        if 'weather' in nouns:
            await self.process_petition.show_climate_information(user_question, self.city_context, context, chat_id)
        elif any(term in nouns for term in ['cuisine', 'food', 'eat']) or 'eat' in verbs  or 'drink' in verbs:
            await self.process_petition.show_cuisine_information(user_question, self.city_context, verbs, adverbs, adjectives, context, chat_id)
        elif 'attraction' in nouns or 'activity' in nouns:
            await self.process_petition.show_tourist_attractions(user_question, adjectives, adverbs, self.city_context, verbs, context, chat_id)
        elif 'language' in nouns:
            await self.process_petition.show_language_information(user_question, self.city_context, nouns, context, chat_id)
        elif 'currency' in nouns:
            await self.process_petition.show_currency_information(nouns, user_question, self.city_context, context, chat_id)
        elif 'restaurant' in nouns:
            await self.process_petition.show_restaurant_information(user_question, self.city_context, adjectives, context, chat_id)
        elif any(term in nouns for term in ['hotel']) or any(term in verbs for term in ['stay', 'sleep']):
            await self.process_petition.show_hotel_information(self.city_context, context, chat_id)
        elif any(term in nouns for term in ['flight', 'plane']) or any(term in verbs for term in ['travel']) or 'get there' in ' '.join(words) or 'get to' in ' '.join(words):
            await self.process_petition.show_flight_information(adverbs, nouns, user_question, self.city_context, context, chat_id)
        elif 'transport' in nouns or 'get around' in ' '.join(words):
            await self.process_petition.show_transport_information(adverbs, user_question, self.city_context, verbs, context, chat_id)
        elif 'culture' in nouns:
            await self.process_petition.show_city_culture_information(adverbs, user_question, self.city_context, verbs, context, chat_id)
        elif 'tourism' in nouns:
            await self.process_petition.search_tourism_type(adverbs, user_question, self.city_context, verbs, context, chat_id)
        elif 'cost' in nouns:
            await self.process_petition.show_cost_of_living(adverbs, user_question, self.city_context, context, chat_id)
        elif any(term in nouns for term in ['beach', 'city', 'mountain']):
            # Extreure el tipus de lloc
            place_type = None
            for noun in nouns:
                if noun in ['beach', 'city', 'mountain']:
                    place_type = noun
                    break

            await self.process_petition.show_type_recommendations(adverbs, place_type, user_question, verbs, context, chat_id)
        else:
            return False
        return True

    async def handle_adjectives(self, adjectives, nouns, adverbs, user_question, verbs, context, chat_id):
        if any(term in adjectives for term in
               ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']):

            # Extreure el tipus de cultura
            culture_type = None
            for adj in adjectives:
                if adj in ['historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive']:
                    culture_type = adj
                    break

            await self.process_petition.show_culture_recommendations(adverbs, culture_type, user_question, verbs, context, chat_id)
        elif any(term in adjectives for term in
           ['mild', 'cold', 'warm']):

            # Extreure el tipus de cultura
            weather_type = None
            for weather in adjectives:
                if weather in ['mild', 'cold', 'warm']:
                    weather_type = weather
                    break

            await self.process_petition.show_weather_recommendations(nouns, adverbs, weather_type, user_question, verbs, context, chat_id)
        elif any(term in adjectives for term in ['expensive', 'moderate', 'cheap']):

            if 'cities' or 'place' or 'city' or 'destinations' in nouns:
                range_type = None
                for price in adjectives:
                    if price in ['expensive', 'moderate', 'cheap']:
                        range_type = price
                        break

                await self.process_petition.cost_adjective(adverbs, user_question, verbs, range_type, context, chat_id)
        elif 'expensive' in adjectives:
            await self.process_petition.show_cost_of_living(adverbs, user_question, self.city_context, context, chat_id)
        elif 'similar' in adjectives:
            await self.process_petition.show_similar_cities(user_question, self.city_context, context, chat_id)
        else:
            return False
        return True

    async def handle_specific_verbs(self, verbs, adverbs, user_question, context, chat_id):
        if 'pay' in verbs:
            if 'how' in adverbs:
                await self.process_petition.show_currency_information(adverbs, user_question, self.city_context, context, chat_id)
            else:
                print(self.gpt_api.not_understood_response())
        else:
            return False
        return True

    async def handle_adverbs(self, adverbs, nouns, verbs, adjectives, words, tags, user_question, context, chat_id):
        if 'what' in adverbs or 'which' in adverbs:
            await self.handle_what_which_questions(nouns, verbs, user_question, adverbs, adjectives, context, chat_id)
        elif 'where' in adverbs:
            await self.handle_where_questions(words, tags, user_question, context, chat_id)
        elif 'when' in adverbs:
            await self.handle_when_questions(words, user_question, context, chat_id)
        elif 'why' in adverbs:
            await self.handle_why_questions(words, user_question, context, chat_id)
        else:
            return False
        return True

    async def handle_what_which_questions(self, nouns, verbs, user_question, adverbs, adjectives, context, chat_id):
        if 'climate' in nouns:
            await self.process_petition.show_climate_information(user_question, self.city_context, context, chat_id)
        elif any(term in nouns for term in ['eat', 'cuisine', 'food', 'restaurant', 'drink', 'beverage', 'dish', 'meal']):
            await self.process_petition.show_cuisine_information(user_question, self.city_context, verbs, adverbs, adjectives, context, chat_id)
        elif 'language' in nouns:
            await self.process_petition.show_language_information(user_question, self.city_context, nouns, context, chat_id)
        else:
            print(self.gpt_api.not_understood_response())

    async def handle_where_questions(self, words, tags, user_question, context, chat_id):
        if "food" in words or "cuisine" in words:
            await self.process_petition.show_food_recommendations(user_question, self.city_context, context, chat_id)
        else:
            print(self.gpt_api.not_understood_response())

    async def handle_when_questions(self, words, user_question, context, chat_id):
        if 'visit' in words or 'go' in words:
            await self.process_petition.show_best_times_to_visit(user_question, self.city_context, context, chat_id)
        else:
            print(self.gpt_api.not_understood_response())

    async def handle_why_questions(self, words, user_question, context, chat_id):
        if 'visit' in words or 'go' in words:
            await self.process_petition.show_reasons_to_visit_certain_places(user_question, self.city_context, context, chat_id)
        else:
            print(self.gpt_api.not_understood_response())


