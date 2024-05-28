from api.gpt_api import GPTAPI

# Context Nouns
contemplated_nouns = [
    'cuisine', 'attractions', 'language', 'food', 'beach', 'city', 'cost', 'culture', 'transport',
    'places', 'experiences', 'reasons', 'time', 'tourism', 'weather', 'country', 'rating', 'destination', 'tour',
    'currency', 'activities', 'public_transport', 'car_rental', 'taxi',
]

# Context adjectives
contemplated_adjectives = [
    'expensive', 'cultural', 'historical', 'best', 'cheap', 'moderate', 'modern', 'traditional', 'warm', 'cold', 'mild',
    'variable', 'free'
]

# Context verbs
contemplated_verbs = [
    'show', 'suggest', 'visit', 'go', 'get around', 'eat', 'see'
]


# Context adverbs
contemplated_adverbs = [
    'what', 'where', 'when', 'why', 'which', 'how'
]


def convert_input(user_input):
    gpt = GPTAPI()
    return gpt.transform_input(user_input, contemplated_verbs, contemplated_nouns, contemplated_adjectives)