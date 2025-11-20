import json
import os

DATA_FILE = "data/data.json"


class DataManager:

    def __init__(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({"readings": {}, "tariffs": {}}, f)

    def load_all(self):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_all(self, data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_readings(self):
        return self.load_all().get("readings", {})

    def load_tariffs(self):
        return self.load_all().get("tariffs", {})

    def save_readings(self, readings):
        data = self.load_all()
        data["readings"] = readings
        self.save_all(data)

    def save_tariffs(self, tariffs):
        data = self.load_all()
        data["tariffs"] = tariffs
        self.save_all(data)
