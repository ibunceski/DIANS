import pickle
from pathlib import Path


class DataStorage:
    def __init__(self, storage_path="issuers_data.pkl"):
        self.storage_path = Path(storage_path)
        self.ensure_storage_exists()

    def ensure_storage_exists(self):
        if not self.storage_path.exists():
            self.save_data({})

    def load_data(self):
        try:
            with open(self.storage_path, 'rb') as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, EOFError):
            print(f"Warning: Could not load data from {self.storage_path}. Creating new storage.")
            return {}

    def save_data(self, data):
        with open(self.storage_path, 'wb') as f:
            pickle.dump(data, f)

    def update_issuer(self, issuer: str, last_date: str):
        data = self.load_data()
        data[issuer] = last_date
        self.save_data(data)
