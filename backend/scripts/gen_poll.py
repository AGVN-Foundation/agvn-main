import random
import pandas as pd
from datetime import datetime
from _aux import gen_strings, DEBUG_OUT
from functools import reduce


def fstr(template, **kwargs):
    # CREDIT kadee -> https://stackoverflow.com/questions/54351740/how-can-i-use-f-string-with-a-variable-not-with-a-string-literal
    # for providing fstr() parameterization
    return eval(f"f'{template}'", kwargs)


question_type = ['economics', 'lifestyle and culture', 'community', 'infrastructure', 'international', 'health',
                 'education and employment', 'national security', 'safety', 'industry', 'science and technology', 'environment']
question_policy = ['taxation', 'lifestyle', 'community', 'infrastructure', 'foreign relations', 'health', 'education and employment',
                   'national security', 'safety', 'industry', 'science and technology', 'environment', 'energy', 'assets', 'economy', 'foreign trade', 'natural resources']

# words should be unique. They dont necessarily have to, since we can loop through each policy type and reweigh policies with similar words
# choose a policy type, then choose one of the following from the list
# based on the amount of matching, weigh the policy higher. Based on the sentiment strength, weigh it more strongly.
# Extension: for each sub word, give it a weight accordng to how relevant it is to the concept. Can just give specific values weights and weigh everything else the same.
question_policy_map = {
    'taxation': ['income', 'individualism', 'government control', 'fairness', 'income', 'salary', 'tired', 'taxes'],
    'lifestyle': ['life', 'living conditions', 'situation', 'home', 'way of living', 'happiness'],
    'community': ['neighborhood', 'public', 'home', ''],
    'infrastructure': ['public transport', 'public infrastructure', 'public utilities', 'housing', 'roads', 'rail', 'sanitation'],
    'foreign relations': ['geopolitics', 'public administration', 'international', 'competition', 'tariffs', 'sanctions', 'genocide', 'war', 'friendly'],
    'health': ['sanitation', 'illness', 'standard of living', 'hospitals', 'aged care', 'youth care', 'welfare'],
    'education and employment': ['schools', 'vocational training', 'productivity', 'higher education', 'universities', 'public schools', 'private schools', 'early education', 'training', 'employment', 'jobs', 'growth', 'salary', 'future'],
    'national security': ['security', 'safety', 'foreign', 'immigration', 'migration', 'invasion', 'defense', 'protection'],
    'safety': ['safety', 'welfare', 'protection', 'prevention', 'danger', 'industry safety', 'workplace safety'],
    'industry': ['industrial', 'manufacturing', 'production', 'construction', 'business', 'energy', 'labor', 'work', 'tradesmen', 'trade', 'profession'],
    'science and technology': ['science', 'physics', 'technology', 'reason', 'proof', 'advances', 'advancement', 'scientist', 'engineer', 'maths', 'profession', 'scientific method', 'innovation', 'invention', 'future', 'competition'],
    'environment': ['parks', 'waste'],
    'energy': ['natural', 'fossil fuels', 'renewable energy', 'green', 'sustainability', 'environment', 'growth', 'independence'],
    'assets': ['economy', 'budget', 'production'],
    'economy': ['economics', 'economy', 'jobs', 'growth', 'trade', 'interest rates'],
    'foreign trade': ['international', 'economy', 'tarrifs', 'exchange rates'],
    'natural resources': ['assets', 'renewable', 'sustainability'],
}

question_prompts = [r'What do you think about {x}', r'Do you like the idea of {x}', r'How much do you like about {x}',
                    r'If you would think about how {x} affects you', r'What impact does {x} have on you']


def reduce_strings(string_list):
    '''
    Reduce a list of strings into a single string
    '''
    DEBUG_OUT(f"string_list -> {string_list}")
    result = str(reduce(lambda x, y: str(x)+','+str(y), string_list))
    return result


def gen_polls(n=15):
    '''
    Generates n polls (questions) of a randomly chosen type
    '''
    def gen_scale_question():
        '''
        Generate question prompt and possible answers
        Assume frontend separates answers based on ',' comma
        '''
        upper = random.choice([5, 10])
        possible_answers = list(range(1, upper+1))
        return f"On a scale of 1 to {upper} on", reduce_strings(possible_answers)

    def gen_multichoice_question():
        # Answers: generate list of 4-5 random strings
        possible_answers = gen_strings(n=random.choice([4, 5]))
        return "Choose from one of the following on", reduce_strings(possible_answers)

    def gen_shortanswer_question():
        '''
        Basic sentiment analysis -> e.g. hate, love, like against a specific policy topic.
        '''
        # Answers: generate a longer, random string (100 chars)
        # Actually: just generate a null string and let frontend handle
        possible_answers = "any"
        return "Give a short answer about", possible_answers

    def gen_dropdown_question():
        # Answers: generate a list of 20-30 random strings
        possible_answers = gen_strings(
            n=random.choice(list(range(20, 31))), max_gen=25)
        return "Choose from the list of following on", reduce_strings(possible_answers)

    def gen_checkbox_question():
        # Answers: generate a list of 5-8 random strings
        n_gen = range(5, 8)
        possible_answers = gen_strings(
            n=random.choice(list(n_gen)), max_gen=40)
        return "Tick the boxes you agree with on", reduce_strings(possible_answers)

    def gen_question(question):
        prompt = random.choice(question_prompts)
        index = random.randint(0, 16)
        topic = question_policy[index]
        index_2 = random.randrange(0, len(question_policy_map[topic]))
        keyword = question_policy_map[topic][index_2]
        return question + ': ' + fstr(prompt, x=keyword), index, topic

    possible_questions = [gen_multichoice_question, gen_scale_question,
                          gen_shortanswer_question, gen_checkbox_question, gen_dropdown_question]

    questions = []
    possible_answers = []
    end_dates = []
    question_types = []
    subjects = []

    def gen_date():
        '''
        Generate dates from 2021-06-20
        Assume polls never end at 29-31
        '''
        year = random.randint(2021, 3000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return str(year) + '-' + str(month) + '-' + str(day)

    for _ in range(n):
        # Generate a random question
        index = random.randint(0, 4)
        question = possible_questions[index]()
        generated = gen_question(question[0])
        questions.append(generated[0])

        possible_answers.append(question[1])

        question_types.append(index+1)

        # Specify the poll topic
        subjects.append(generated[2])

        # Generate end date
        end_dates.append(gen_date())

    questions_df = pd.DataFrame()
    questions_df['question'] = questions
    questions_df['ongoing'] = [False for _ in range(n)]
    questions_df['type'] = question_types
    questions_df['end_dates'] = end_dates
    questions_df['possible_answers'] = possible_answers
    questions_df['subject'] = subjects

    questions_df.to_csv('generated_data/polls.csv')


def gen_poll_results(answers_per_q=3):
    '''
    Requires users.csv with 10,000 users
    Requires questions.csv with > 10 questions

    RN, generates 3 answers (polls) per question from 3 randomly chosen users
    Algorithm
        for all polls
            choose 3 users
            choose 3 random dates
            choose 3 random answers from list of possible answers
            append 3 users and stuff to list of poll results
    '''
    questions = pd.read_csv('generated_data/polls.csv')
    users = pd.read_csv('generated_data/users.csv')['user_id']
    q_ids = len(questions)  # not required
    n_users_per_question = 3
    voter_answers = []
    voters = []
    answered_questions = []
    date_answered = []

    # possible answers should be string separated by comma
    # if possible answer is null, then generate random string
    for i, possible_answers in enumerate(questions['possible_answers']):
        DEBUG_OUT(possible_answers)
        # get end_date for current poll
        current_end = questions['end_dates'][i]
        # convert to datetime
        current_end = datetime.strptime(current_end, '%Y-%m-%d')
        # generate an 'answered date' < end date within 1 month
        # if end date == jan, then skip back a year and do 12

        def get_timestamp():
            if current_end.month == 1:
                answered_date = datetime(
                    current_end.year-1, current_end.month, random.randint(1, 28))
            else:
                answered_date = datetime(
                    current_end.year, current_end.month-1, random.randint(1, 28))
            return answered_date.strftime("%Y-%m-%d")

        for j in range(n_users_per_question):
            date_answered.append(get_timestamp())

        chosen_users = random.choices(users, k=n_users_per_question)
        if possible_answers != None:
            # listfy the string separated by comma
            answers_list = possible_answers.split(',')
            chosen_answers = random.choices(
                answers_list, k=n_users_per_question)
        else:
            chosen_answers = gen_strings(n_users_per_question)
        voter_answers += chosen_answers
        voters += chosen_users
        answered_questions += [i] * n_users_per_question

    polls = pd.DataFrame()
    polls['q_id'] = answered_questions
    polls['user_id'] = voters
    polls['date_time'] = date_answered
    polls['answers'] = voter_answers

    polls.to_csv('generated_data/poll_results.csv', index=False)


if __name__ == '__main__':
    gen_poll_results()
