from api.gpt_api import GPTAPI
from api.travel_api import TravelAPI
from nlp.nlp_processor import NLPProcessor
from knowledge.knowledge_DAO import KnowledgeDAO
from formatting.response_formatter import ResponseFormatter


def main():
    user_input = input("¿Qué te gustaría saber sobre viajes? ")

    # Paso 1: Transformar el input del usuario
    gpt = GPTAPI()
    transformed_input = gpt.transform_input(user_input)

    # Paso 2: Procesar con NLP
    nlp = NLPProcessor()
    intent, entities = nlp.process(transformed_input)

    # Paso 3: Buscar en la base de conocimiento
    knowledge_dao = KnowledgeDAO()
    knowledge_result = knowledge_dao.search(intent, entities)

    if knowledge_result:
        response = knowledge_result
    else:
        # Paso 4: Llamada a la API de Booking.com
        travel_api = TravelAPI()
        api_result = travel_api.get_info(intent, entities)
        response = api_result

    # Paso 5: Construir y reformar la respuesta
    formatted_response = ResponseFormatter.format(response)
    final_response = gpt.reform_response(formatted_response)

    print(final_response)


if __name__ == "__main__":
    main()
