from abc import ABC
class _CustomeException(Exception):
    def __init__(self):
        self.error_name = ""
        self.error_data = ""

    def __str__(self):
        print(f"{self.error_name} {self.error_data}")
