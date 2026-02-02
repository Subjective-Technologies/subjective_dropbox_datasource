import os
from subjective_abstract_data_source_package import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger

class SubjectiveDropboxDataSource(SubjectiveDataSource):
    def fetch(self):
        return []

    def get_icon(self) -> str:
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        try:
            with open(icon_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            BBLogger.log(f"Error reading icon file: {e}")
            return ""

    def get_connection_data(self) -> dict:
        return {"connection_type": "Custom", "fields": ["connection_name"]}
