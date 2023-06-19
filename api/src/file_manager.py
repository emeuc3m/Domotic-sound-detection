import json

class FileManager():
    def open_json(self, path: str):
        with open(path) as file:
            return json.load(file)
    def save_json(self, data: dict, path:str):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
        return
