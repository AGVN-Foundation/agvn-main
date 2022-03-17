"""
Negative testing
Expect bad output on bad input
"""
from hypothesis import given, strategies as st
import pytest
from ..models import Voter, Poll, Vote, ContributionBenefits


@pytest.mark.xfail
def test_neg_basic():
    assert 1 != 1 and "cook" != "cook" and [] != []


@pytest.mark.xfail
def test_voter_initialization():
    voter = Voter()


@pytest.mark.xfail
def test_poll_initialization():
    poll = Poll()


@pytest.mark.xfail
def test_vote_initialization():
    vote = Vote()


@pytest.mark.xfail
def test_contribution_benefits_initialization():
    contribution_benefits = ContributionBenefits()

