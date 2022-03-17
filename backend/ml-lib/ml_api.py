# 1. Read polling data
# 2. Read voting data
# 3. Read all user data
# 4. Predict where users will be on the political spectrum -> clustering
# 5. Predict which values to set for each policy type -> deep reinforcement learning
# 6. Generate polls
import random
import json

import torch
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from datetime import date

from sentiment_analysis.model import NeuralNet
from sentiment_analysis.nltk_utils import bag_of_words, tokenize
from _aux import PolicyType, PollType, InitiativeType
from _aux import conservative_values, progressive, libertarian_values, activist, left_libertarian, social_democratic, statism, authoritarian


class sentimentNN(object):

    model = None
    all_words = None
    device = None
    tags = None

    def __init__(self):

        if sentimentNN.model is None:
            sentimentNN.device = torch.device(
                'cuda' if torch.cuda.is_available() else 'cpu')

            FILE = "sentiment_analysis/data.pth"
            data = torch.load(FILE, map_location=sentimentNN.device)

            input_size = data["input_size"]
            hidden_size = data["hidden_size"]
            output_size = data["output_size"]
            sentimentNN.all_words = data['all_words']
            sentimentNN.tags = data['ratings']
            model_state = data["model_state"]

            sentimentNN.model = NeuralNet(
                input_size, hidden_size, output_size).to(sentimentNN.device)
            sentimentNN.model.load_state_dict(model_state)
            sentimentNN.model.eval()

    def sentiment(self, sentence):

        if sentimentNN.model is None:
            return 0

        sentence = tokenize(sentence)
        X = bag_of_words(sentence, sentimentNN.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(sentimentNN.device)

        output = sentimentNN.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = sentimentNN.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        sentiment = sum(probs[0][i]*(i+1) for i in range(0, 5)) - 3
        return sentiment


def hyperml(q_id, results):
    '''
    Runs the pipeline
    '''
    p = process_polling_data(q_id)
    initiatives = predict_initiatives()
    initialise_voters()
    w = weighted_sum_method(results)

    return p, initiatives, w


def process_polling_data(q_id, debug=False):
    '''
        Algorithm that processes a poll results given a poll id and returns a sentiment
    '''

    poll_results = pd.read_csv("../scripts/generated_data/poll_results.csv")
    polls = pd.read_csv("../scripts/generated_data/polls.csv", index_col=0)
    # drop all data no equal to it.
    poll_results = poll_results[poll_results.q_id == q_id]
    results = 0

    q_type = int(polls.type.iloc[q_id])

    if debug:
        print(q_type)
        print(poll_results)

    if q_type == PollType.SCALE:

        min_scale = float(polls.iloc[q_id].possible_answers.split(',')[0])
        max_scale = float(polls.iloc[q_id].possible_answers.split(',')[-1])
        results = poll_results.answers.astype(int).mean()
        # scale between 0 & 1 and then multiply by 4 and minus -2, to make it between -2 & 2

        if debug:
            print(f'min scale: {min_scale}, max scale: {max_scale}')
            print(f'results: {results}')

        results = (results-min_scale)/(max_scale-min_scale) * 4 - 2

    elif q_type == PollType.MULTI_CHOICE or q_type == PollType.DROP_DOWN:
        # questions in order from highest to lowest
        answers = polls.iloc[q_id].possible_answers.split(',')
        scaling = len(answers)-1

        for i in range(len(answers)):
            poll_results = poll_results.replace(
                answers[i], (scaling-i)/scaling)

        results = poll_results.answers.astype(float).mean()

        if debug:
            print(poll_results)
            print(f'results: {results}')

    elif q_type == PollType.SHORT_ANSWER:
        # loop through each one and find sentiment analysis
        total_responses = poll_results.shape[0]
        for i in range(total_responses):
            # assumes result is returned between -2 & 2
            model = sentimentNN()
            response = poll_results.answers.iloc[i]
            sentiment = model.sentiment(response)
            results += sentiment

            if debug:
                print(f'response: {response}')
                print(f'sentiment: {sentiment}')

        results /= total_responses

    elif q_type == PollType.CHECK_BOX:

        # Top half of CheckBox are positive
        answers = polls.iloc[q_id].possible_answers.split(',')
        n = len(answers)

        if n % 2 == 0:
            for i in range(n):
                if 0 <= i and i < n/2:
                    poll_results = poll_results.replace(answers[i], 2/(n/2))
                else:
                    poll_results = poll_results.replace(answers[i], -2/(n/2))
        else:
            for i in range(n):
                if 0 <= i and i < n//2:
                    poll_results = poll_results.replace(answers[i], 2/(n/2))
                elif i == n//2:
                    poll_results = poll_results.replace(answers[i], 0)
                else:
                    poll_results = poll_results.replace(answers[i], -2/(n/2))

        results = poll_results.answers.astype(float).mean()

    else:
        results = 0

    if abs(results) <= 2:
        return results
    else:
        raise ValueError(
            f"Results were {results} and not between -2 and 2, something went wrong.")


def predict_initiatives():
    '''
    Generate initiatives based on user political interests

    PART 1:
        - cluster users together based on their whole data
        - form a set of policy weights for each cluster
        - generate initiatives based on polling data.

    PART 2: Extension
        - define a similiarity function between weights and 'sentiments'
    '''
    voter_predictions = pd.read_csv('initiative_clusters.csv')

    total_sentiment = np.zeros((17,), dtype=np.float32)

    initiative_weights = []

    for i in range(1, 9):
        init = voter_predictions[voter_predictions.initiative_type == i].reset_index(
        )
        init_sentiment = np.zeros((17,), dtype=np.float32)

        # if an initiative has no voters do not consider them in picking the best one
        if init.shape[0] == 0:
            continue

        for j in range(init.shape[0]):
            policy_interests = np.fromstring(init.policy_interests.iloc[j].replace(
                '\n', '').strip('[]'), dtype=np.float32, sep=' ')
            init_sentiment += policy_interests
            total_sentiment += policy_interests

        init_sentiment /= init.shape[0]

        initiative_weights.append((i, init_sentiment))

        # add anything here

    total_sentiment /= voter_predictions.shape[0]

    print(f'population weighting: {total_sentiment}')

    from math import sqrt

    shortest_dist = np.inf
    # In the rare case multiple initiatives have the same value
    best_initiatives = [InitiativeType.PROGRESSIVE]

    for init, values in initiative_weights:

        euclid_dist = sqrt(
            np.sum((total_sentiment-values)*(total_sentiment-values)))

        print(
            f'initiative type: {init}, initiative weighting diff {euclid_dist}')
        #print(f'initiative values {values}')

        if euclid_dist < shortest_dist:
            shortest_dist = euclid_dist
            best_initiatives = [init]
        elif euclid_dist == shortest_dist:
            best_initiatives.append(init)

    from random import choice

    return choice(best_initiatives)


def initialise_voters():
    voters = pd.read_csv("../scripts/generated_data/voters.csv")

    voters.country = np.where(voters.country == 0, -1, voters.country)
    voters.country = np.where(voters.country > 0, 0, voters.country)
    voters.country = np.where(voters.country == -1, 1, voters.country)

    # education level is going to be a bug in the future if these strings change
    education_levels = {'Certificate 1': 1, 'Certificate 2': 2, 'Certificate 3': 3,
                        'Certificate 4': 4, 'Advanced Diploma': 6, 'Bachelor Degree': 7,
                        'Honors Degree': 8, 'Masters Degree': 9, 'Doctoral Degree': 10,
                        }

    for key, value in education_levels.items():
        voters.loc[voters.education.astype(str).str.contains(
            key, case=False), 'education'] = value

    voters.loc[voters.education.astype(str).str.contains(
        'Diploma', case=False), 'education'] = 5

    for i in range(voters.shape[0]):
        contribution = float(
            voters.contribution.iloc[i].strip('{}').split(',')[-1])
        voters.loc[i, 'contribution'] = contribution

    voters.sex = (voters.sex - voters.sex.min()) / \
        (voters.sex.max()-voters.sex.min())
    voters.education = (voters.education - voters.education.min()) / \
        (voters.education.max()-voters.education.min())
    voters.contribution = (voters.contribution - voters.contribution.min()) / \
        (voters.contribution.max()-voters.contribution.min())
    voters.occupation = (voters.occupation - voters.occupation.min()) / \
        (voters.occupation.max()-voters.occupation.min())
    voters.age = (voters.age - voters.age.min()) / \
        (voters.age.max()-voters.age.min())
    voters.income = (voters.income - voters.income.min()) / \
        (voters.income.max()-voters.income.min())
    voters.occupation_rank = (voters.occupation_rank - voters.occupation_rank.min())/(
        voters.occupation_rank.max()-voters.occupation_rank.min())
    voters.n_family = (voters.occupation_rank - voters.occupation_rank.min()) / \
        (voters.occupation_rank.max()-voters.occupation_rank.min())

    from math import sqrt

    clusters = pd.DataFrame(
        columns=['user_id', 'initiative_type', 'policy_interests'])

    global conservative_values, progressive, libertarian_values, activist, left_libertarian, social_democratic, statism, authoritarian

    initiative_weights = [(libertarian_values, InitiativeType.LIBERTARIAN),
                          (conservative_values, InitiativeType.CONSERVATIVE),
                          (activist, InitiativeType.ACTIVIST),
                          (left_libertarian, InitiativeType.LEFT_LIBERTARIAN),
                          (progressive, InitiativeType.PROGRESSIVE),
                          (social_democratic, InitiativeType.SOCIAL_DEMOCRATIC),
                          (statism, InitiativeType.STATIST),
                          (authoritarian, InitiativeType.AUTHORITARIAN)
                          ]

    for i in range(voters.shape[0]):
        # to do update
        political_interests = initialise_voter_polictical_interests(
            voters.iloc[i])

        voter_id = voters.id.iloc[i]

        shortest_dist = np.inf
        best_initiative = InitiativeType.PROGRESSIVE

        for values, initiative_type in initiative_weights:
            euclid_dist = 0

            for j in range(len(political_interests)):
                euclid_dist += (values[j] - political_interests[j])**2

            euclid_dist = sqrt(euclid_dist)

            if euclid_dist < shortest_dist:
                shortest_dist = euclid_dist
                best_initiative = initiative_type

        clusters.loc[i] = [voter_id, best_initiative,
                           np.array(political_interests, dtype=object)]

        # UPDATE HERE

    clusters.to_csv('initiative_clusters.csv', index=False)


def initialise_voter_polictical_interests(voter):

    scaling_policy_taxation = (4*(3*(1-voter.income)+2*voter.education+3*(1-voter.income)*(voter.education)
                                  + 2*voter.contribution+1*voter.occupation_rank) + 3 * (3*voter.country)
                               + (1-voter.sex))/(4*(3+2+3+2+1)+3*(3)+(1))

    scaling_policy_lifestyle_culture = (4*((1-voter.income)+(1-voter.education)+(1-voter.income)*(1-voter.education)
                                           + 2*voter.contribution)
                                        + 3*(voter.n_family + 3*(1-voter.age))
                                        )/(4*(1+1+1+2)+3*(1+3))

    scaling_policy_community = (4*((1-voter.income)+3*(voter.education)+(1-voter.income)*(voter.education)
                                   + 3*voter.contribution+(1-voter.occupation_rank))
                                + 3*(3*voter.n_family + 2*(1-voter.age))
                                )/(4*(1+3+1+3+1)+3*(3+2))

    scaling_policy_infrastructure = 0.1 + 0.9 * \
        ((4*(3*(1-voter.income)+2*(1-voter.occupation_rank)) +
         3*(3*voter.n_family))/(4*(3+2)+3*(3)))

    scaling_policy_foreign_relations = 0.05 + 0.95 * (4*((voter.education)
                                                         + 3*voter.contribution+(voter.occupation_rank))
                                                      + 3*(voter.country)
                                                      )/(4*(1+3+1)+3*(1))

    scaling_policy_health = 0.2 + 0.8 * (4*(3*(1-voter.income)+2*(voter.education)+(1-voter.income)*(voter.education)
                                            + 3*voter.contribution+3*(1-voter.occupation_rank))
                                         + 3*(3*voter.n_family + 2*(voter.age))
                                         )/(4*(3+2+1+3+3)+3*(3+2))

    scaling_policy_education_employment = (4*(3*(1-voter.income)+(voter.education)
                                           + voter.contribution+3*(1-voter.occupation_rank))
                                           + 3*(voter.n_family + (1-voter.age))
                                           )/(4*(3+1+1+3)+3*(1+1))

    scaling_policy_national_security = 0.2 + 0.8 * (4*(voter.contribution+voter.education)
                                                    + 3*(voter.n_family +
                                                         3*(voter.country))
                                                    )/(4*(1+1) + 3*(1+3))

    scaling_policy_safety = 0.1 + 0.9 * (4*(2*(1-4*(voter.income-0.5)**2)+(voter.education)
                                            + voter.contribution)
                                         + 3*(voter.n_family +
                                              3*(voter.country))
                                         )/(4*(2+1+1)+3*(1+3))

    scaling_policy_industry = (4*((1-voter.income)+3*(1-voter.education)+(1-voter.income)*(1-voter.education)
                                  + (1-voter.occupation_rank))
                               + 3*(voter.n_family + (voter.age) +
                                    2*(voter.country))
                               + (3*(1-voter.sex))
                               )/(4*(1+3+1+3+1)+3*(1+1+2)+(3))

    scaling_policy_science_technology = (4*((voter.income)+3*(voter.education)+voter.contribution
                                            + (1-4*(voter.occupation_rank-0.5)**2))
                                         + 3*((1-voter.age))
                                         + ((1-voter.sex))
                                         )/(4*(1+3+1+1)+3*(1)+(1))

    scaling_policy_environment = (4*(2*(1-voter.income)+2*(voter.education)+3*(1-voter.income)*(voter.education)
                                     + 3*voter.contribution+(1-voter.occupation_rank))
                                  + 3*(2*(1-voter.age))
                                  + (2*(voter.sex)))/(4*(2+2+3+3+1)+3*(2)+(2))

    scaling_policy_energy = (4*(2*(voter.income)+2*(1-voter.education)+1*(voter.income)*(1-voter.education)
                                + (4*(voter.occupation_rank-0.5)**2))
                             + 3*((voter.age))
                             + ((1-voter.sex)))/(4*(2+2+1+1)+3*(1)+(1))

    scaling_policy_assets = (4*(3*(voter.income)+2*(1-voter.education)+1*(voter.income)*(voter.education)
                                + 3*(voter.occupation_rank))
                             + 3*((voter.age))
                             + (3*(1-voter.sex)))/(4*(3+2+1+3)+3*(1)+(3))

    scaling_policy_economy = (4*(3*(voter.income)
                                 + 3*(voter.occupation_rank))
                              + ((1-voter.sex)))/(4*(3+3)+3*(1)+(1))

    scaling_policy_foreign_trade = (4*(3*(voter.income)+2*(1-voter.education)+1*(voter.income)*(voter.education)
                                       + 3*(voter.occupation_rank))
                                    + 3*((1-voter.country))
                                    + ((1-voter.sex)))/(4*(3+2+1+3)+3*(1)+(1))

    scaling_policy_natural_resources = (4*((1-voter.income)+3*(1-voter.education)+(1-voter.income)*(1-voter.education)
                                           + (4*(voter.occupation_rank-0.5)**2))
                                        + 3*(2*(voter.age) + 3*(voter.country))
                                        + (3*(1-voter.sex))
                                        )/(4*(1+3+1+3+1)+3*(2+3)+(3))

    voter_political_interests = [
        scaling_policy_taxation, scaling_policy_lifestyle_culture,
        scaling_policy_community, scaling_policy_infrastructure,
        scaling_policy_foreign_relations, scaling_policy_health,
        scaling_policy_education_employment, scaling_policy_national_security,
        scaling_policy_safety, scaling_policy_industry,
        scaling_policy_science_technology, scaling_policy_environment,
        scaling_policy_energy, scaling_policy_assets,
        scaling_policy_economy, scaling_policy_foreign_trade,
        scaling_policy_natural_resources
    ]

    for i in range(len(voter_political_interests)):
        voter_political_interests[i] = 4*voter_political_interests[i] - 2

        # To handle human error

        if voter_political_interests[i] > 2:
            voter_political_interests[i] = 2
        elif voter_political_interests[i] < -2:
            voter_political_interests[i] = -2

    return voter_political_interests


def weighted_sum_method(results):
    '''
        @params: results is a list containing tuples of polling results & date
        ordered from latest to oldest
        [(Rn,Dn),...,(R,D)]
    '''
    if len(results) == 0:
        return 0

    _t, latest_date = results[0]

    if len(results) == 1:
        return _t

    total_days = 0

    for _x, poll_date in results:
        total_days += (latest_date-poll_date).days

    initiative = 0

    for result, poll_date in results:
        initiative = (total_days-(latest_date-poll_date).days)*result

    initiative /= 2*total_days

    return initiative


def gen_poll(prompt, topic: int, max_length=50):
    '''
    NOTE: might just generate poll manually.
    Generate a poll based on sentiment over past 30 days
    Extension: consider how voter data changed over past 30 days

    In - prompt, STR containing policy topic and sentiment
       - max_length, INT max length of poll question to generate
       - topic, ENUM policy type

    The prompt should be a string
        e.g. "how do you think about {topic}"
    These prompts should be randomly generated


    GPT will autocomplete the question prompt and the topic prompt with 20-30 more chars
    '''
    from transformers import pipeline, set_seed
    generator = pipeline('text-generation', model='gpt2')
    set_seed(1000)
    question = generator(prompt, max_length=max_length,
                         num_return_sequences=1)[0]

    return question
