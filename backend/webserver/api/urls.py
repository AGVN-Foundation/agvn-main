from .models.ElectionResults import ElectionResults
from django.http.response import HttpResponse
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename="user")
router.register(r'voters', VoterDetail, basename="voter_details")
router.register(r'skills', SkillViewSet, basename="skills")
router.register(r'interests', InterestViewSet, basename="interests")
router.register(r'occupations', OccupationViewSet, basename="occupations")
router.register(r'residences', ResidenceViewSet, basename="residences")
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'votes', VoteView, basename="vote")
router.register(r'departments', DepartmentView, basename='departments')
router.register(r'poll-results', PollResultViewSet, basename='poll-results')
router.register(r'election', ElectionGenericView, basename='elections')
router.register(r'initiative', InitiativeGenericView, basename='initiatives')
router.register(r'sentiment', SentimentView, basename='sentiment')
router.register(r'policy', PolicyView, basename='policy')
router.register(r'elected-initiative', ElectedInitiativeView,
                basename='elected-initiative')
router.register(r'election-results', ElectionResultsView,
                basename='election-results')


urlpatterns = [
    path('', include(router.urls)),
    path('test', main),
    path('register', UserViewSet.as_view()),
    path('login', login),
    path('profile', get_userData),
    path('notifications/', notifications),
    path('change/password', change_password),
    path('user/interests', get_interests),
    path('user/interests/update', update_interests),
    path('user/skills', get_skills),
    path('user/skills/update', update_skills),
    path('results/', retrieve_results),
    path('do/election', ElectionView),
    path('gboost', do_gboost),
    path('initiatives', get_initiative),
    path('vote', vote),
    path('polls/submit', create_poll),
    path('end/election', end_election),
    path('offers', get_offers),
]
