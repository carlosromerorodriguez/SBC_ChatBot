from preprocessing.preprocessor import convert_input
# from nlp_processor import NLPProcessor
from api.gpt_api import GPTAPI

def main():
    # nlp = NLPProcessor()
    gpt = GPTAPI()
    print(gpt.start_response())

    exitFlag = False
    while True:
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
        transformed_input = convert_input(user_input)

        # Pas 2: Procesar amb NLP i comprovar si hem de sortir del bucle
        # exitFlag = nlp.process(transformed_input)


if __name__ == "__main__":
    main()
