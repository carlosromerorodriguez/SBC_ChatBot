from api.travel_api import TravelAPI
from nlp.nlp_processor import *
from preprocessing.preprocessor import Preprocessor
from api.gpt_api import GPTAPI

# TODO: Passar user input a humanize per aconseguir una resposta més natural

test_questions = [
    "What is the weather like in Barcelona?",
    "What kind of food can I eat in Paris?",
    "What are the best attractions to visit in Rome?",
    "What language do they speak in Tokyo?",
    "What currency is used in London?",
    "Can you recommend a restaurant in New York?",
    "Where can I stay in Dubai?",
    "How can I get to Sydney?",
    "How do I get around in Amsterdam?",
    "What is the culture like in Istanbul?",
    "What kind of tourism is popular in Berlin?",
    "Is there a beach in Miami?",
    "What are the modern attractions in Los Angeles?",
    "How expensive is living in San Francisco?",
    "Which cuisine is famous in Bangkok?",
    "Where can I find the best beaches in Thailand?",
    "When is the best time to visit Vienna?",
    "Why should I visit Prague?",
    "How do I get around in Hong Kong?"
]

def main():
    gpt = GPTAPI()
    nlp = NLPProcessor()
    prp = Preprocessor()

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

        # Dividir las preguntas si hay múltiples
        separated_questions = gpt.split_questions(user_input)
        print(separated_questions)

        if separated_questions:
            questions = separated_questions.split(' ; ')
        else:
            questions = [user_input]

        for question in questions:
            # Pas 1: Preprocessar
            transformed_input, flagCont, city_context = prp.transform_input_with_fallback_to_gpt(question)

            if flagCont:
                continue

            # Pas 2: Procesar amb NLP i comprovar si hem de sortir del bucle
            exitFlag = nlp.process(transformed_input, city_context)

            if exitFlag:
                exit(0)

    """for user_input in test_questions:
        transformed_input, flagCont, city_context = prp.transform_input_with_fallback_to_gpt(user_input)

        # Pas 2: Procesar amb NLP i comprovar si hem de sortir del bucle
        exitFlag = nlp.process(transformed_input, city_context)

        if exitFlag:
            exit(0)
    """

if __name__ == "__main__":
    main()
