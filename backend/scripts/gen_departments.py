import random
import pandas as pd
import string
from functools import reduce
from _aux import gen_strings


def gen_departments(n):
    '''
    Generate N departments
    Return -> tuple(list(int), list(int), list(str))
    '''
    type = [random.randint(1, 17) for _ in range(n)]
    # right now only two departments exist
    departments = [random.randint(1, 2) for _ in range(n)]
    levels = [random.randint(1, 3) for _ in range(n)]
    descriptions = []
    for _ in range(n):
        description = random.choices(string.ascii_lowercase, k=20)
        descriptions.append(reduce(lambda x, y: x+y, description))

    df = pd.DataFrame()
    df['type'] = type
    df['department'] = departments
    df['description'] = descriptions
    df['levels'] = levels

    df.to_csv('generated_data/departments.csv')


def gen_lower_deps():
    # Read from departments and randomly assign the values
    all_departments = pd.read_csv('generated_data/departments.csv')['id']
    # total lower departments = 434
    n_lower = 434
    # choose department ids
    department_ids = random.choices(all_departments, k=434)

    states = ["NSW", "VIC", "NT", "TAS", "QLD", "WA", "SA", "ACT"]

    state_departments = pd.DataFrame()
    state_ids = []
    state_names = []

    # assign 25 departments
    for i in range(25):
        state_id = random.choice(department_ids)
        department_ids.remove(state_id)
        state_ids.append(state_id)
        state_name = random.choice(states)
        state_names.append(state_name)

    state_departments['id'] = state_ids
    state_departments['state'] = state_names

    state_departments.to_csv(
        'generated_data/state_departments.csv', index=False)

    # generate 409 electoral districts
    electoral_districts = gen_strings(n=409, max_gen=15)

    local_ids = []
    local_names = []
    local_departments = pd.DataFrame()
    for e in electoral_districts:
        local_id = random.choice(department_ids)
        department_ids.remove(local_id)
        local_ids.append(local_id)
        local_name = random.choice(electoral_districts)
        local_names.append(local_name)

    local_departments['id'] = local_ids
    local_departments['electoral_district'] = electoral_districts

    local_departments.to_csv(
        'generated_data/local_departments.csv', index=False)


if __name__ == '__main__':
    # gen_departments(600)
    gen_lower_deps()
