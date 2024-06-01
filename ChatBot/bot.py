import asyncio
import threading
from queue import Queue, Empty
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from process_petition import ProcessPetition
from preprocessing.preprocessor import Preprocessor
from nlp.nlp_processor import NLPProcessor
from api.gpt_api import GPTAPI
from session_manager import session_manager


test_questions = [
    "What is the weather like in Barcelona?",
    "What kind of food can I eat in Paris?",
    "What are the best attractions to visit in Rome?",
    "What language do they speak in Tokyo?",
    "What currency is used in London?",
    "How do they pay in Moscow?",
    "What other languages are spoken in Berlin?",
    "Can you recommend a restaurant in New York?",
    "Where can I stay in Dubai?",
    "How can I get to Sydney?",
    "How do I get around in Amsterdam?",
    "What is the culture like in Istanbul?",
    "What kind of tourism is popular in Berlin?",
    "Is there a beach in Miami?",
    "What are the modern attractions in Barcelona?",
    "How expensive is living in San Francisco?",
    "Which cuisine is famous in Bangkok?",
    "When is the best time to visit Vienna?",
    "Why should I visit Prague?",
    "How do I get around in Hong Kong?",
    "Any similar cities to Tokyo?",
    "Suggest me warm and expensive destinations that have a beach"
]

# Queue to store pending responses
pending_requests = {}
response_queues = {}


def handle_response_queue(chat_id, response_queue, context):
    while True:
        try:
            response = response_queue.get(timeout=2)  # Esperar por una respuesta durante 2 segundos en cada iteración
            if response:
                return response
        except Empty:
            continue  # Continua esperant
        except Exception as e:
            print(f"Error handling response for chat_id {chat_id}: {e}")
            return None

def process_messages(context, chat_id):
    while True:
        if 'messages' not in context.user_data:
            context.user_data['messages'] = []

        # Comprobar si estamos esperando una respuesta
        if context.user_data.get('waiting_for_response'):
            print("Estoy esperando una respuesta")
            response = handle_response_queue(chat_id, response_queues[chat_id], context)
            if response:
                context.user_data['waiting_for_response'] = False
                print("Respuesta recibida y procesada")
                return response


async def send_message_to_telegram(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str) -> None:
    message = await context.bot.send_message(chat_id=chat_id, text=text)
    context.user_data['messages'].append(message.message_id)


async def send_message_and_wait_for_response(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str) -> str:
    response_queue = Queue()
    response_queues[chat_id] = response_queue

    await send_message_to_telegram(context, chat_id, text)
    print("Esperando respuesta... 1")

    # Utilitzar un thread per processar els missatges
    response = await asyncio.to_thread(process_messages, context, chat_id)

    if response is None:
        await context.bot.send_message(chat_id=chat_id, text="Tiempo de espera agotado. Por favor, intenta de nuevo.")
    return response


async def receive_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_input = update.message.text

    if chat_id in response_queues:
        response_queue = response_queues[chat_id]
        response_queue.put(user_input)
        print("Respuesta recibida y puesta en la cola")


gpt = GPTAPI()
prp = Preprocessor(send_message_to_telegram)
process_petition = ProcessPetition(prp, send_message_to_telegram, send_message_and_wait_for_response)
nlp = NLPProcessor(prp, process_petition, send_message_to_telegram)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'messages' not in context.user_data:
        context.user_data['messages'] = []

    message = await update.message.reply_text(gpt.start_response())
    context.user_data['messages'].append(update.message.message_id)
    context.user_data['messages'].append(message.message_id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("message received")
    if 'messages' not in context.user_data:
        context.user_data['messages'] = []

    # Comprobar si estamos esperando una respuesta
    if context.user_data.get('waiting_for_response'):
        print("Estoy esperando una respuesta")
        await receive_response(update, context)
        return

    text = update.message.text
    chat_id = update.message.chat_id
    user_input = text

    # Si flag check-in vol
    if session_manager.get_session(chat_id, 'cities_in_question'):
        print(session_manager.get_session(chat_id, 'cities_in_question'))
        await process_petition.flight_api_request(prp.city_context, chat_id, context, "Can you recommend me flights", user_input)
        return

    # Si flag check-in hotel
    if session_manager.get_session(chat_id, 'asking_for_hotel_check_in'):
        await process_petition.save_hotel_check_in_date(context, chat_id, user_input)
        return

    # Si el flag check out hotel
    if session_manager.get_session(chat_id, 'asking_for_hotel_check_out'):
        await process_petition.hotel_api_request(prp.city_context, chat_id, context, user_input)
        return

    if gpt.is_greeting_input(user_input):
        await send_message_to_telegram(context, chat_id, gpt.salutation_response())
        return
    elif gpt.is_goodbye_input(user_input):
        await send_message_to_telegram(context, chat_id, gpt.goodbye_response())
        return
    elif gpt.is_asking_for_me(user_input):
        await send_message_to_telegram(context, chat_id, gpt.start_response())
        return
    elif gpt.is_thanking_me(user_input):
        await send_message_to_telegram(context, chat_id, gpt.thanking_response())
        return

    separated_questions = gpt.split_questions(user_input)
    if separated_questions:
        questions = separated_questions.split(' ; ')
    else:
        questions = [user_input]

    for question in questions:
        transformed_input, flagCont, city_context = await prp.transform_input_with_fallback_to_gpt(question, chat_id, context)
        if flagCont:
            continue

        exitFlag = await nlp.process(transformed_input, city_context, context, chat_id)

        if exitFlag:
            await send_message_to_telegram(context, chat_id, gpt.goodbye_response())
            return


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id

    await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)

    if 'messages' in context.user_data:
        for msg_id in context.user_data['messages']:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"Error al borrar mensaje {msg_id}: {e}")
        context.user_data['messages'] = []


def main() -> None:
    application = Application.builder().token("7435215887:AAEJOiLco8PY2m26PqtysIRhtuNtdhZ--nY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()