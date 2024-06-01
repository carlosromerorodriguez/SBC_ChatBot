import random
from knowledge.knowledge_DAO import KnowledgeDAO
from api.gpt_api import GPTAPI
from utils import *
from api.travel_api import TravelAPI
from session_manager import session_manager


class ProcessPetition:
    def __init__(self, prp, send_message, send_message_and_wait_for_response):
        self.dao = KnowledgeDAO()
        self.gpt = GPTAPI()
        self.travel_api = TravelAPI("6eb7659adbmshe5fc3c22f1bddbbp19d5eajsnf7dd83dc13fc")
        self.prp = prp
        self.send_message = send_message
        self.send_message_and_wait_for_response = send_message_and_wait_for_response

    async def show_climate_information(self, user_question, city_context, context, chat_id):
        found = False

        results = self.dao.search(city_context)
        if results:  # Verificar si se encontraron resultados
            city_info = random.choice(results)
            for frase_template in frases:
                try:
                    frase = frase_template.format(**city_info)
                    await self.send_message(context, chat_id,
                                            self.gpt.humanize_response(frase, user_question, self.prp))
                    found = True
                    break
                except KeyError as e:
                    # Mensaje solo de epuración
                    print(f"Missing information for key: {e}")
                    print("Available keys:", city_info.keys())

        if not found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_cuisine_information(self, user_question, city_context, verbs, adverbs, adjectives, context, chat_id):
        if 'suggest' in verbs or 'recommend' in verbs or 'where' in adverbs:
            await self.show_restaurant_information(user_question, city_context, adjectives, context, chat_id)
        else:
            city_found = False
            results = self.dao.search(city_context)

            if results:
                city_info = random.choice(results)

                # Check if 'typical_food' exists in the city_info
                if 'typical_food' in city_info:
                    typical_food = ", ".join(city_info['typical_food'])
                    response = f"The typical food in {city_info['city']} includes: {typical_food}."
                else:
                    response = f"No typical food information available for {city_info['city']}."

                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_language_information(self, user_question, city_context, nouns, context, chat_id):
        language_found = False

        if 'other' in nouns:
            city_found = False
            results = self.dao.search(city_context)
            if results:
                city_info = random.choice(results)
                language_info = city_info.get('other_languages_spoken', "")
                response = f"{city_info['city']}, {city_info['country']} is known for its {city_info['language']} language, and also speaks {language_info}."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())
        else:

            results = self.dao.search(city_context)
            if results:
                language_info = random.choice(results)
                frase = random.choice(frases).format(**language_info)
                await self.send_message(context, chat_id, self.gpt.humanize_response(frase, user_question, self.prp))
                language_found = True

            if not language_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_culture_recommendations(self, adverbs, culture_type, user_question, verbs, context, chat_id):
        if 'what' in adverbs or 'which' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            results = self.dao.search_by_culture_type(culture_type)

            if results:
                response = f"Top recommendations for {culture_type} culture: "
                random_results = random.sample(results, min(2, len(results)))  # Selecciona fins a 2 resultats aleatoris
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            else:
                response = f"No destinations with {culture_type} culture found in the database."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_city_culture_information(self, adverbs, user_question, city_context, verbs, context, chat_id):
        if 'what' in adverbs or 'which' in adverbs or 'where' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            city_found = False

            results = self.dao.search(city_context)
            if results:
                city_info = results[0]
                culture_info = city_info.get('culture', "")
                response = f"{city_info['city']}, {city_info['country']} is known for its {culture_info} culture."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def search_tourism_type(self, adverbs, user_question, city_context, verbs, context, chat_id):
        if 'what' in adverbs or 'which' in adverbs or 'where' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            city_found = False

            results = self.dao.search(city_context)
            if results:
                city_info = results[0]
                tourism_types = ", ".join(city_info['tourism_type'])
                response = f"{city_info['city']}, {city_info['country']} is known for its {tourism_types} tourism."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_type_recommendations(self, adverbs, type, user_question, verbs, context, chat_id):
        if 'which' or 'where' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            results = self.dao.search_by_tourism_type(type)

            if results:
                response = f"Top {type} recommendations: "
                random_results = random.sample(results, min(2, len(results)))
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            else:
                print(f"No {type} destinations found in the database.")
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_transport_information(self, adverbs, user_question, city_context, verbs, context, chat_id):
        if 'how' or 'what' in adverbs or 'explain' in verbs:
            city_found = False

            results = self.dao.search(city_context)
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
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_best_times_to_visit(self, user_question, city_context, context, chat_id):
        response = [
            "The best time to visit {city} is during {month}. {reason}"
        ]

        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            best_time_info = city_info['best_time_to_visit']
            response = random.choice(response).format(
                city=city_info['city'],
                month=best_time_info['month'],
                reason=best_time_info['reason']
            )
            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_reasons_to_visit_certain_places(self, user_question, city_context, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            tourism_types = ", ".join(city_info['tourism_type'])
            reasons = f"The reasons to visit {city_info['city']}: "
            reasons += f"Is known for its {city_info['culture']} culture, "
            reasons += f"you will enjoy its {city_info['climate']} climate, "
            reasons += f"enjoy its delicious {city_info['typical_food']} cuisine, "
            reasons += f"and explore its tourism types like {tourism_types}. "
            reasons += f"Furthermore, the citizens here speak {city_info['language']}."

            await self.send_message(context, chat_id, self.gpt.humanize_response(reasons, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_how_expensive(self, user_question, city_context, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            cost_level = city_info['cost']
            response = f"The cost of living in {city_info['city']}, {city_info['country']} is considered {cost_level}. Because of its {city_info['culture']} culture, {city_info['climate']} climate, and tourism types like {', '.join(city_info['tourism_type'])}."
            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_why_expensive(self, user_question, city_context, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            cost_level = city_info['cost']
            tourism_types = ", ".join(city_info['tourism_type'])
            response = f"The cost of living in {city_info['city']}, {city_info['country']} is considered {cost_level} because of its {city_info['culture']} culture, {city_info['climate']} climate, and tourism types like {tourism_types}."
            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_cost_of_living(self, adverbs, user_question, city_context, context, chat_id):
        if 'how' or 'what' or 'which' in adverbs:
            await self.show_how_expensive(user_question, city_context, context, chat_id)
        elif 'why' in adverbs:
            await self.show_why_expensive(user_question, city_context, context, chat_id)
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_tourist_attractions(self, user_question, adjectives, adverbs, city_context, verbs, context, chat_id):
        if 'what' in adverbs or 'which' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            city_found = False

            results = self.dao.search(city_context)
            if results:
                city_info = results[0]
                activities = city_info.get('activities', {})

                # Filtra les activitats segons els adjectius
                if 'free' in adjectives:
                    selected_activities = activities.get('free', [])
                elif 'moderate' in adjectives:
                    selected_activities = activities.get('moderate', [])
                elif 'expensive' in adjectives:
                    selected_activities = activities.get('expensive', [])
                else:
                    # Si no hi ha adjectius específics, mostra totes les activitats
                    selected_activities = activities.get('free', []) + activities.get('moderate', []) + activities.get(
                        'expensive', [])

                if selected_activities:
                    attraction_names = [activity['name'] for activity in selected_activities]
                    response = f"The top attractions in {city_info['city']} are: {', '.join(attraction_names)}"
                else:
                    response = f"There are no specific attractions found for {city_info['city']}."

                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
                city_found = True

            if not city_found:
                await self.send_message(context, chat_id, self.gpt.city_not_in_database())
        elif 'where' in adverbs:
            await self.search_tourism_type(adverbs, user_question, city_context, verbs)
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def cost_adjective(self, adverbs, user_question, verbs, range_type, context, chat_id):
        await self.show_price_recommendations(adverbs, user_question, verbs, range_type, context, chat_id)

    async def show_price_recommendations(self, adverbs, user_question, verbs, range_type, context, chat_id):
        if 'which' or 'where' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            results = self.dao.search_by_price_range(range_type)

            if results:
                response = f"Top {range_type} recommendations: "
                random_results = random.sample(results, min(2, len(results)))
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            else:
                print(f"No {range_type} destinations found in the database.")
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_destinations(self, user_question, city_context, context, chat_id, adjectives):
        # Busquem a la base de dades destinacions amb els adjectius especificats
        results = self.dao.search_by_adjectives(adjectives)

        await self.send_message(context, chat_id, self.gpt.humanize_response("Searching for destinations...", user_question, self.prp))

        if results:
            await self.send_message(context, chat_id, self.gpt.humanize_response("I found some destinations for you:" + ", ".join([city['city'] for city in results]), user_question, self.prp))
        else:
            await self.send_message(context, chat_id, self.gpt.humanize_response("No destinations found with the specified adjectives.", user_question, self.prp))

    async def show_currency_information(self, nouns, user_question, city_context, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            currency_info = city_info.get('currency', 'Currency information not available')
            response = f"The currency used in {city_info['city']}, {city_info['country']} is {currency_info}. That can be represented as"
            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_restaurant_information(self, user_question, city_context, adjectives, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            restaurant_info = city_info.get('restaurants', {})
            selected_restaurants = []

            if 'cheap' in adjectives:
                selected_restaurants = restaurant_info.get('cheap', [])
            elif 'moderate' in adjectives:
                selected_restaurants = restaurant_info.get('moderate', [])
            elif 'expensive' in adjectives:
                selected_restaurants = restaurant_info.get('expensive', [])
            else:
                selected_restaurants = (restaurant_info.get('cheap', []) +
                                        restaurant_info.get('moderate', []) +
                                        restaurant_info.get('expensive', []))

            if selected_restaurants:
                response = f"The recommended restaurants in {city_info['city']} are:"
                for restaurant in selected_restaurants:
                    response += f"\n- {restaurant['name']} ({restaurant['cuisine']}) - {restaurant['price_range']}"
            else:
                response = f"No restaurant information available for {city_info['city']}."

            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    async def show_hotel_information(self, city_context, context, chat_id):
        string = f"In {city_context}, there are various hotels you can stay at. Can you fill in the check-in and check-out dates? So I can help you find the best hotel for your stay."
        await self.send_message(context, chat_id, self.gpt.humanize_response(string, city_context, self.prp))

        await self.send_message(context, chat_id, "Enter the check-in date (YYYY-MM-DD): ")
        session_manager.set_session(chat_id, 'asking_for_hotel_check_in', True)

    async def save_hotel_check_in_date(self, context, chat_id, check_in_date):
        session_manager.clear_session(chat_id, 'asking_for_hotel_check_in')
        session_manager.set_session(chat_id, 'hotel_check_in', check_in_date)
        await self.send_message(context, chat_id, "Enter the check-out date (YYYY-MM-DD): ")
        session_manager.set_session(chat_id, 'asking_for_hotel_check_out', True)


    async def hotel_api_request(self, city_context, chat_id, context, check_out_date):
        session_manager.clear_session(chat_id, 'asking_for_hotel_check_out')

        check_in_date = session_manager.get_session(chat_id, 'hotel_check_in')

        self.send_message(context, chat_id, "⏳ Searching for hotels... ⏳")

        destination_response = self.travel_api.search_destination(query=city_context)
        if not destination_response or not destination_response.get('data'):
            msg = f"I couldn't find the destination for the city due to an API error: {city_context}"
            await self.send_message(context, chat_id, self.gpt.humanize_response(msg, city_context, self.prp))
            return

        dest_id = destination_response['data'][0]['dest_id']

        hotels_response = self.travel_api.search_hotels(dest_id=dest_id, checkin_date=check_in_date,
                                                        checkout_date=check_out_date)
        if not hotels_response or not hotels_response.get('data') or not hotels_response['data'].get('hotels'):
            msg = f"I couldn't find any hotels for the destination due to an API error: {city_context}"
            await self.send_message(context, chat_id, self.gpt.humanize_response(msg, city_context, self.prp))
            return

        hotel_id = hotels_response['data']['hotels'][0]['hotel_id']
        hotel_details = self.travel_api.get_hotel_details(hotel_id, check_in_date, check_out_date)

        if hotel_details:
            hotel_data = hotel_details['data']
            response = f"I found a hotel for you in {city_context}. Here are the details:"
            response += f"Name: {hotel_data['hotel_name']}"
            response += f"URL: {hotel_data['url']}"
            response += f"Address: {hotel_data['address']}, {hotel_data['city']}, {hotel_data['country_trans']}"
            response += f"Check-in: {hotel_data['arrival_date']}"
            response += f"Check-out: {hotel_data['departure_date']}"
            response += f"Price: {hotel_data['product_price_breakdown']['gross_amount_hotel_currency']['amount_rounded']}"
            response += f"Review Score: {hotel_data.get('wifi_review_score', {}).get('rating', 'N/A')} (based on {hotel_data['review_nr']} reviews)"

            await self.send_message(context, chat_id, self.gpt.humanize_response(response, city_context, self.prp))
        else:
            print("No se pudo obtener los detalles del hotel.")


    async def show_flight_information(self, adverbs, nouns, user_question, city_context, context, chat_id):
        string = "I can help you find the best flight for your trip. Can you provide me with the departure date?"
        await self.send_message(context, chat_id, self.gpt.humanize_response(string, user_question, self.prp))

        # Extraiem les ciutats de la preguntas
        cities_in_question, flag = self.gpt.get_cities(user_question)

        if flag:
            await self.send_message(context, chat_id,
                                    self.gpt.humanize_response("I am sorry, petition to API failed. Please try again.",
                                                               user_question, self.prp))
            return

        unique_cities = set(cities_in_question.values())

        # Verifiquem que hi hagi ciutats en la pregunta
        if unique_cities:
            if len(unique_cities) == 1:
                # Si només hi ha una ciutat, i la ciutat de contexte no està present
                if self.prp.city_context and city_context not in unique_cities:
                    unique_cities.add(city_context)
                else:
                    await self.send_message(context, chat_id, self.gpt.humanize_response(
                        "I need you to specify both origin and destination cities, could you reformulate the sentence?",
                        user_question, self.prp))
                    return
        else:
            # Si no hi ha ciutats en la pregunta
            if not city_context:
                await self.send_message(context, chat_id, self.gpt.humanize_response(
                    "I need you to specify both origin and destination cities, could you reformulate the sentence?",
                    user_question, self.prp))
                return

            # Agregem la ciutat de contexte a la llista de ciutats
            unique_cities.add(city_context)

        await self.send_message(context, chat_id, "Enter the departure date (YYYY-MM-DD): ")

        self.send_message(context, chat_id, "⏳ Searching for flights... ⏳")

        # Activar FLAG y guardar cities_in_question
        session_manager.set_session(chat_id, 'cities_in_question', list(unique_cities))

    async def flight_api_request(self, city_context, chat_id, context, user_question, depart_date):
        # Recuperar cities_in_questionon(ch
        cities_in_question = session_manager.get_session(chat_id, 'cities_in_question')
        print(cities_in_question)

        user_question += f"for {cities_in_question}."

        # TODO: MOSTRAR CARREGA A TELEGRAM AL USUARI

        city_found = False
        if cities_in_question:
            unique_cities = set(cities_in_question)
            if len(unique_cities) == 2 or (len(unique_cities) == 1 and city_context not in unique_cities):
                if len(unique_cities) == 2:
                    departure_city, destination_city = unique_cities
                else:
                    self.send_message(context, chat_id, self.gpt.humanize_response(
                        "I need you to specify me both origin and destination cities, could you reformulate the sentence?",
                        user_question, self.prp))
                # Realizar la petición a la API para obtener información de vuelos
                cheapestFlight, fastestFlight, bestFlight = self.travel_api.get_flight_info(departure_city,
                                                                                            destination_city,
                                                                                            depart_date)

                if cheapestFlight and fastestFlight and bestFlight:
                    response = f"Flights from {departure_city} to {destination_city}:\n"
                    response += "I have 3 options for you (Cheapest, Fastest, Best):\n"
                    response += f"\n\tCheapest flight: {cheapestFlight} \n\tFastest flight: {fastestFlight}.\n"
                    response += f"\tThe best flight is: {bestFlight}.\n"
                    await self.send_message(context, chat_id,
                                            self.gpt.humanize_response(response, user_question, self.prp))
                    city_found = True
                else:
                    print("I couldn't find any flights for the selected cities.")

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

        session_manager.clear_session(chat_id, 'cities_in_question')

    async def show_weather_recommendations(self, nouns, adverbs, weather_type, user_question, verbs, context, chat_id):
        if 'where' in adverbs or 'which' in adverbs or 'what' in adverbs or 'suggest' in verbs or 'recommend' in verbs:
            results = self.dao.search_by_weather_type(weather_type)

            if results:
                response = f"Top {weather_type} recommendations: "
                random_results = random.sample(results, min(2, len(results)))
                for city_info in random_results:
                    response += f"\n- {city_info['city']}, {city_info['country']}: Known for its {city_info['climate']} climate, {city_info['culture']} culture, and {', '.join(city_info['tourism_type'])} tourism."
                await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            else:
                print(f"No {weather_type} destinations found in the database.")
        else:
            await self.send_message(context, chat_id, self.gpt.not_understood_response())

    async def show_similar_cities(self, user_question, city_context, context, chat_id):
        city_found = False

        results = self.dao.search(city_context)
        if results:
            city_info = results[0]
            similar_cities = city_info.get('similar_destinations', [])
            response = f"The cities similar to {city_info['city']} are: {', '.join(similar_cities)}"
            await self.send_message(context, chat_id, self.gpt.humanize_response(response, user_question, self.prp))
            city_found = True

        if not city_found:
            await self.send_message(context, chat_id, self.gpt.city_not_in_database())

    """
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

    """
