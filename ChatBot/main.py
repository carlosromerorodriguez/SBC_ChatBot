from nlp.nlp_processor import *
from preprocessing.preprocessor import transform_input_with_fallback_to_gpt
from api.gpt_api import GPTAPI

# TODO: Passar user input a humanize per aconseguir una resposta més natural

def main():
    gpt = GPTAPI()
    nlp = NLPProcessor()

    #print(gpt.start_response())

    exitFlag = False
    while not exitFlag:
        user_input = input("> ")

        if gpt.is_greeting_input(user_input):
            print(gpt.salutation_response())
            continue
        elif gpt.is_goodbye_input(user_input):
            print(gpt.goodbye_response())
            break
        elif gpt.is_asking_for_me(user_input):
            print(gpt.start_response())
            continue

        # Pas 1: Preprocessar
        transformed_input = transform_input_with_fallback_to_gpt(user_input)

        # Pas 2: Procesar amb NLP i comprovar si hem de sortir del bucle
        exitFlag = nlp.process(transformed_input)


if __name__ == "__main__":
    main()
