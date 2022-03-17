'''
GPT 2
Encode each word to a number -> Specify length of output -> Decode each output number to words

# Extension: create a list of action stimuli for each action topic
'''
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import pipeline, set_seed
import random
# import tensorflow as tf
# tf.random.set_seed(random.randint(1, 100))

# ACTION_TYPES = [
#     'flood',
#     'coastal erosion'
# ]

generator = pipeline('text-generation', model='gpt2')


def gen_sentences(prompt="AGVN is sending emergency relief to Cyclone Debbie", max_length=1000):
    '''
    Generate sentences based on a prompt
    For emergencies, the prompt beginning is 'AGVN is sending emergency relief' or 'AGVN will directly assist in supporting'
    '''
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
    model = GPT2LMHeadModel.from_pretrained(
        'gpt2-large', pad_token_id=tokenizer.eos_token_id)
    # EOS = 'end of sentence' word '<|endoftext|>'

    # return the input id tensors as pytorch tensors (1D tensor)
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    # e.g. tensor([12 67 98 2])

    # beam search -> search for the appropriate next words as 5 beam trees
    # no repeat ngram -> do not repeat the same words after 2 times so we dont get stuck in a word repeat loop. When a sequence of two particular words is generated, it will not generate it again.
    # early_stopping -> stop when highest probability of next word is low
    output = model.generate(
        input_ids,
        max_length=max_length,
        do_sample=True,
        # num_beams=5,
        top_k=50,
        top_p=0.85,
        # no_repeat_ngram_size=2,
        early_stopping=False
    )
    # skip special tokens -> EOF, etc. that we dont need to output
    result = tokenizer.decode(output[0], skip_special_tokens=True)

    return result


def gen_blog_pipeline(prompt="AGVN is sending emergency relief to Cyclone Debbie. A disastrous event indeed.", max_length=1000):
    set_seed(69000)
    return generator(prompt, max_length=1000)[0]['generated_text']


def example_1():
    sample_1 = gen_sentences()
    states = ["NSW", "VIC", "NT", "WA", "SA", "ACT", "TAS", "QLD"]
    state = random.choice(states)
    sample_2 = gen_sentences(
        f"AGVN will directly assist in supporting victims of the recent flooding on {state}")

    print(sample_1)
    print(sample_2)


def example_2():
    sample_1 = gen_sentences(
        "The government will take measures to stop irresponsible and anti-competitive corporate conduct")
    print(sample_1)


def example_3():
    x = """
        Flooding is natural and cannot be stopped and can have both positive and negative impacts.

    The positive impacts of flooding, for example, include water for wetland ecosystems and replenishing soil moisture and nutrients.

    The negative impacts can bring substantial damages to homes and businesses, critical infrastructure and to farming, such as agriculture and crops. However, the negative effects of floods can be reduced with good planning and the right actions.

    Flood planning and action is a shared community responsibility. Local, state and federal governments all have a role to play in reducing the damage from floods in Victoria but so do you and your neighbours.
    """
    print(gen_blog_pipeline(x))
