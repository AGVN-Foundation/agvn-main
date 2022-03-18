import random
from numpy.random import rand
import pandas as pd
from functools import reduce


def gen_votes(n=10000):
    '''
    Gen N votes for a specific election
    @n 90-95% of the voter population
    '''
    user_ids = pd.read_csv('generated_data/users.csv')['user_id']
    elections = pd.read_csv('generated_data/elections.csv')
    initiatives = pd.read_csv('generated_data/initiatives.csv')
    years = elections['year']

    # sort the initiatives in order of election
    initiatives = initiatives['initiative'].sort_values(by=['election'])

    # store votes
    initiative_votes = []

    # generate 8000-n votes, initiative choices randomly selected from users
    # loop by election years
    for year, current_election_initiatives in years, initiatives:

        n_votes_year = random.randint(8000, n)
        users_voted = random.choices(user_ids, k=n_votes_year)

        # for each user, generate a random initiative array for this election
        current_election_voter_choices = []
        for user in users_voted:
            user_election = random.choices(
                current_election_initiatives, k=len(current_election_initiatives))
            # convert list to string and reduce to a single string
            user_election = list(map(lambda x: str(x), user_election))
            user_election_str = reduce(lambda x, y: x+y, user_election)
            current_election_voter_choices.append(user_election_str)

        initiative_votes += current_election_voter_choices

    df = pd.DataFrame()
    df['election'] = years
    df['user_id'] = user_ids
    df['initiative'] = initiative_votes

    df.to_csv('generated_data/votes.csv')


def gen_elections(n=100):
    '''
    Gen N elections
    @n around 100
    '''
    base_election_year = 2000
    election_cycle = 3
    election_years = [base_election_year + i*election_cycle for i in range(n)]
    election_months = [random.randint(1, 12) for _ in range(n)]

    df = pd.DataFrame()
    df['election_year'] = election_years
    df['election_month'] = election_months

    df.to_csv('generated_data/elections.csv', index=False)


def gen_initiatives():
    '''
    Generate 7-15 initiatives for each election
    '''
    elections = pd.read_csv('generated_data/elections.csv')
    all_initiatives = []
    election_years = []
    all_policy_weights = []

    for election in elections:
        n_generate = random.randint(7, 15)
        initiatives = [i for i in range(n_generate)]
        all_initiatives += initiatives
        election_year = [election['year'] for _ in range(n_generate)]
        policy_weights = []

        for _ in range(n_generate):
            policy_weights.append([random.uniform(-2, 2)
                                  for _ in range(1, 18)])

        all_policy_weights += policy_weights
        election_years += election_year

    df = pd.DataFrame()
    df['initiative'] = initiatives
    df['election'] = election_years
    df['policy_type_weights'] = all_policy_weights
    df.to_csv('generated_data/initiatives.csv')


if __name__ == '__main__':
    gen_elections(100)
    gen_initiatives()
