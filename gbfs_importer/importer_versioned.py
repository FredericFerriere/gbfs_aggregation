import requests
import datetime


class ImporterVersioned:
    """
    Abstract class to define common methods to be implemented by versioned_importer
    """
    file_updates = {}

    def import_sub_files(self, file_list: []):
        for el in file_list:
            self.process_sub_file(el['name'], el['url'])

    def process_sub_file(self, file_name: str, file_url: str):
        return

    @staticmethod
    def read_file(file_url: str):
        response = requests.get(file_url)
        data = response.json()
        return data

    @classmethod
    def need_update(cls, file_name, file_update_time):
        if file_name not in cls.file_updates:
            cls.file_updates[file_name] = file_update_time
            return True
        if file_update_time - cls.file_updates[file_name] <= datetime.timedelta(seconds=10):
            return False
        cls.file_updates[file_name] = file_update_time
        return True


