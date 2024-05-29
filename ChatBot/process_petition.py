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
