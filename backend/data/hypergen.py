'''
Module consisting of auxiliary functions
'''
import string
from random import choice, choices
from functools import reduce
from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

DEBUG_OUT = lambda x: print("DEBUG:", x)

def gen_strings(n, max_gen=20, lowercase=False):
    '''
    Generate n strings of maximum max_gen length
    @max_gen >= 1
    '''
    use_string = string.ascii_letters
    if lowercase:
        use_string = string.ascii_lowercase

    strings = []
    for _ in range(n):
        gen = choices(use_string+" ", k=max_gen)
        # always ensure first letter is a non space
        gen[0] = choice(use_string)
        strings.append(reduce(lambda x, y: x+y, gen))

    return strings if n > 1 else strings[0]


def gen_text_list(prompts):
    '''
    Generates random text based on prompts.
    Uses GPT-Neo as backend -> Insert a prompt for the model to infer (generator sequencing)
    :param: n -> int
    :param: prompts -> str or list of strings

    NOTE: prompts shouldn't be too large as this can take a long time to generate
    '''
    responses = []
    if type(prompts) == list:
        for i in range(len(prompts)):
            responses.append(generator(prompts[i], do_sample=True, min_length=50)[0])
        return responses
    else:
        return generator(prompts, do_sample=True, min_length=50)[0]

