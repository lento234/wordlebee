import os

import numpy as np
from rich import print
from rich.prompt import Confirm, Prompt


def filter_word(filter_func, words) -> np.ndarray:
    return np.array(list(filter(filter_func, words)))


def get_words() -> np.ndarray:
    # Get data
    filepath = os.path.join(os.path.dirname(__file__), "data/words_filtered.txt")
    return np.loadtxt(filepath, dtype="str")


def cli() -> None:

    words = get_words()

    while True:
        # Get user input to filter words
        raw_input = Prompt.ask(
            "Enter [bold][[red]<Letter>[/red] [green]<position>[/green]][/bold] (position: 1-5, not: -1, unknown: 0)"
        ).split(" ")
        # Clean input
        char = raw_input[0].lower()
        pos = int(raw_input[1])
        if pos == -1:
            words = filter_word(lambda x: x.find(char) == -1, words)
        elif pos == 0:
            words = filter_word(lambda x: x.find(char) != -1, words)
        elif pos >= 1 and pos <= 5:
            words = filter_word(lambda x: x.find(char) == pos - 1, words)
        else:
            break
        if len(words) == 1:
            print(f"Solution: [bold][green]{words[0]}[/green][/bold] :partying_face:")

            break
        elif len(words) == 0:
            print("Failed!", ":sob:")
            restart = Confirm.ask("Restart guess?")
            if restart:
                words = get_words()
            else:
                break
        else:
            print("Possible words:", words)


if __name__ == "__main__":
    cli()
