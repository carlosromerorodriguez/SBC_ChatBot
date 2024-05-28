import json
class KnowledgeDAO:
    def __init__(self):
        with open('knowledge/knowledge.json', 'r') as file:
            self.knowledge = json.load(file)

    def search(self, city):
        # Lógica para buscar en la base de conocimiento
        results = []
        for entry in self.knowledge:
            if entry['city'].lower() == city.lower():
                results.append(entry)

        return results
