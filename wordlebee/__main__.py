import os
from contextlib import suppress

import numpy as np
from rich import print
from rich.prompt import Confirm, Prompt


def filter_array(filter_func, words) -> np.ndarray:
    return np.array(list(filter(filter_func, words)))


def filter_words(words, letters, pos) -> np.ndarray:
    for char in letters:
        if pos == 0:  # not inside
            words = filter_array(lambda x: x.find(char) == -1, words)
        elif pos >= 1 and pos <= 5:  # known position
            words = filter_array(lambda x: x.find(char) == pos - 1, words)
        elif pos < 0:  # known not position
            words = filter_array(lambda x: x.find(char) != -1, words)
            words = filter_array(lambda x: x.find(char) != -pos - 1, words)
    return words


def get_words() -> np.ndarray:
    # Get data
    filepath = os.path.join(os.path.dirname(__file__), "data/words_filtered.txt")
    return np.loadtxt(filepath, dtype="str")


def print_help() -> None:
    print(
        "Help (?) [bold blue]position[/]: "
        + "([bold green]green[/]): 1 to 5, "
        + "([bold]black[/]): 0, "
        + "([bold yellow]yellow[/]): -1 to -5"
    )


def format_guess(guess) -> str:
    formated_guess = ""
    for char in guess:
        if char == "x":
            formated_guess += char
        else:
            formated_guess += "[bold white on green]" + char + "[/]"
    return formated_guess


def cli() -> None:

    # Init by parsing wordlist
    words = get_words()

    # Helper
    print_help()

    guess = "xxxxx"

    with suppress(KeyboardInterrupt):
        while True:
            # Get user input to filter words
            raw_input = Prompt.ask(
                f"Guess word ({format_guess(guess)}) [bold][[red]<letter(s)>[/red] [blue]<position>[/blue]][/]"
            )
            if raw_input[0] == "?":
                print_help()
                continue
            else:
                # Parse input
                letters, pos_str = raw_input.split(" ")
                pos = int(pos_str)
                # Filter words
                words = filter_words(words, letters, pos)
                if pos > 0:
                    guess = guess[: pos - 1] + letters[0] + guess[pos:]

            # Print status
            if len(words) == 1:
                guess = words[0]
                print(f"Solution: [bold green]{guess}[/] :partying_face:")
                break

            elif len(words) == 0:
                print("Failed!", ":sob:")

                restart = Confirm.ask("Restart guess?")
                if restart:
                    words = get_words()
                    guess = "xxxxx"
                else:
                    break

            else:
                print("Possible words:", words)


if __name__ == "__main__":
    cli()
