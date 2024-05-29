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


def convert_first_word_to_lowercase(input_string):
    words = input_string.split()
    if words:
        words[0] = words[0].lower()
    return ' '.join(words)

# Funció per trobar paraules que no estan a la llista completa i no són paraules a ignorar
def find_non_matching_words(input_text, word_list, ignore_list, cities):
    word_list = [word.lower() for word in word_list]
    ignore_list = [word.lower() for word in ignore_list]
    cities = [city.lower() for city in cities]

    # Dividir el text d'entrada en paraules i convertir a minúscules
    input_words = re.findall(r'\b\w+\b', input_text.lower())

    # Afegir les paraules que no estan en les llistes a non_matching_words
    non_matching_words = [word for word in input_words if
                          word not in word_list and word not in ignore_list and word not in cities]

    return non_matching_words


def correct_cities_in_sentence(user_input, gpt):
    city_dict = gpt.get_cities(user_input)
    if not city_dict:
        return user_input, {}

    for original, corrected in city_dict.items():
        user_input = user_input.replace(original, corrected)
    return user_input, city_dict.values()

def transform_input_with_fallback_to_gpt(user_input):
    gpt = GPTAPI()

    complete_list = contemplated_adverbs + contemplated_verbs + contemplated_adjectives + contemplated_nouns

    ignore_list = ["the", "is", "a", "an", "and", "or", "but", "if", "in", "on", "with", "for", "to", "of", "at", "by"]

    user_input, cities = correct_cities_in_sentence(user_input, gpt)
    print(f"Cities: {cities}")

    non_matching_words = find_non_matching_words(user_input, complete_list, ignore_list, cities)

    if not non_matching_words:
        return convert_first_word_to_lowercase(user_input)

    return convert_first_word_to_lowercase(gpt.transform_input(user_input, contemplated_adverbs, contemplated_verbs, contemplated_nouns,
                               contemplated_adjectives, non_matching_words))
