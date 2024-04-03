import os
import sys
from collections import namedtuple

Counts = namedtuple(
    "Counts", ["num_words", "num_paragraphs", "num_letters", "num_chars"]
)


def count_words_paragraphs_letters(file_path: str) -> Counts:
    with open(file_path, "r") as file:
        text = file.read()

    words = text.split()
    num_words = len(words)

    paragraphs = text.split("\n\n")  # Assuming paragraphs are separated by two newlines
    num_paragraphs = len(paragraphs)

    num_letters = len([char for char in text if char.isalpha()])

    num_chars = len(text)

    return Counts(num_words, num_paragraphs, num_letters, num_chars)


def count_file(file_path: str):
    counts = count_words_paragraphs_letters(file_path)
    print(f"--------- {file_path} ---------")
    print(f"Number of words: {counts.num_words}")
    print(f"Number of paragraphs: {counts.num_paragraphs}")
    print(f"Number of letters: {counts.num_letters}")
    print(f"Number of characters: {counts.num_chars}")
    print()


def count_directory(directory: str):
    print("Directory:", directory)
    for root, _, files in os.walk(directory):
        print("Root:", root)
        print("Files:", files)
        for filename in files:
            print("Filename:", filename)
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                count_file(file_path)


if __name__ == "__main__":
    path = sys.argv[1]

    if os.path.isdir(path):
        count_directory(path)
    elif os.path.isfile(path):
        count_file(path)
    else:
        print("Given path is neither a file nor a directory.", file=sys.stderr)
        exit(1)
