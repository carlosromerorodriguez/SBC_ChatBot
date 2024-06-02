

<div style="text-align: center;">
    <h1>Exploryst ChatBot</h1>
    <img src="ChatBot/images/logo.jpg" alt="Project Logo" style="width:200px;"/>
</div>  

Exploryst is a chatbot that helps you explore the world and make your travel plans. It can provide you with information about the weather, culture, restaurants..., and even suggest places to visit. It is a great tool for travelers who want to make the most of their trips.

## Requirements

- Python 3.11, 3.11.5, 3.12 (hasn't been tested on other versions)
- Internet Connection
- Telegram Account

# How to run the project
## Creating the Virtual Environment

To create a virtual environment, run the following command in the terminal in the project directory:

```sh
python -m venv env
```

This will create a folder `env` in your current directory where all dependencies will be installed.

## Activating the Virtual Environment

To activate the virtual environment, use the following command:

### Windows

```sh
env\Scripts\activate
```

### MacOS/Linux

```sh
source env/bin/activate
```

## Installing Dependencies

Once the virtual environment is activated, you can install the required dependencies with:

```sh
cd Chatbot
pip install -r requirements.txt
```

## Running the Project

Once the environment is set up, access this link on the internet: [t.me/exploryst_bot](https://t.me/exploryst_bot). Once you are in the bot's chat, run the following command in the project terminal:

```sh
python bot.py
```

This will start the bot, and you can interact with it via Telegram.

## Question examples

Questions can be asked in different ways. Here are some examples of questions that the chatbot can answer:

### Simple questions
```python
simple_questions = [
    "What is the weather like in Barcelona?",
    "What kind of food can I eat in Paris?",
    "What are the best attractions to visit in Rome?",
    "What language do they speak in Tokyo?",
    "What currency is used in London?",
    "What other languages are spoken in Berlin?",
    "Can you recommend a restaurant in New York?",
    "Where can I stay in Dubai?",
    "How do I get around in Amsterdam?",
    "What is the culture like in Istanbul?",
    "What kind of tourism is popular in Berlin?",
    "How do I fly from Paris to London?",
    "How expensive is living in San Francisco?",
    "Which cuisine is famous in Bangkok?",
    "When is the best time to visit Vienna?",
    "Why should I visit Prague?",
    "How do I get around in Hong Kong?",
    "Any similar cities to Tokyo?",
]
```

### Double questions
```python
double_questions = [
    "What is the weather like in Barcelona and what kind of food can I eat there?",
    "What are the best attractions to visit in Rome and what language do they speak there?",
    "What currency is used in London and what other languages are spoken there?",
    "Can you recommend a restaurant in New York and where can I stay there?",
    "How do I get around in Amsterdam and what is the culture like in Istanbul?",
    "What kind of tourism is popular in Berlin and how do I fly from Paris to London?",
    "How expensive is living in San Francisco and which cuisine is famous in Bangkok?",
    "When is the best time to visit Vienna and why should I visit Prague?",
    "How do I get around in Hong Kong and are there any similar cities to Tokyo?",
]
```

### Contextual questions

To ask a contextual question the chatbots needs to know a city. The city can be set by sending a message with the city name to the bot. Or asking the bot for destinations that require certain adjectives.

```python
simple_context_questions = [
    "What is the weather like?",
    "What kind of food can I eat?",
    "What are the best attractions to visit?",
    "What language do they speak?",
    "What currency is used?",
    "How do they pay?",
    "What other languages are spoken?",
    "Can you recommend a restaurant?",
    "Where can I stay?",
    "How do I get around?",
    "What is the culture like?",
    "What kind of tourism is popular?",
    "What are the modern attractions?",
    "How expensive is living there?",
    "When is the best time to visit?",
    "Why should I visit it?",
    "Any similar cities there?",
]
```

### Suggestions

```python
suggestion_questions = [
    "Suggest me warm and expensive destinations that have a beach",
    "Suggest me a place that has mountains and is cold to go skiing",
]
```

## Deactivating the Virtual Environment

To deactivate the virtual environment, you can use:

```sh
deactivate
```

Thank you for setting up your development environment!
