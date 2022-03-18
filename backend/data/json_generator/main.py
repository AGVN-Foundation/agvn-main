import json
import random
import uuid
from faker import Faker

education_levels = ['Certificate I', 'Certificate II', 'Certificate III', 'Certificate  IV', 'Diploma', 'Advanced Diploma',
                    'Associate Degree', 'Bachelor Degree', 'Bachelor Honours', 'Graduate Certificate', 'Graduate Diploma', 'Masters Degree', 'Doctoral Degree']

with open('sample_elec.json', 'r') as f:
    elec = json.load(f)

sex = [1, 2]

result = []

fake = Faker('en-AU')

for i in range(0, 500):

    uid = int(str(uuid.uuid4().fields[-1])[:10])
    gender = random.choice(sex)
    if gender == 1:
        name = fake.name_male()
    else:
        name = fake.name_female()
    age = random.randint(0, 150)
    edu = random.choice(education_levels)
    job = fake.job()
    electro = random.choice(elec)
    postcode = random.choice(electro['postcodes'])
    address = fake.building_number() + ' ' + fake.street_name() + ' ' + \
        fake.city() + ', ' + fake.state_abbr()
    driver_license = fake.ean(length=8)
    medicare = fake.numerify('##########')
    data = {
        'u_id': uid,
        'legal_name': name,
        'age': age,
        'sex': gender,
        'education_level': edu,
        'occupation': {
            'u_id': uid,
            'position': job,
            'ranking': random.randint(1, 5)
        },
        'family': [],
        'residence': {
            'country_id': 0,
            'address': address,
            'postcode': postcode,
            'electroal_district': electro['electroate_id']
        },
        'background': [0],
        'interests': [],
        'skills': [],
        'contribution': 0,
        'poll': [],
        'vote': [],
        'driver_license': driver_license,
        'medicare_number': medicare
    }
    result.append(data)

with open('sample_user.json', 'w') as f:
    data = json.dump(result, f, indent=2)
