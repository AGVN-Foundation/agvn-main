import requests
import pytest

DOMAIN = 'http://localhost:1337/'
MSG_URL = DOMAIN + 'message/'


# @pytest.fixture
# def startup():
#     '''
#     Start up the server
#     '''
#     run_server()


def test_get_root():
    res = requests.get(DOMAIN, data={"message": "Hi"})
    assert res.status_code == 200
    assert res.json()['AGVN'] == "ChatbotTM"


def test_send_message():
    res = requests.get(MSG_URL + '?message=Hi')
    assert res.status_code == 200
    reply = res.json()['message']
    assert type(reply) is str
    assert len(reply) > 0


def test_send_message_bad():
    res = requests.get(MSG_URL + '?message=21r512hfkE!))nni0we')
    reply = res.json()['message']
    assert "I do not understand" in reply
