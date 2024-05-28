from preprocessing.preprocessor import convert_input
from nlp.nlp_processor import NLPProcessor



def main():
    nlp = NLPProcessor()

    while not exit:
        user_input = input("¿Qué te gustaría saber sobre viajes? ")

        # Pas 1: Preprocessar
        transformed_input = convert_input(user_input)

        # Pas 2: Procesar amb NLP i comprovar si hem de sortir del bucle
        exit = nlp.process(transformed_input)


if __name__ == "__main__":
    main()
