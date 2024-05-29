import openai
import random


class GPTAPI:
    API_KEY = "sk-proj-HpMoLYRWcDGxR48zvvGiT3BlbkFJIaC5flIDtLiuIAEjcuhe"
    openai.api_key = API_KEY

    def transform_input(self, user_input, adverbs, verbs, nouns, adjectives, non_matching_words):
        prompt = (
            f"Transform the sentence '{user_input}' by replacing the words {', '.join(non_matching_words)} "
            f"with suitable words from the provided lists of adverbs, verbs, nouns, and adjectives. "
            f"Ensure the sentence retains its original meaning. "
            f"Here are the lists of words to use: "
            f"Adverbs: {', '.join(adverbs)}. "
            f"Verbs: {', '.join(verbs)}. "
            f"Nouns: {', '.join(nouns)}. "
            f"Adjectives: {', '.join(adjectives)}. "
            f"Output only the transformed sentence without any additional text or highlighted words."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=300,
                stream=False,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None


    def humanize_response(self, response):
        prompt = f"Rephrase this response to be more natural, I mean, more human and coherent: {response}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                stream=False,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def goodbye_response(self):
        prompts = [
            "Generate only a concise and kind farewell message as a chatbot. Respond only the chatbot response"
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                stream=False,
            )
            # Extraer el contenido del mensaje de la respuesta
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def start_response(self):
        prompt = (
            "You are Exploryst, a friendly and knowledgeable travel assistant chatbot. Generate a welcoming "
            "introduction message for new users."
            "Introduce yourself, explain your role, and invite users to ask questions about travel destinations, "
            "accommodations, and activities."
            "Keep the tone warm and welcoming."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120,
                stream=False,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def salutation_response(self):
        prompts = [
            "Acting as a chatbot generate a friendly greeting response to a user saying hello.",
            "Acting as a chatbot create a welcoming message to respond to a user's greeting.",
            "Acting as a chatbot generate a warm and friendly hello message to a user."
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                stream=False,
            )
            # Extraer el contenido del mensaje de la respuesta
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def not_understood_response(self):
        prompts = [
            "Generate a response that indicates you didn't understand the user's message, but make it polite and ask them to rephrase.",
            "Create a response where you apologize for not understanding the user's input and ask them to clarify.",
            "Generate a message that shows confusion and requests the user to explain their message in a different way."
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                stream=False,
            )
            # Extraer el contenido del mensaje de la respuesta
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def is_greeting_input(self, user_input):
        prompts = [
            f"Given this message: {user_input}, respond YES if it is a greeting or welcome input and NO otherwise"
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                stream=False,
            )

            # Extraer el contenido del mensaje de la respuesta
            reformulated_response = response.choices[0].message.content
            if reformulated_response == "YES":
                return True
            return False
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def is_goodbye_input(self, user_input):
        prompts = [
            f"Given this message: {user_input}, respond YES if it is a goodbye inpunt and NO otherwise"
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                stream=False,
            )
            # Extraer el contenido del mensaje de la respuesta
            reformulated_response = response.choices[0].message.content
            if reformulated_response == "YES":
                return True
            return False
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def is_asking_for_me(self, user_input):
        prompts = [
            f"Given this message: {user_input}, respond YES if it is a message that is asking for any Exploryst (a chatbot) information (name, what it does, etc...) and NO otherwise"
        ]
        prompt = random.choice(prompts)

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                stream=False,
            )

            reformulated_response = response.choices[0].message.content
            if reformulated_response == "YES":
                return True
            return False
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def city_not_in_database(self):
        prompt = (
            f"Act as a chatbot, generate a response to inform the user that the city introduced is not in the database. "
            "Apologize for the inconvenience and suggest asking about another city."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None

    def get_cities(self, user_input):
        prompt = (
            f"Given the user input: '{user_input}', identify the known cities mentioned in the text. "
            f"Generate a dictionary where the keys are the original city names found (with possible misspellings) and the values are the corrected city names. "
            f"Ensure the city names are correctly spelled and in lowercase if there are any errors. "
            f"If there are no cities, return an empty dictionary."
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=100,
                stream=False,
            )

            # Convertir la respuesta en una lista de ciudades
            city_dict = eval(response.choices[0].message.content.strip())
            return city_dict
        except Exception as e:
            print(f"Error en la llamada a la API de GPT: {e}")
            return None