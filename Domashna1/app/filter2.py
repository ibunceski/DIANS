from datetime import date, timedelta


class DataDateChecker:
    def __init__(self, storage):
        self.storage = storage

    def get_last_data_date(self, issuer):
        storage_data = self.storage.load_data()
        last_date = storage_data.get(issuer)

        if last_date:
            return last_date
        else:
            return date.today() - timedelta(days=3650)
