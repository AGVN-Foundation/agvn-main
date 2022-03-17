import pytest
from ..models.DBConnection import DBConnection


def test_db_connection():
    '''
    Tests if connection to AGVN db works by checking it doesn't raises a
    ConnectionError.
    '''
    try:
        conn = DBConnection.Instance()
    except ConnectionError as e:
        pytest.fail()
