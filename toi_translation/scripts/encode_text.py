import json
import os
import sys


def encode(text: str) -> str:
    # return text.encode().decode()
    return json.dumps(text)


if __name__ == "__main__":
    path = sys.argv[1]

    if not os.path.isfile(path):
        print("Given path is neither a file nor a directory.", file=sys.stderr)
        exit(1)

    with open(path, "r") as file:
        text = file.read()

    encoded_text = encode(text)
    print(encoded_text)
