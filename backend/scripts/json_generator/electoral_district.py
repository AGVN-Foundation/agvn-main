import random
import json
from faker import Faker

fake = Faker('en-AU')

result = []

for i in range(0, 10):
  postcodes = []
  for j in range (0, 5):
    postcodes.append(fake.postcode())
  electro_distrct = {
    "electroate_id": i,
    "postcodes": postcodes,
    'council_members': random.randint(1, 10)
  }
  result.append(electro_distrct)

with open('sample_elec.json', 'w') as f:
  data = json.dump(result, f, indent=2)