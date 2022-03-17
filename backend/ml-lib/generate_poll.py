import random
from datetime import datetime
from functools import reduce
from transformers import pipeline
from generate_blog import gen_blog_pipeline

nlp = pipeline("question-answering")

# context = r"""
# Extractive Question Answering is the task of extracting an answer from a text given a question. An example of a
# question answering dataset is the SQuAD dataset, which is entirely based on that task. If you would like to fine-tune
# a model on a SQuAD task, you may leverage the `run_squad.py`.
# """


def fstr(template, **kwargs):
    return eval(f"f'{template}'", kwargs)


def reduce_strings(string_list):
    '''
    Reduce a list of strings into a single string
    '''
    return str(reduce(lambda x, y: str(x)+','+str(y), string_list))


# print(nlp(question="What is extractive question answering?", context=context))
# print(nlp(question="What is a good example of a question answering dataset?", context=context))


question_type = ['economics', 'lifestyle', 'community', 'infrastructure', 'international', 'health',
                 'education', 'national security', 'safety', 'industry', 'science', 'environment']
question_policy = ['taxation', 'lifestyle', 'community', 'infrastructure', 'foreign relations', 'health', 'education',
                   'national security', 'safety', 'industry', 'science', 'environment', 'energy', 'assets', 'economy', 'foreign trade', 'natural resources']
question_policy_map = {
    'taxation': ['income', 'individualism', 'government control', 'fairness', 'income', 'salary', 'tired', 'taxes'],
    'lifestyle': ['life', 'living conditions', 'situation', 'home', 'way of living', 'happiness', 'culture'],
    'community': ['neighborhood', 'public', 'home', ''],
    'infrastructure': ['public transport', 'public infrastructure', 'public utilities', 'housing', 'roads', 'rail', 'sanitation'],
    'foreign relations': ['geopolitics', 'public administration', 'international', 'competition', 'tariffs', 'sanctions', 'genocide', 'war', 'friendly'],
    'health': ['sanitation', 'illness', 'standard of living', 'hospitals', 'aged care', 'youth care', 'welfare'],
    'education': ['schools', 'vocational training', 'productivity', 'higher education', 'universities', 'public schools', 'private schools', 'early education', 'training', 'employment', 'jobs', 'growth', 'salary', 'future'],
    'national security': ['security', 'safety', 'foreign', 'immigration', 'migration', 'invasion', 'defense', 'protection'],
    'safety': ['safety', 'welfare', 'protection', 'prevention', 'danger', 'industry safety', 'workplace safety'],
    'industry': ['industrial', 'manufacturing', 'production', 'construction', 'business', 'energy', 'labor', 'work', 'tradesmen', 'trade', 'profession'],
    'science': ['science', 'physics', 'technology', 'reason', 'proof', 'advances', 'advancement', 'scientist', 'engineer', 'maths', 'profession', 'scientific method', 'innovation', 'invention', 'future', 'competition'],
    'environment': ['parks', 'waste'],
    'energy': ['natural', 'fossil fuels', 'renewable energy', 'green', 'sustainability', 'environment', 'growth', 'independence'],
    'assets': ['economy', 'budget', 'production'],
    'economy': ['economics', 'economy', 'jobs', 'growth', 'trade', 'interest rates'],
    'foreign trade': ['international', 'economy', 'tarrifs', 'exchange rates'],
    'natural resources': ['assets', 'renewable', 'sustainability'],
}
question_prompts = [r'What do you think about {x}', r'Do you like the idea of {x}', r'How much do you like about {x}',
                    r'If you would think about how {x} affects you', r'What impact does {x} have on you']

# idea => add 1 or 2 words to the text for the AI to generate from
Sentiments = {
    "good": ["Positive",  "Support", "For", "Accept", "Agree", "Appealing", "Esteemed", "Secure", "Safe", "Vigorous", "Whole", "Thriving"],
    "bad": ["Against", "Problematic", "Adverse", "Corrupt", "Corrosive", "Deformed", "Dishonest", "Decaying", "Distress", "Guilty", "Hate", "Ignorant", "Lose", "Sad", "Suspect", "Stressful", "Stupid", "Sickening"],
    "great": ["Great", "Amazing", "Loving it", "Attractive", "Brilliant", "Elegant", "Enthusiastic", "Engaging", "Excellent", "Wonderful", "Worthy", "Win"],
    "terrible": ["Terrible", "Horrific", "Fear", "Frustration", "Abysmal", "Faulty", "Damaging", "Alarming", "Criminal", "Dreadful", "Dismal", "Enraged", "Grim", "Noxious", "Offensive", "Oppressive", "Repugnant", "Worthless"]
}

"""
Idea
    - receive a question topic (policy type)
    - generate a random question based on that topic
    - randomly choose a question type
    - if the question is not scale based or short answer
        - generate 4 more questions
        - concat all the policy type synonyms together with join ' '
        - autocomplete that into a complete text
        - for all 4 questions
        - use the question answer format
"""


def reduce_nlp_answers(answers):
    '''
    In - [{score, start, answer}]
    Out - [answer1, answer2, etc.]
    '''
    res = list(map(lambda x: x["answer"], answers))
    return res


def gen_multichoice_question(policy_type, sentiment=None):
    topic = policy_type

    prompts = question_prompts
    prompt_to_use = random.choice(prompts)

    # generate N different questions for N question prompts
    questions = [i for i in prompts]
    for p in prompts:
        # choose a random topic
        topic_temp = random.choice(question_policy_map[topic])
        # append to question
        questions.append(fstr(p, x=topic_temp))

    specific_topic = random.choice(question_policy_map[topic])
    prompt = fstr(prompt_to_use, x=specific_topic)

    text = ' '.join(question_policy_map[topic])
    text += ' Australia '  # to make it more relevant
    if sentiment: text += random.choice(Sentiments[sentiment])

    # autocomplete full text
    text = gen_blog_pipeline(text)

    # generate answers
    # for each question in questions
    possible_answers = []
    for q in questions:
        ans = nlp(question=q, context=text)
        possible_answers.append(ans)

    possible_answers = reduce_nlp_answers(possible_answers)
    # remove duplicates
    possible_answers = list(dict.fromkeys(possible_answers))

    question = f"{prompt}"
    return question, possible_answers, "multiple_choice"


def gen_dropdown_question(policy_type, sentiment=None):
    topic = policy_type

    prompts = question_prompts
    prompt_to_use = random.choice(prompts)

    # generate N different questions for N question prompts
    questions = [i for i in prompts]
    for p in prompts:
        # choose a random topic
        topic_temp = random.choice(question_policy_map[topic])
        # append to question
        questions.append(fstr(p, x=topic_temp))

    specific_topic = random.choice(question_policy_map[topic])
    prompt = fstr(prompt_to_use, x=specific_topic)

    text = ' '.join(question_policy_map[topic])
    text += ' Australia'  # to make it more relevant
    if sentiment: text += random.choice(Sentiments[sentiment])

    # autocomplete full text
    text = gen_blog_pipeline(text)

    # generate answers
    # for each question in questions
    possible_answers = []
    for q in questions:
        ans = nlp(question=q, context=text)
        possible_answers.append(ans)

    possible_answers = reduce_nlp_answers(possible_answers)
    # remove duplicates
    possible_answers = list(dict.fromkeys(possible_answers))

    question = f"{prompt}"
    return question, possible_answers, "dropdown"


def gen_checkbox_question(policy_type, sentiment=None):
    topic = policy_type

    prompts = question_prompts
    prompt_to_use = random.choice(prompts)

    # generate N different questions for N question prompts
    questions = [i for i in prompts]
    for p in prompts:
        # choose a random topic
        topic_temp = random.choice(question_policy_map[topic])
        # append to question
        questions.append(fstr(p, x=topic_temp))

    specific_topic = random.choice(question_policy_map[topic])
    prompt = fstr(prompt_to_use, x=specific_topic)

    text = ' '.join(question_policy_map[topic])
    text += ' Australia'  # to make it more relevant
    if sentiment: text += random.choice(Sentiments[sentiment])

    # autocomplete full text
    text = gen_blog_pipeline(text)

    # generate answers
    # for each question in questions
    possible_answers = []
    for q in questions:
        ans = nlp(question=q, context=text)
        possible_answers.append(ans)

    possible_answers = reduce_nlp_answers(possible_answers)
    # remove duplicates
    possible_answers = list(dict.fromkeys(possible_answers))

    question = f"{prompt}"
    return question, possible_answers, "checkbox"


def gen_scale_question(policy_type):
    '''
    Scale of 1-5 or 1-10. Usually the more positive the answer, the more in favor they are of the policy type implementation.
    '''
    topic = policy_type
    # concat all synonyms
    text = ' '.join(question_policy_map[topic])
    text += ' Australia'  # to make it more relevant
    prompt = random.choice(question_prompts)
    specific_topic = random.choice(question_policy_map[topic])
    prompt = fstr(prompt, x=specific_topic)

    upper = random.choice([5, 10])
    possible_answers = list(range(1, upper+1))
    question = f"On a scale of 1 to {upper}, {prompt}"

    # return the question and stringed list of possible answers
    return question, possible_answers, "scale"


def gen_shortanswer_question(policy_type):
    '''
    Used for basic sentiment analysis -> e.g. hate, love, like against a specific policy topic.
    '''
    topic = policy_type
    text = ' '.join(question_policy_map[topic])
    prompt = random.choice(question_prompts)
    specific_topic = random.choice(question_policy_map[topic])
    prompt = fstr(prompt, x=specific_topic)

    question = f"{prompt}"
    possible_answers = "any"
    return question, possible_answers, "short_answer"


def gen_question(policy_type):
    # Note: any underscores become a space

    policy_type = policy_type.replace('_', ' ')
    # choose a random poll type, then generate it
    poll_types = [gen_multichoice_question, gen_shortanswer_question,
                  gen_scale_question, gen_checkbox_question, gen_dropdown_question]
    chosen_gen = random.choice(poll_types)

    return chosen_gen(policy_type)


if __name__ == '__main__':
    res = gen_question('infrastructure')
    print(res)
    res = gen_question('science')
    print(res)
    res = gen_question('health')
    print(res)
    res = gen_question('foreign relations')
    print(res)
    res = gen_question('foreign trade')
    print(res)
    res = gen_question('education')
    print(res)
    res = gen_question('lifestyle')
    print(res)
    res = gen_question('community')
    print(res)
