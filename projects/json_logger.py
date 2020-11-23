import os
import json

class JsonLogger:
    def __init__(self, filename, max_file_size_bytes, indent=4, sort_keys=True, default=str):
        self.max_file_size_bytes = max_file_size_bytes
        self.filename = filename
        self.indent = indent
        self.sort_keys = sort_keys
        self.default = default

    def write_json(self, data):
        if (os.path.getsize(self.filename) == self.max_file_size_bytes):
            os.rename(self.filename, f'{self.filename}'
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=self.indent, sort_keys=self.sort_keys, default=self.default)

