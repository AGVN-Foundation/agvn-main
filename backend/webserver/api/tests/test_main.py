"""
Test the main functionalities of the server
Includes:
    Login
    Registration
    Model methods
"""
import random
from hypothesis import given, strategies as st
from ..models import *
import pytest
from django.db import transaction, DatabaseError

def test_sanity():
    assert 1 == 1
