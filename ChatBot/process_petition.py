import random
from knowledge.knowledge_DAO import KnowledgeDAO
from api.gpt_api import GPTAPI
from utils import *


class ProcessPetition:
    def __init__(self):
        self.dao = KnowledgeDAO()
        self.gpt = GPTAPI()

    def show_climate_information(self, nouns):
        found = False

        for noun in nouns:
            results = self.dao.search(noun.lower())
            if results:  # Verificar si se encontraron resultados
                city_info = random.choice(results)
                for frase_template in frases:
                    try:
                        frase = frase_template.format(**city_info)
                        print("Frase elegida random: " + frase)
                        print("Frase humanizada: " + self.gpt.humanize_response(frase))
                        found = True
                        break
                    except KeyError as e:
                        # Mensaje solo de epuración
                        print(f"Missing information for key: {e}")
                        print("Available keys:", city_info.keys())
                if found:
                    break

        if not found:
            print("No climate information available for the specified location.")

    def show_cuisine_information(self, tokens):
        city_found = False
        for token in tokens:
            results = self.dao.search(token.lower())
            if results:
                city_info = random.choice(results)
                frase = random.choice(frases).format(**city_info)
                print(self.gpt.humanize_response(frase))
                city_found = True
                break
        if not city_found:
            print("Sorry, we don't have cuisine information for that location.")

    def show_language_information(self, nouns):
        language_found = False
        for noun in nouns:
            results = self.dao.search(noun.lower())
            if results:
                language_info = random.choice(results)
                frase = random.choice(frases).format(**language_info)
                print(self.gpt.humanize_response(frase))
                language_found = True
                break
        if not language_found:
            print("Sorry, I don't know the language for that location.")

    def show_culture_recommendations(nouns, adverbs, culture_type):
        if 'what' in adverbs or 'which' in adverbs:
            results = dao.search_by_culture_type(culture_type)

            if results:
                response = f"Top recommendations for {culture_type} culture: "
                random_results = random.sample(results, min(2, len(results)))  # Selecciona fins a 2 resultats aleatoris
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                print(response)
            else:
                print(f"No destinations with {culture_type} culture found in the database.")
        else:
            print(gpt.not_understood_response())


    def show_city_culture_information(nouns, adverbs):
        if 'what' in adverbs or 'which' in adverbs or 'where' in adverbs:
            city_found = False
            for noun in nouns:
                results = dao.search(noun)
                if results:
                    city_info = results[0]
                    culture_info = city_info.get('culture', "")
                    response = f"{city_info['city']}, {city_info['country']} is known for its {culture_info} culture."
                    print(gpt.humanize_response(response))
                    city_found = True
                    break

            if not city_found:
                print(gpt.city_not_in_database())
        else:
            print(gpt.not_understood_response())


    def search_tourism_type(nouns, adverbs):
        if 'what' in adverbs or 'which' in adverbs or 'where' in adverbs:
            city_found = False
            for noun in nouns:
                results = dao.search(noun)
                if results:
                    city_info = results[0]
                    tourism_types = ", ".join(city_info['tourism_type'])
                    response = f"{city_info['city']}, {city_info['country']} is known for its {tourism_types} tourism."
                    print(gpt.humanize_response(response))
                    city_found = True
                    break

            if not city_found:
                print(gpt.city_not_in_database())
        else:
            print(gpt.not_understood_response())

    def show_type_recommendations(adverbs, type):
        if 'which' or 'where' in adverbs:
            results = dao.search_by_tourism_type(type)

            if results:
                response = f"Top {type} recommendations: "
                random_results = random.sample(results, min(2, len(results)))
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                print(response)
            else:
                print(f"No {type} destinations found in the database.")
        else:
            print(gpt.not_understood_response())


    def show_transport_information(adverbs, nouns):
        if 'how' or 'what' in adverbs:
            city_found = False
            for noun in nouns:
                results = dao.search(noun)
                if results:
                    city_info = results[0]
                    transport_info = city_info.get('transport', {})
                    response_parts = [f"Transport information for {city_info['city']}, {city_info['country']}:"]

                    if 'public_transport' in transport_info:
                        response_parts.append(f"Public Transport: {transport_info['public_transport']}")
                    if 'car_rental' in transport_info:
                        response_parts.append(f"Car Rental: {transport_info['car_rental']}")
                    if 'taxi' in transport_info:
                        response_parts.append(f"Taxi: {transport_info['taxi']}")

                    response = " ".join(response_parts)
                    print(gpt.humanize_response(response))
                    city_found = True
                    break

            if not city_found:
                print(gpt.city_not_in_database())
        else:
            print(gpt.not_understood_response())


    def show_visit_question(nouns, adverbs):
        if 'why' in adverbs:
            self.show_reasons_to_visit_certain_places(nouns)
        elif 'when' in adverbs:
            self.show_best_times_to_visit(nouns)
        else:
            print(gpt.not_understood_response())

    def show_best_times_to_visit(nouns):
        response_templates = [
            "The best time to visit {city} is during {month}. {reason}"
        ]

        city_found = False
        for noun in nouns:
            results = dao.search(noun)
            if results:
                city_info = results[0]
                best_time_info = city_info['best_time_to_visit']
                response = random.choice(response_templates).format(
                    city=city_info['city'],
                    month=best_time_info['month'],
                    reason=best_time_info['reason']
                )
                print(gpt.humanize_response(response))
                city_found = True
                break
        if not city_found:
            print(gpt.city_not_in_database())

    def show_reasons_to_visit_certain_places(nouns):
        city_found = False
        for noun in nouns:
            results = dao.search(noun)
            if results:
                city_info = results[0]
                tourism_types = ", ".join(city_info['tourism_type'])
                reasons = f"The reasons to visit {city_info['city']}: "
                reasons += f"Is known for its {city_info['culture']} culture, "
                reasons += f"you will enjoy its {city_info['climate']} climate, "
                reasons += f"enjoy its delicious {city_info['cuisine']} cuisine, "
                reasons += f"and explore its tourism types like {tourism_types}. "
                reasons += f"Furthermore, the citizens here speak {city_info['language']}."

                print(gpt.humanize_response(reasons))
                city_found = True
                break

        if not city_found:
            print(gpt.city_not_in_database())

    def show_how_expensive(nouns):
        dao = KnowledgeDAO()
        city_found = False

        for noun in nouns:
            results = dao.search(noun)
            if results:
                city_info = results[0]
                cost_level = city_info['cost']
                response = f"The cost of living in {city_info['city']}, {city_info['country']} is considered {cost_level}."
                print(gpt.humanize_response(response))
                city_found = True
                break

        if not city_found:
            print(gpt.city_not_in_database())

    def show_why_expensive(nouns):
        dao = KnowledgeDAO()
        city_found = False

        for noun in nouns:
            results = dao.search(noun)
            if results:
                city_info = results[0]
                cost_level = city_info['cost']
                tourism_types = ", ".join(city_info['tourism_type'])
                response = f"The cost of living in {city_info['city']}, {city_info['country']} is considered {cost_level} because of its {city_info['culture']} culture, {city_info['climate']} climate, and tourism types like {tourism_types}."
                print(gpt.humanize_response(response))
                city_found = True
                break

        if not city_found:
            print(gpt.city_not_in_database())

    def show_cost_of_living(adverbs, nouns):
        if 'how' in adverbs:
            self.show_how_expensive(nouns)
        elif 'why' in adverbs:
            self.show_why_expensive(nouns)
        else:
            print(gpt.not_understood_response())

    def suggest_city(preferences):
        affirmative_responses = ["yes", "yeah", "sure", "of course", "absolutely", "yep"]
        negative_responses = ["no", "not really", "nope", "nah", "don't", "do not"]

        matching_cities = [city for city in cities_dataset if all(city[attr] == val for attr, val in preferences.items())]

        if not matching_cities:
            print("I'm sorry, but we couldn't find any cities that match your preferences.")
            return

        another_city_prompts = [
            "Would you like to see another city that matches your preferences?: ",
            "Are you interested in exploring another matching city?: ",
            "Do you want to check out another city like this one?: ",
            "Would you like me to suggest another city?: ",
            "Interested in seeing more cities?: "
        ]

        while matching_cities:
            selected_city = random.choice(matching_cities)
            phrase = random.choice(frases)
            phrase_filled = phrase.format(**selected_city)
            print(phrase_filled + "\n")
            matching_cities.remove(selected_city)

            if len(matching_cities) == 0:
                print("There are no more cities that match your preferences.")
                break

            user_response = input(random.choice(another_city_prompts)).lower()
            if user_response in negative_responses or not any(
                    resp for resp in affirmative_responses if resp in user_response):
                break


    def suggest(verbs_passed, nouns_passed, adjectives_passed, adverbs_passed):
        types_dict_extended = {
            "cost": ["low", "cheap", "budget", "economical", "medium", "moderate", "reasonable", "high", "expensive",
                     "premium", "luxury"],
            "climate": ["warm", "hot", "sunny", "tropical", "cold", "chilly", "freezing", "polar", "mild", "temperate",
                        "moderate", "variable", "changing", "unpredictable"],
            "culture": ["traditional", "modern", "artistic", "natural", "nordic", "contemporary", "ancient", "creative",
                        "cosmopolitan", "liberal", "innovative", "enological", "historical", "spiritual", "adventure",
                        "colonial", "festive", "indigenous", "multicultural", "cultural", "musical"],
            "cuisine": ["seafood", "eastern european", "swiss", "french", "spanish", "mexican", "norwegian", "canadian",
                        "japanese", "south african", "thai", "icelandic", "australian", "italian", "middle eastern",
                        "brazilian", "moroccan", "indian", "american", "greek", "vietnamese", "turkish", "international",
                        "dutch", "czech", "argentinian", "swedish", "danish", "chinese", "russian", "multicultural",
                        "kenyan", "hungarian", "chilean", "cuban", "malaysian", "peruvian", "austrian", "new zealand",
                        "colombian", "british", "guatemalan", "laotian", "mediterranean", "portuguese"],
            "tourism_type": ["city", "urban", "metropolitan", "beach", "coastal", "seaside", "oceanic", "nature", "natural",
                             "wildlife", "outdoors", "rural"],
            "language": ["portuguese", "polish", "german", "spanish", "norwegian", "english", "japanese", "thai",
                         "icelandic", "italian", "arabic", "hindi", "greek", "vietnamese", "turkish", "dutch", "czech",
                         "swedish", "danish", "mandarin", "russian", "hungarian", "malay", "french", "lao", "maltese"]
        }

        preferences = {}
        already_done = set()
        all_passed = set(nouns_passed + verbs_passed + adjectives_passed + adverbs_passed)

        for key in types_dict_extended.keys():
            filtered_words = [word for word in all_passed if word != "city"]  # Treiem city ja que forma part de la pregunta
            for word in filtered_words:
                understood, lemma = is_response_understood(key, all_passed, types_dict_extended)
                if understood and key not in already_done:
                    preferences[key] = lemma
                    already_done.add(key)

        lemmatizer = WordNetLemmatizer()

        questions_keys = questions.keys()  # Les diferents keys de les preguntes

        for key, question_list in questions.items():
            if key in already_done:
                continue

            while True:
                question = random.choice(question_list)
                print(question)

                # response és la resposta del usuari
                response = input("> ")

                # Processem la resposta del usuari
                words = nltk.word_tokenize(response)
                tags = nltk.pos_tag(words)

                nouns = [token for token, pos in tags if pos.startswith('N')]
                verbs = [token for token, pos in tags if pos.startswith('V')]
                adjectives = [token for token, pos in tags if pos.startswith('J')]

                verbs_lemm = [lemmatizer.lemmatize(verb, pos="v") for verb in verbs]
                nouns_lemm = [lemmatizer.lemmatize(noun, pos="n") for noun in nouns]
                adjectives_lemm = [lemmatizer.lemmatize(adjective, pos="a") for adjective in adjectives]

                understood = True  # Variable per si hem entés la resposta

                # Comprovem si hem entes la resposta i agafem el valor que coincideix
                understood, lemma = is_response_understood(key, nouns_lemm + verbs_lemm + adjectives_lemm,
                                                           types_dict_extended)

                if understood:
                    preferences[key] = lemma  # Actualitzem les preferencies en base al atribut que coincideix
                    break
                else:
                    print(random.choice(misunderstood_responses))

            while True:
                if len(preferences) >= len(questions_keys):  # SI ja tenim tots els atributs no cal preguntar més
                    return preferences

                more_question = random.choice(more_preferences_questions)
                print(more_question)  # Preguntem si té més preferencies

                # more aqui és la resposta del usuari
                more = input("> ")

                # Processem la resposta del usuari
                if more.lower() in affirmative_responses:
                    break  # Si te més preferencies
                elif more.lower() in negative_responses:
                    return preferences  # Si no te més preferencies retornem el que tenim
                else:  # No hem entes i per tant tornem a preguntar
                    print(random.choice(misunderstood_responses))

