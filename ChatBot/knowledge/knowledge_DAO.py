import json
class KnowledgeDAO:
    def __init__(self):
        with open('knowledge/knowledge.json', 'r', encoding='utf-8') as file:
            self.knowledge = json.load(file)

    def search(self, city):
        # Lógica para buscar en la base de conocimiento
        results = []
        for entry in self.knowledge:
            if entry['city'].lower() == city.lower():
                results.append(entry)

        return results

    def search_by_tourism_type(self, tourism_type):
        results = []
        for entry in self.knowledge:
            if tourism_type.lower() in entry['tourism_type']:
                results.append(entry)
        return results

    def search_by_culture_type(self, culture_type):
        results = []
        for entry in self.knowledge:
            if entry['culture'].lower() == culture_type.lower():
                results.append(entry)
        return results

    def search_by_weather_type(self, weather_type):
        results = []
        for entry in self.knowledge:
            if entry['climate'].lower() == weather_type.lower():
                results.append(entry)
        return results

    def search_by_price_range(self, price_range):
        results = []
        for entry in self.knowledge:
            if entry['cost'].lower() == price_range.lower():
                results.append(entry)
        return results

    def search_by_adjectives(self, adjectives):
        result = []
        for city in self.knowledge:
            matches = {adj: False for adj in adjectives}  # Diccionari per rastrejar els adjectius trobats
            for key, value in city.items():
                if key not in ['restaurants', 'activities', 'best_times_to_visit', 'transport']:  # Excloent restaurants i activitats
                    if isinstance(value, str):
                        for adj in adjectives:
                            if adj.lower() in value.lower():
                                matches[adj] = True
                    elif isinstance(value, list):
                        for adj in adjectives:
                            if any(adj.lower() in item.lower() for item in value if isinstance(item, str)):
                                matches[adj] = True
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, str):
                                for adj in adjectives:
                                    if adj.lower() in sub_value.lower():
                                        matches[adj] = True
                            elif isinstance(sub_value, list):
                                for adj in adjectives:
                                    if any(adj.lower() in item.lower() for item in sub_value if isinstance(item, str)):
                                        matches[adj] = True
            if all(matches.values()):  # Si tots els adjectius estan presents
                result.append(city)
        return result

