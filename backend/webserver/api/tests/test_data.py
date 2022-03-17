"""
Test data in a newly created postgres database
How to test:
    1. create a new postgres database
    2. generate schema from output of python manage.py migrate
    3. create object instances succesfully
"""

from uuid import uuid4
from ..models import Occupation, Residence, Country
from ..models import Voter, User
from ..models import Skill, Interests
import pytest

pytestmark = [pytest.mark.django_db]


def test_basic():
    try:
        while True:
            # 128-bit user id, e.g. 10101010001001...
            id = uuid4()

            try:
                User.objects.get(user_id=id)
                print("Trying another ID")
            except User.DoesNotExist:
                break

        medicare = "0123456789"
        license = "abcd1234"

        user = User.objects.create(
            user_id=id, email="email@emai.com", hashed_password="greatest_password99&")

        user_id = user.user_id

        voter = Voter.objects.create(user_id=user_id, medicare=medicare, driver_license=license,
                                     legal_name="best name", sex=1, education_level="Bachelor of gender study", contribution=100)

        occ = Occupation.objects.create(user=user,
                                        position="Reddit lU L", description="full time twitter poster")
        res = Residence.objects.create(user=user,
                                       address="lamo", suburb="the place", postcode=2000, electoral_district="idk sydney or something")
        cty = Country.objects.create(user=user,
                                     country="Holy American Empire", friendly_terms=True)
        interest = Interests.objects.create(user=user,
                                            level_of_interest=10, description="S L E E P ON B E D")
        skill = Skill.objects.create(
            user=user, proficiency=1, description="gaming")

    except Exception as e:
        print("Error:", e)
        pytest.fail()
