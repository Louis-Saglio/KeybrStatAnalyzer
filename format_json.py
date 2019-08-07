import json

from constants import DATA_FILE_PATH


def format_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        with open(path, "w+") as write_file:
            write_file.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    format_json(DATA_FILE_PATH)
