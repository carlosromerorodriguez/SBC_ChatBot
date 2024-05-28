from api.gpt_api import GPTAPI


contemplated_verbs = ["viajar", "conocer", "visitar", "explorar"]
contemplated_nouns = ["viaje", "destino", "lugar", "ciudad"]
contemplated_adjectives = ["increíble", "maravilloso", "interesante", "divertido"]

def convert_input(user_input):
    gpt = GPTAPI()
    return gpt.transform_input(user_input, contemplated_verbs, contemplated_nouns, contemplated_adjectives)