from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from process_petition import ProcessPetition
from preprocessing.preprocessor import Preprocessor
from nlp.nlp_processor import *
from api.gpt_api import GPTAPI

# TODO: Logica de fechas (ej: inicial > final)
# TODO: Check date format in hotel i flight petitions
# TODO: Segueix ficant la ciutat com a context a la resposta del GPT quan no toca, exemple: Suggest...
# TODO: input flights hotels per telegram
# TODO: Pulir preprocessing

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
    "How do I get around in Hong Kong?"
    "Any similar cities to Tokyo?",
]


async def send_message_to_telegram(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str) -> None:
    message = await context.bot.send_message(chat_id=chat_id, text=text)
    context.user_data['messages'].append(message.message_id)


gpt = GPTAPI()
prp = Preprocessor()
process_petition = ProcessPetition(prp, send_message_to_telegram)
nlp = NLPProcessor(prp, process_petition)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'messages' not in context.user_data:
        context.user_data['messages'] = []

    message = await update.message.reply_text('¡Hola! Soy tu bot de Telegram.')
    context.user_data['messages'].append(update.message.message_id)
    context.user_data['messages'].append(message.message_id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'messages' not in context.user_data:
        context.user_data['messages'] = []

    text = update.message.text
    chat_id = update.message.chat_id
    user_input = text

    if gpt.is_greeting_input(user_input):
        await send_message_to_telegram(context, chat_id, gpt.salutation_response())
        return
    elif gpt.is_goodbye_input(user_input):
        await send_message_to_telegram(context, chat_id, gpt.goodbye_response())
        return
    elif gpt.is_asking_for_me(user_input):
        await send_message_to_telegram(context, chat_id, gpt.start_response())
        return

    separated_questions = gpt.split_questions(user_input)
    if separated_questions:
        questions = separated_questions.split(' ; ')
    else:
        questions = [user_input]

    for question in questions:
        transformed_input, flagCont, city_context = prp.transform_input_with_fallback_to_gpt(question)
        if flagCont:
            continue

        exitFlag = await nlp.process(transformed_input, city_context, context, chat_id)

        if exitFlag:
            print("El proceso ha terminado.")
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
