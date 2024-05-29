import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer, SnowballStemmer
import process_petition
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import random
lemmatizer = WordNetLemmatizer()
from api.gpt_api import GPTAPI

class NLPProcessor:
    city_context = None

    def process(self, user_question):
        words = nltk.word_tokenize(user_question.lower())
        tags = nltk.pos_tag(words)

        nouns = [token for token, pos in tags if pos.startswith('N')]
        verbs = [token for token, pos in tags if pos.startswith('V')]
        adverbs = [token for token, pos in tags if pos.startswith('W')]
        adjectives = [token for token, pos in tags if pos.startswith('J')]

        #Lemmatize
        verbs_lemm = [lemmatizer.lemmatize(verb, pos="v") for verb in verbs]
        nouns_lemm = [lemmatizer.lemmatize(noun, pos="n") for noun in nouns]
        adjectives_lemm = [lemmatizer.lemmatize(adjective, pos="a") for adjective in adjectives]
        adverbs_lemm = [lemmatizer.lemmatize(adverb, pos="r") for adverb in adverbs]

        #TODO:
        # - Si la pregunta té dos adjectius o més dels que contemplem s'ha de processar diferent que si només en té un
        #   o conté dos camps o més per els quals classifiquem les ciutats
        # - Guardar el context de la ciutat per a les preguntes que ho requereixin
        # - Canviar dataset perque només hi tingui els tipus de cultura que contemplem
        # - API
        # - Bucle de preguntes i suggeriments


        if 'weather' in nouns:
            show_climate_information(nouns)
        elif 'eat' or 'cuisine' or 'food' in nouns:
            show_cuisine_information(nouns + adjectives)
        elif 'see' in verbs_lemm or 'visit' in verbs_lemm or 'attractions' in nouns:
            show_tourist_attractions(nouns)
        elif 'language' in nouns:
            show_language_information(nouns)
        elif 'currency' in nouns:
            show_currency_information(nouns)

        elif 'restaurant' in nouns:
            show_restaurant_information(nouns) # TODO: API
        elif 'hotel' or 'stay' or 'sleep' in nouns:
            show_hotel_information(nouns) # TODO: API
        elif 'travel' in nouns or 'flight' in nouns or 'plane' in nouns or 'get there' in ' '.join(words): # TODO: API
            show_flight_information(adverbs, nouns)

        elif 'transport' in nouns or 'get around' in ' '.join(words) in words: # DONE
            show_transport_information(adverbs, nouns)


        elif 'historical' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "historical")
        elif 'modern' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "modern")
        elif 'artistic' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "artistic")
        elif 'traditional' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "traditional")
        elif 'cosmopolitan' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "cosmopolitan")
        elif 'festive' in adjectives: # DONE
            show_culture_recommendations(nouns, adverbs, "festive")

        elif 'culture' in nouns: # DONE
            show_city_culture_information(nouns, adverbs)
        elif 'tourism' in nouns: # DONE
            search_tourism_type(nouns, adverbs)

        elif 'beach' in nouns: # DONE
            show_type_recommendations(adverbs, "beach")
        elif 'mountain' in nouns: # DONE
            show_type_recommendations(adverbs, "mountain")
        elif 'city' in nouns: # DONE
            show_type_recommendation(adverbs, "city")

        elif 'visit' in verbs_lemm or 'go' in verbs_lemm: # DONE
            show_visit_question(nouns, adverbs)
        elif 'expensive' in adjectives: # DONE
            show_cost_of_living(adverbs, nouns)

        # ...



        if 'what' in adverbs:
            if 'climate' in nouns:
                show_climate_information(nouns)
            elif 'eat' in verbs_lemm or 'cuisine' in nouns:
                show_cuisine_information(nouns + adjectives)
            elif 'see' in verbs_lemm or 'visit' in verbs_lemm or 'attractions' in nouns: #TODO WITH API
                # show_tourist_attractions(nouns)   Atracciones turísticas recomendadas
            elif 'language' in nouns:
                show_language_information(nouns)
            else:
                print(GPTAPI.not_understood_response())

        elif 'where' in adverbs:
            # Ens guardem el primer atribut
            # Bucle de preguntes i suggriment
            if "cultural" in words:
                show_cultural_recommendations()
            elif "food" in words or "cuisine" in words:
                show_food_recommendations()
            elif "beach" in words:
                show_beach_recommendations()
            elif "historical" in words:
                city_name = None
                for i, (token, tag) in enumerate(tags):
                    if token == 'in' and i+1 < len(tags):
                        city_name = tags[i+1][0]
                        break

                show_historical_recommendations(city_name)
            else:
                print("Can you specify what kind of places or experiences you're interested in?")

        elif 'when' in adverbs: # En base al climate
            if 'visit' in words or 'go' in words:
                show_best_times_to_visit(nouns)  # Los mejores momentos para visitar ciudades basadas en clima
            else:
                print(GPTAPI.not_understood_response())

        elif 'why' in adverbs:
            if 'visit' in words or 'go' in words:
                show_reasons_to_visit_certain_places(nouns)  # Razones para visitar lugares específicos
            else:
                print(GPTAPI.not_understood_response())

        elif 'which' in adverbs or 'suggest' in verbs:
            # Bucle de preguntes i suggriment
            suggest_city(suggest(verbs_lemm, nouns_lemm, adjectives_lemm, adverbs_lemm))

        elif 'how' in adverbs:
            if 'expensive' in adjectives:
                show_cost_of_living(tags)
            elif 'get around' in ' '.join(words) or 'transport' in words: #TODO
                # show_transport_options(nouns)
                print("Transport")
            else:
                print(GPTAPI.not_understood_response())
        else:
            print(GPTAPI.not_understood_response())
