import re
import numpy as np
from rich import print
from rich.prompt import Prompt, Confirm
import os

def filter_word(filter_func, words):
    return np.array(list(filter(filter_func, words)))

def get_words():
    # Get data
    filepath = os.path.join(os.path.dirname(__file__), 'data/words_filtered.txt')
    return np.loadtxt(filepath, dtype='str')

def cli():
    
    words = get_words()
    
    while True:
        # Get user input to filter words
        char, flag = Prompt.ask('Enter [bold][[red]<Letter>[/red] [green]<position>[/green]][/bold] (position: 1-5, not: -1, unknown: 0)').split(' ')
        # Clean input
        char = char.lower()
        flag = int(flag)
        if flag == -1: # Not 
            words = filter_word(lambda x: x.find(char) == -1, words)
        elif flag == 0:
            words = filter_word(lambda x: x.find(char) != -1, words)
        elif flag >= 1 and flag <= 5:
            words = filter_word(lambda x: x.find(char) == flag-1, words)
        else:
            break
        if len(words) == 1:
            print(f'Solution: [bold][green]{words[0]}[/green][/bold] :partying_face:')
             
            break
        elif len(words) == 0:
            print('Failed!', ':sob:')
            restart = Confirm.ask('Restart guess?')
            if restart:
                words = get_words()
            else:
                break
        else:            
            print(f'Possible words:', words)
            
if __name__ == "__main__":
    cli()
