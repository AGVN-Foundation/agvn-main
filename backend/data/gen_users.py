'''
    Generates 2x more voters than users. Have 10,000 voter details not registered.
    For tokens that are linked to users -> simply need to verify whether the token corresponds to the user.
    May need to delete extra terms like the 'b' in b'assa$as' which is generated from bcrypt, test first.
    Prob doesnt matter too much since we aren't logging in with these accounts.
'''

from uuid import uuid4
import random
import pandas as pd
import string
from functools import reduce
from hypergen import gen_strings, DEBUG_OUT
from hash import hash_password
from numpy.random import exponential
import numpy as np


def gen_user_id(n):
    '''
    Generate N user ids
    How it works:
        Statistically speaking, 2N randomly generated UUID4s should have >99.9999% chance of having N unique values.
    Return -> list(int)
    '''
    ids = [uuid4() for _ in range(2*n)]
    return list(set(ids))[:n]


def gen_voters(n=20000):
    '''
    Generate N voters
    Assumes that countries, occupations, etc. are generated beforehand.
    '''
    ids = pd.read_csv('generated_data/users.csv')

    first_names = pd.read_csv('sampledata/first_names.txt')
    last_names = pd.read_csv('sampledata/last_names.txt')
    first_names['First Name'] = list(
        map(lambda x: x+' ', first_names['First Name']))
    legal_names = first_names['First Name'] + last_names['Last Name']
    legal_names.dropna(inplace=True)
    legal_names = legal_names.iloc[:n]

    sex = [random.randint(1, 2) for _ in range(n)]

    medicares, licenses = [], []
    for _ in range(100*n):
        license = random.choices(string.ascii_letters+string.digits, k=8)
        licenses.append(reduce(lambda x, y: x+y, license))
        medicare = random.choices(string.ascii_letters+string.digits, k=10)
        medicares.append(reduce(lambda x, y: x+y, medicare))

    # take unique values only
    medicares = list(set(medicares))[:n]
    licenses = list(set(licenses))[:n]

    DEBUG_OUT(f"length of medicares -> {len(medicares)}")
    DEBUG_OUT(f"length of licenses -> {len(licenses)}")

    education = pd.read_csv('sampledata/sample_education_levels.txt')
    education = list(education['Education Level'])
    educations = random.choices(education, k=n)

    def get_countries(weight=0.7):
        '''
        Weighs Australia more. 
        NOTE: Assume index 0 is Australia -> do for gen uneditable details [country].

        Read in countries.csv and make it a list
        For each user, choose a country index
        '''
        countries = pd.read_csv('generated_data/countries.csv')
        n_countries = len(countries)
        user_countries = []

        for i in range(n):
            chance = random.randint(0, 10)
            if chance <= weight:
                user_countries.append(0)
            else:
                user_countries.append(random.randint(1, n_countries-1))

        return user_countries

    def get_residences():
        '''
        Extension: simulate peaks for some areas. Have 2 'main' postcode areas, e.g. 2000, 3000. This should be proportional to the actual population. Then just weigh the postcodes near 2000, 3000 more than others.

        Read in residences.csv and note the number of residences as n_residences
        For each user, choose a residence index
        '''
        residences = pd.read_csv('generated_data/residences.csv')
        n_residences = len(residences)
        user_residences = [random.randint(0, n_residences-1) for _ in range(n)]

        return user_residences

    def get_skills():
        '''
        Skills for each voter. 0-300.

        NOTE the following functions are basically the same and can be abstracted, though in the future we may change the models so good to keep them like so.
        '''
        skills = pd.read_csv('generated_data/skills.csv')
        n_skills = len(skills)

        user_skills = [random.randint(0, n_skills-1) for _ in range(n)]
        return user_skills

    def get_interests():
        '''
        Interests for each voter. 0-300
        '''
        interests = pd.read_csv('generated_data/interests.csv')
        n_interests = len(interests)

        user_interests = [random.randint(0, n_interests-1) for _ in range(n)]
        return user_interests

    def get_occupations():
        '''
        Occupations for each voter. 0-300
        '''
        occupations = pd.read_csv('generated_data/occupations.csv')
        n_occ = len(occupations)

        user_occupations = [random.randint(0, n_occ-1) for _ in range(n)]
        return user_occupations

    voters = pd.DataFrame()
    # Assign only half n users to voters
    k = int(n/2)
    ids_to_use = [np.nan] * k
    ids_to_use += list(ids['user_id'][:k])
    voters['id'] = [i for i in range(n)]
    voters['user_id'] = ids_to_use
    voters['legal_name'] = legal_names
    voters['sex'] = sex
    voters['driver_license'] = licenses
    voters['medicare'] = medicares
    voters['n_family'] = [random.randint(1,10) for _ in range(n)]
    voters['education_level'] = educations

    def gen_contributions():
        '''
        For n/2 voters that have registered
            Get a base contribution
            Generate 30 more ints by adding 1-100 each time
        '''
        contributions = []
        for _ in range(k):
            contribution_start = random.gauss(500, 50)
            last_30_day_contribution = [contribution_start]

            for j in range(29):
                current_day_contribution = last_30_day_contribution[j]
                next_contribution = current_day_contribution + \
                    exponential(scale=5)
                last_30_day_contribution.append(next_contribution)

            formatted_cont = str(last_30_day_contribution).replace('[', '{')
            formatted_cont = formatted_cont.replace(']', '}')

            contributions.append(formatted_cont)

        contributions += [0] * k
        return contributions

    voters['residence'] = get_residences()
    voters['country'] = get_countries()
    voters['current_occupation'] = get_occupations()
    voters['occupation_rank'] = [random.randint(0, 10) for _ in range(n)]
    voters['income'] = [random.gauss(70000, 10000) for _ in range(n)]
    voters['government_employee'] = [random.choices(
        [0, 1], [0.95, 0.01])[0] for _ in range(n)]
    
    voters['skills'] = get_skills()
    voters['interests'] = get_interests()

    # generate political interests
    def gen_political_interests():
        # turn lists into strings with {}
        all_political_interests = []
        for i in range(n):
            # generate a list[17] of interests
            political_interests = [random.uniform(-2, 2) for _ in range(17)]
            stringified_interests = str(political_interests)
            stringified_interests = stringified_interests.replace('[', '{')
            stringified_interests = stringified_interests.replace(']', '}')

            all_political_interests.append(stringified_interests)

        return all_political_interests

    voters['contributions'] = gen_contributions()
    voters['political_interest'] = gen_political_interests()

    # write out
    voters.to_csv('generated_data/voters.csv', index=True)


def gen_users(n=10000):
    def gen_email():
        email_gen = random.choices(
            string.ascii_letters+'_', k=random.randint(5, 20))
        email_first = reduce(lambda x, y: x+y, email_gen)
        # low level domain name name 5-10 characters
        domain_1 = random.choices(
            string.ascii_lowercase, k=random.randint(5, 10))
        domain_1 = reduce(lambda x, y: x+y, domain_1)
        domain_2 = random.choice(["com", "org", "info"])
        email = email_first + '@' + domain_1 + '.' + domain_2

        return email

    def gen_password():
        password = random.choices(
            string.ascii_letters, k=random.randint(6, 8))
        password += random.choices(
            string.digits, k=random.randint(2, 3))
        allowed_punctuation = '!#$%&()*+,-.:;<=>@[]^_~'
        password += random.choices(allowed_punctuation, k=random.randint(1, 3))
        random.shuffle(password)

        return reduce(lambda x, y: x+y, password)

    current = pd.DataFrame()
    current['user_id'] = gen_user_id(n)
    emails = [gen_email() for _ in range(100*n)]
    current['email'] = list(set(emails))[:n]
    raw_passwords = [gen_password() for _ in range(n)]
    passwords = []
    for i in range(n):
        passwords.append(hash_password(raw_passwords[i]))
        print(f"generated password {i}")
    current['password'] = passwords

    current.to_csv('generated_data/users.csv')


def gen_voter_details_editable():
    '''
    Functions to output data to csv.
    Editable by Voter -> Skills, Interests, Occupation, Residence
    :param user_ids: list of uuid4 - list(int)
    :param n: number of rows to generate - int
    '''
    def gen_skill(n=300):
        '''
        Generates skills and outputs to csv
        '''
        skills = pd.DataFrame()
        descriptions = gen_strings(n)
        skills['description'] = descriptions

        skills.to_csv('generated_data/skills.csv')

    def gen_interests(n=300):
        interests = pd.DataFrame()
        levels = [random.choice([1, 2, 3]) for _ in range(n)]
        descriptions = gen_strings(n)
        interests['description'] = descriptions

        interests.to_csv('generated_data/interests.csv')

    def gen_occupations(n=30*18):
        '''
        Statistically, randomly generated descriptions for the same type of occupation should be quite random
        '''
        occupations = pd.DataFrame()
        types = [random.choice(list(range(1, 19))) for _ in range(n)]
        descriptions = gen_strings(n)
        occupations['types'] = types
        occupations['description'] = descriptions

        occupations.to_csv('generated_data/occupations.csv')

    def gen_residences(places=5000):
        residences = pd.DataFrame()
        address = gen_strings(places, max_gen=50)
        suburb = gen_strings(places, max_gen=15)
        postcodes = [random.randint(1000, 9000) for _ in range(places)]
        residences['address'] = address
        residences['suburb'] = suburb
        residences['postcode'] = postcodes

        residences.to_csv('generated_data/residences.csv')

    gen_skill()
    gen_interests()
    gen_occupations()
    gen_residences()


def gen_voter_details_uneditable():
    '''
    Uneditable by Voter -> Background
    '''
    def gen_country(n=300):
        # generate 300 country names
        # for each of them, set friendly [0, 1] with 0.9 chance

        countries = pd.DataFrame()
        country_names = gen_strings(n, max_gen=56, lowercase=True)
        friendly = [random.choices([0, 1], weights=[0.9, 0.1])[0]
                    for _ in range(n)]
        country_names[0] = 'Australia'
        countries['country'] = country_names
        countries['friendly terms'] = friendly

        countries.to_csv('generated_data/countries.csv')

    gen_country()


if __name__ == '__main__':
    # user_ids = pd.read_csv('generated_data/users.csv')['user_id']
    # gen_voter_details_editable()
    # gen_voter_details_uneditable()
    gen_voters()
