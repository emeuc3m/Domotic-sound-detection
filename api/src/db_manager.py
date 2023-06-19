from file_manager import FileManager
DEFAULT_DB_PATH = "./db.json"
class DBManager():
    def __init__(self, path=DEFAULT_DB_PATH):
        self.db_path = path
        self.file_manager = FileManager()
    
    def get_db(self) -> list[dict]:
        return self.file_manager.open_json(self.db_path)
    def save_to_db(self, data: dict):
        self.file_manager.save_json(data, self.db_path)
        return