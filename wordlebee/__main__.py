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


def print_help() -> None:
    print(
        "Help (?) [bold blue]position[/bold blue]: "
        + "([bold green]green[/bold green]): 1 to 5, "
        + "(black): 0, "
        + "([bold yellow]yellow[/bold yellow]): -1 to -5"
    )


def cli() -> None:

    # Init by parsing wordlist
    words = get_words()

    # Helper
    print_help()

    while True:
        # Get user input to filter words
        raw_input = Prompt.ask(
            "Enter [bold][[red]<letter(s)>[/red] [blue]<position>[/blue]][/bold]"
        )
        if raw_input[0] == "?":
            print_help()
            continue
        else:
            # Parse input
            letters, pos_str = raw_input.split(" ")
            pos = int(pos_str)
            # Filter words
            for char in letters:
                if pos == 0:  # not inside
                    words = filter_word(lambda x: x.find(char) == -1, words)
                elif pos >= 1 and pos <= 5:  # known position
                    words = filter_word(lambda x: x.find(char) == pos - 1, words)
                elif pos < 0:  # known not position
                    words = filter_word(lambda x: x.find(char) != -1, words)
                    words = filter_word(lambda x: x.find(char) != -pos - 1, words)
                else:
                    break

        # Print status
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
