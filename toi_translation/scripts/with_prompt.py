import sys


# PROMPT = f"""Translate the following English article to {LANGUAGE}, providing context for the cultural references
#
# """

if __name__ == "__main__":
    if len(sys.argv) == 2:
        FROM_LANGUAGE = "English"
        TO_LANGUAGE = "Hindi"
        file_path = sys.argv[1]
    elif len(sys.argv) > 2:
        FROM_LANGUAGE = sys.argv[1]
        TO_LANGUAGE = sys.argv[2]
        file_path = sys.argv[3]
    else:
        print("Invalid arguments.", file=sys.stderr)
        exit(1)

    with open(file_path, "r") as file:
        file_text = file.read()

    PROMPT = f"Translate the following {FROM_LANGUAGE} text to {TO_LANGUAGE}:\n\n"

    print(PROMPT + file_text)
