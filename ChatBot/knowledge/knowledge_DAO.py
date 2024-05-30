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
            if tourism_type in entry['tourism_type']:
                results.append(entry)
        return results

    def search_by_culture_type(self, culture_type):
        results = []
        for entry in self.knowledge:
            if entry['culture'].lower() == culture_type.lower():
                results.append(entry)
        return results