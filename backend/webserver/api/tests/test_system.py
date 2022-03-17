'''
    POST, GET, PUT requests to api endpoints
    /api/v1/login, register, polls, vote, initiatives, contribution benefits, chatbot
    
    NOTE: The way testing should be done is as follows:
    - first few tests should be hardcoded and ensure sanity and basic methods are working
    - next tests should be edge cases that are property based
    
    Extension: write some property based tests after the basic ones
'''
import requests
import pytest
from hypothesis import given, strategies as st

API_URL = 'http://localhost:8000/api/v1/'


def test_sanity_system():
    # with pytest.raises() <- use with expected exceptions on negative testing
    res = requests.get(API_URL+'/bad_route')
    assert res.status_code == 404


def test_register():
    '''
        Tests if user can be successfuly registered.
    '''
    # assume user with medicare '0123456789' and license 'abcd1234' exists
    payload = {'email': 'email@email.com',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': 'abcd1234'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 201:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token != None

def test_register_invalid_email():
    '''
        Tests to insure a user cannot be created if email is of an invalid type.
        e.g not example@domain.com
    '''
    payload = {'email': 'invalidemail:)',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': 'abcd1234'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()
    
    token = res.json()["token"]
    assert token == None

def test_register_same_email():
    '''
        Test to ensure users cannot not register with an already registered email.
    '''
    payload = {'email': 'email@email.com',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': 'abcd1234'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 201:
        print(res.reason)
        pytest.fail()

    # Check if first user with email@email.com successfully registers
    token = res.json()["token"]
    assert token != None

    payload = {'email': 'email@email.com',
               'password': 'password',
               'medicare': '9876543210',
               'driver_license': '1234abcd'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    # Check if second user with email@email.com unsuccessfully registers
    token = res.json()["token"]
    assert token == None

def test_register_same_details():
    '''
        A user cannot register with the same details as an already registered 
        user details.
    '''
    payload = {'email': 'email@email.com',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': 'abcd1234'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 201:
        print(res.reason)
        pytest.fail()

    # Check if first user with email@email.com successfully registers
    token = res.json()["token"]
    assert token != None

    payload = {'email': 'email2@email.com',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': 'abcd1234'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    # Check if second user with email2@email.com unsuccessfully registers
    token = res.json()["token"]
    assert token == None

def test_register_different_values():
    '''
        Test to ensure users cannot register with details from two different
        voter details.
    '''
    payload = {'email': 'email2@email.com',
               'password': 'password',
               'medicare': '0123456789',
               'driver_license': '1234abcd'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token == None

def test_register_missing_details():
    '''
        Test to ensure you cannot register with details that are not in the
        database.
    '''
    payload = {'email': 'email2@email.com',
               'password': 'password',
               'medicare': '1234512345',
               'driver_license': '12345678'}
    res = requests.post(API_URL+'register/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token == None

def test_login():
    '''
        Test if sucessful login.
    '''

    payload = {'email': 'example@email.com',
               'password': 'password'}
    res = requests.post(API_URL+'login/', data=payload)

    if res.status_code != 201:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token != None

def test_login_incorrect_email():
    '''
        Test to ensure a user cannot login with a non-existent email.
    '''
    payload = {'email': 'exampleghedaszhbtimc@email.com',
               'password': 'password'}
    res = requests.post(API_URL+'login/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token == None

def test_login_incorrect_passsword():
    '''
        Test to ensure a user cannot login with wrong password.
    '''

    payload = {'email': 'example@email.com',
               'password': 'password1'}
    res = requests.post(API_URL+'login/', data=payload)

    if res.status_code != 400:
        print(res.reason)
        pytest.fail()

    token = res.json()["token"]
    assert token == None