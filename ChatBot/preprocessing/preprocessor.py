from api.gpt_api import GPTAPI
import re

# Context Nouns
contemplated_nouns = [
    'cuisine', 'attractions', 'language', 'food', 'beach', 'city', 'cost', 'culture', 'transport',
    'reasons', 'time', 'tourism', 'weather', 'country', 'rating', 'currency', 'activities', 'public_transport', 'car_rental', 'taxi', 'mountain',  'other', 'mountain',
    'hotel', 'flight', 'plane', 'restaurant', 'stay', 'sleep', 'restaurants', 'other', 'hotels', 'flights', 'planes', 'around', 'destination', 'destinations', 'from'
]

# Context adjectives
contemplated_adjectives = [
    'expensive', 'historical', 'best', 'cheap', 'moderate', 'warm', 'cold', 'mild',
    'variable', 'free', 'historical', 'modern', 'artistic', 'traditional', 'cosmopolitan', 'festive', "similar"
]

# Context verbs
contemplated_verbs = [
    'show', 'suggest', 'visit', 'go', 'get around', 'eat', 'see', 'travel', 'get', 'there', 'pay', 'recommend', 'speak',
    'living', 'live', 'staying', 'sleeping', 'sleep', 'stay', 'find', 'discover', 'explore', 'experience'
]

# Context adverbs
contemplated_adverbs = [
    'what', 'where', 'when', 'why', 'which', 'how'
]

class Preprocessor:
    city_context = None

    def __init__(self):
        self.gpt = GPTAPI()

    def change_city_context_value(self, new_city_context):
        # print("Changing city context to: " + new_city_context)
        self.city_context = new_city_context
        # print("City context is now: " + self.city_context)

    def convert_first_word_to_lowercase(self, input_string):
        words = input_string.split()
        if words:
            words[0] = words[0].lower()
        return ' '.join(words)

    # Funció per trobar paraules que no estan a la llista completa i no són paraules a ignorar
    def find_non_matching_words(self, input_text, word_list, ignore_list, cities):
        word_list = [word.lower() for word in word_list]
        ignore_list = [word.lower() for word in ignore_list]
        cities = [city.lower() for city in cities]

        # Dividim el text d'entrada en paraules i convertir a minúscules
        input_words = re.findall(r'\b\w+\b', input_text.lower())

        # Afegim les paraules que no estan en les llistes a non_matching_words
        non_matching_words = [
            word for word in input_words
            if word not in word_list
            if word not in ignore_list
            if word not in cities
        ]

        # Si self.city_context no és None afegim la comparació
        if self.city_context is not None:
            non_matching_words = [
                word for word in non_matching_words
                if word.lower() != self.city_context.lower()
            ]

        return non_matching_words


    def correct_cities_in_sentence(self, user_input):
        city_dict, flag = self.gpt.get_cities(user_input)

        if flag:
            print(self.gpt.humanize_response("Petition to API failed, something might go wrong. Please try again.", user_input, self))
            return user_input, {}

        if not city_dict:
            return user_input, {}

        for original, corrected in city_dict.items():
            user_input = user_input.replace(original, corrected)
        return user_input, list(city_dict.values())

    def transform_input_with_fallback_to_gpt(self, user_input):
        complete_list = contemplated_adverbs + contemplated_verbs + contemplated_adjectives + contemplated_nouns

        ignore_list = ["the", "is", "a", "an", "and", "or", "but", "if", "in", "on", "with", "for", "to", "of", "at", "by",
                       "can", "I", "from", "you", "me", "this", "summer", "do", "they", "i", "my", "your", "our", "his"]

        # Si la petició e
        user_input, cities = self.correct_cities_in_sentence(user_input)

        # Si no te ciutats es que s'esta fent alusió a una ciutat o s'esta preguntant per a recomanació de ciutats o ciutat
        if not cities:
            # Mirem si la pregunta es sobre una ciutat o esta preguntat per a que li recomanem una ciutat o ciutats
            if not self.gpt.is_asking_for_cities(user_input):
                if self.city_context: # Si ja tenim una ciutat de contexte
                    user_input = self.gpt.replace_city_context(user_input, self.city_context)
                else:
                    print(self.gpt.humanize_response("I'm sorry, I didn't understand the city you are asking for. Please try again.", user_input, self))
                    return user_input, True, None

        elif cities and not self.city_context:
            self.city_context = cities[-1]

        elif cities and self.city_context:
            self.city_context = cities[-1]

        non_matching_words = self.find_non_matching_words(user_input, complete_list, ignore_list, cities)

        # Passem totes les paraules a minúscules
        non_matching_words = [word.lower() for word in non_matching_words]

        for city in cities:
            city_words = city.lower().split()
            for word in city_words:
                if word.lower() in non_matching_words:
                    non_matching_words.remove(word)

        if self.city_context:
            context_city_words = self.city_context.lower().split()
            for word in context_city_words:
                if word.lower() in non_matching_words:
                    non_matching_words.remove(word)

        if not non_matching_words:
            return self.convert_first_word_to_lowercase(user_input), False, self.city_context

        return self.convert_first_word_to_lowercase(self.gpt.transform_input(user_input, contemplated_adverbs, contemplated_verbs, contemplated_nouns,
                                   contemplated_adjectives, non_matching_words)), False, self.city_context
