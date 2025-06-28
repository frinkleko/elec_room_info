import os
import csv


class CSVRecordHandler:
    def __init__(self, csv_file_path, enabled=True):
        self.csv_file_path = csv_file_path
        self.enabled = enabled
        if enabled:
            self._ensure_csv_file()

    def _ensure_csv_file(self):
        if not os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, "w", newline="") as file:
                fieldnames = [
                    "timestamp",
                    "electricity_balance",
                    "air_conditioner_balance",
                    "water_balance",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def record(self, data):
        if self.enabled:
            with open(self.csv_file_path, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                writer.writerow(data)
