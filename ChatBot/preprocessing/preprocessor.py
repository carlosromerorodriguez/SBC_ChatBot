from api.gpt_api import GPTAPI
import re

# Context Nouns
contemplated_nouns = [
    'cuisine', 'attractions', 'language', 'food', 'beach', 'city', 'cost', 'culture', 'transport',
    'places', 'experiences', 'reasons', 'time', 'tourism', 'weather', 'country', 'rating', 'destination', 'tour',
    'currency', 'activities', 'public_transport', 'car_rental', 'taxi', 'mountain', 'historical'
]

# Context adjectives
contemplated_adjectives = [
    'expensive', 'cultural', 'historical', 'best', 'cheap', 'moderate', 'modern', 'traditional', 'warm', 'cold', 'mild',
    'variable', 'free'
]

# Context verbs
contemplated_verbs = [
    'show', 'suggest', 'visit', 'go', 'get around', 'eat', 'see'
]


# Context adverbs
contemplated_adverbs = [
    'what', 'where', 'when', 'why', 'which', 'how'
]


def transform_input_with_fallback_to_gpt(user_input):
    gpt = GPTAPI()

    complete_list = contemplated_adverbs + contemplated_verbs + contemplated_adjectives + contemplated_nouns

    ignore_list = ["the", "is", "a", "an", "and", "or", "but", "if", "in", "on", "with", "for", "to", "of", "at", "by"]
    cities = ['Barcelona', 'Madrid', 'Paris', 'Lisbon', 'London', 'Berlin', 'Rome', 'Prague', 'Amsterdam', 'Vienna',
              'Budapest', 'Athens', 'Dublin', 'Edinburgh', 'Stockholm', 'Copenhagen', 'Oslo', 'Helsinki', 'Reykjavik',
              'Moscow', 'St. Petersburg', 'Istanbul', 'Dubai', 'Cairo', 'Marrakech', 'Cape Town', 'Nairobi', 'Mumbai',
              'Bangkok', 'Tokyo', 'Beijing', 'Shanghai', 'Seoul', 'Sydney', 'Auckland', 'New York', 'Los Angeles',
              'Chicago', 'Miami', 'Toronto', 'Mexico City', 'Rio de Janeiro', 'Buenos Aires', 'Santiago', 'Lima',
              'Bogota', 'Sao Paulo', 'Lima', 'Quito', 'Caracas', 'San Jose', 'Panama City', 'Havana', 'Kingston',
              'San Juan', 'Santo Domingo', 'Port-au-Prince', 'Belize City', 'Guatemala City', 'Tegucigalpa',
              'San Francisco', 'Seattle', 'Vancouver', 'Calgary', 'Montreal', 'Quebec City', 'Halifax', 'St. John\'s',
              'Anchorage', 'Honolulu', 'Tijuana', 'Monterrey', 'Guadalajara', 'Puebla', 'Merida', 'Oaxaca', 'Acapulco',
              'Cancun', 'Tulum', 'Puerto Vallarta']

    # Normalitza les ciutats a minúscules
    normalized_cities = [city.title() for city in cities]

    # Funció per trobar paraules que no estan a la llista completa i no són paraules a ignorar
    def find_non_matching_words(input_text, word_list, ignore_list, cities):
        input_words = re.findall(r'\b\w+\b', input_text)
        non_matching_words = [word for word in input_words if
                              word not in word_list and word not in ignore_list and word not in cities]
        return non_matching_words

    non_matching_words = find_non_matching_words(user_input, complete_list, ignore_list, normalized_cities)


    # Si la llista de paraules que no coincideixen és buida, no cridem a l'API
    if not non_matching_words:
        return user_input  # La frase és vàlida, no cal reformular

    return gpt.transform_input(user_input, contemplated_adverbs, contemplated_verbs, contemplated_nouns,
                               contemplated_adjectives, non_matching_words)
