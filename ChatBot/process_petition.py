from api.travel_api import TravelAPI
from knowledge.knowledge_DAO import KnowledgeDAO
from formatting.response_formatter import ResponseFormatter



def show_climate_information(nouns):
    found = False
    for city_info in cities_dataset:
        if found:
            break
        for noun in nouns:
            if city_info['city'].lower() == noun.lower():
                frase = random.choice(frases).format(**city_info)
                print(frase)
                found = True
                break
    if not found:
        print("No climate information available for the specified location.")


def show_cuisine_information(tokens):
    city_found = False
    for city_info in cities_dataset:
        if any(city_info['city'].lower() == token.lower() for token in tokens):
            frase = random.choice(frases).format(**city_info)
            print(frase)
            city_found = True
            break

    if not city_found:
        print("Sorry, we don't have cuisine information for that location.")

def show_language_information(nouns):
    for city_info in cities_dataset:
        if city_info['city'].lower() in nouns:
            print(f"In {city_info['city'].title()} they speak {city_info['language'].title()}")
            break

"""# **'When' types of questions**"""

def get_best_times_to_visit_by_climate(climate):
    climate_to_times = {
        "warm": "late spring to early summer (May to July)",
        "cold": "summer (June to August)",
        "mild": "spring (April to June) and fall (September to November)",
        "hot": "early spring (April to June)",
        "variable": "spring and fall are generally good options"
    }
    return climate_to_times.get(climate, "varies, as detailed information is not available")

def show_best_times_to_visit(nouns):
    city_query = ' '.join(nouns)

    response_templates = [
        "Heading to {city}? The ideal period for your trip is {times}, when the weather is just perfect for exploring.",
        "If {city} is on your list, consider visiting during {times}. You’ll find the climate quite agreeable.",
        "The {climate} climate of {city} makes {times} the best time to visit. Enjoy your trip!",
        "Looking to explore {city}? {times} offers the best weather conditions for your adventures.",
        "For a pleasant journey to {city}, aim for {times}. That’s when the climate is most favorable."
    ]

    city_found = False
    for city_info in cities_dataset:
        if any(noun.lower() == city_info["city"].lower() for noun in nouns):
            best_times = get_best_times_to_visit_by_climate(city_info["climate"])
            response = random.choice(response_templates).format(city=city_info['city'], times=best_times, climate=city_info['climate'])
            print(response)
            city_found = True
            break
    if not city_found:
        print("Sorry, we don't have information on the best time to visit that location.")

"""# **'Why' types of questions**"""

def show_reasons_to_visit_certain_places(nouns):
    city_found = False
    for city_info in cities_dataset:
        if any(noun.lower() == city_info['city'].lower() for noun in nouns):
            reasons = f"The reasons to visit {city_info['city']}: "
            reasons += f"Is known for its {city_info['culture']} culture, "
            reasons += f"you will enjoy its {city_info['climate']} climate, "
            reasons += f"enjoy its delicious {city_info['cuisine']} cuisine, "
            reasons += f"and explore its {city_info['tourism_type']} tourism. "
            reasons += f"Furthermore, the citizens here speak {city_info['language']}."

            print(reasons)
            city_found = True
            break

    if not city_found:
        print("There is no relevant information about the city you mention.")

"""# **'How' type of questions**"""

def reassemble_city_names(tags):
    city_names = []
    temp_name = []

    allowed_tags = ['NNP', 'NNPS', 'NN', 'NNS', 'IN', 'JJ', 'VBN']
    for token, tag in tags:
        if tag in allowed_tags:
            temp_name.append(token)
        else:
            if temp_name:
                city_names.append(" ".join(temp_name))
                temp_name = []
    if temp_name:
        city_names.append(" ".join(temp_name))

    return city_names


def show_cost_of_living(tags):
    city_or_country_names = reassemble_city_names(tags)
    adjectives = [token.lower() for token, tag in tags if tag == 'JJ']

    info_found = False
    city = False
    for info  in cities_dataset:
        for name in city_or_country_names:
            if info['city'].lower() == name.lower() or info['country'].lower() == name.lower():
                if info['city'].lower() == name.lower(): city = True
                if "expensive" in adjectives:
                    cost_level = info['cost']
                    if city: print(f"The cost of living in {name.title()}, {info['country'].title()} is considered {cost_level}.")
                    else: print(f"The cost of living in {name.title()} is considered {cost_level}.")
                    info_found = True
                    break
        if info_found:
            break

    if not info_found:
        print("Sorry, we don't have cost information for that location.")

"""# **'Where' type of questions**"""

def show_cultural_recommendations():
    rich_cultural_descriptors = [
        "traditional", "artistic", "ancient", "creative",
        "cosmopolitan", "historical", "spiritual", "colonial",
        "festive", "indigenous", "multicultural", "cultural", "musical"
    ]

    recommended_cities = [city['city'] for city in cities_dataset if any(descriptor in city['culture'].lower() for descriptor in rich_cultural_descriptors)]

    if recommended_cities:
        recommended_city = random.choice(recommended_cities)
        print(f"For rich cultural experiences, consider visiting {recommended_city}.")
    else:
        print("Sorry, we couldn't find a city recommendation for rich cultural experiences.")

def show_food_recommendations():
    # Filtrar ciudades por su oferta gastronómica
    recommended_cities = [city for city in cities_dataset if city['cuisine'] in types_dict['cuisine']]

    if recommended_cities:
        city_info = random.choice(recommended_cities)
        frase = random.choice(frases).format(**city_info)
        print(frase)
    else:
        print("Sorry, we couldn't find a city recommendation for culinary experiences.")

def show_beach_recommendations():
    # Filtrar ciudades que ofrecen turismo de playa
    beach_cities = [city for city in cities_dataset if city['tourism_type'] == 'beach']

    if beach_cities:
        city_info = random.choice(beach_cities)
        frase = random.choice(frases).format(**city_info)
        print(frase)
    else:
        print("Sorry, we couldn't find a city recommendation for beach experiences.")

def show_historical_recommendations(city=None):
    historical_cities = [city for city in cities_dataset if 'historical' in city['culture'] or 'ancient' in city['culture']]
    if city:
        historical_cities = [c for c in historical_cities if c['city'].lower() == city.lower()]

    if historical_cities:
        city_info = random.choice(historical_cities)
        frase = random.choice(frases).format(**city_info)
        print(frase)
    else:
        print(f"Sorry, we couldn't find historical tour recommendations for {city}." if city else "Sorry, we couldn't find any city recommendation for historical experiences.")

"""# **Suggestion based on user's preferences**"""

def map_synonym_to_basic_value(word, key, types_dict_extended):
    synonym_to_value_map = {
        "cost": {
            "low": ["low", "cheap", "budget", "economical"],
            "medium": ["medium", "moderate", "reasonable"],
            "high": ["high", "expensive", "premium", "luxury"]
        },
        "climate": {
            "warm": ["warm", "hot", "sunny", "tropical"],
            "cold": ["cold", "chilly", "freezing", "polar"],
            "mild": ["mild", "temperate", "moderate"],
            "variable": ["variable", "changing", "unpredictable"]
        },
        "tourism_type": {
            "city": ["city", "urban", "metropolitan"],
            "beach": ["beach", "coastal", "seaside", "oceanic"],
            "nature": ["nature", "natural", "wildlife", "outdoors", "rural"]
        }
    }

    if key in synonym_to_value_map:
        for basic_value, synonyms in synonym_to_value_map[key].items():
            if word in synonyms:
                return basic_value
    else:
      if word in types_dict_extended[key]:
            return word
    return None

def suggest(verbs_passed, nouns_passed, adjectives_passed, adverbs_passed):
    