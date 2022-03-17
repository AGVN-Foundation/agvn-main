from requests.api import get
from .models.Initiative import Initiative
from .models.Election import Election
from .models.PollResult import PollResult
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.User import User
from .models.Poll import Poll
from .models.Sentiment import Sentiment
from .serializers import *
from rest_framework import viewsets
from .models.Skill import Skill
from .models.ElectionResults import ElectionResults
from .models.Department import Department
from .models.Interests import Interests
from .models.Residence import Residence
from .models.Voter import Voter
from .models.Occupation import Occupation
from .models.Vote import Vote
from .serializers import DepartmentSerializer, InitiativeSerializer, PolicySerializer, JobOfferSerializer, JobPromotionSerializer
from .models.Education import _Education
from .models.Policy import Policy
from rest_framework.decorators import api_view
from .helper import *
from datetime import datetime, timedelta
import numpy as np


def main(request):
    return HttpResponse("<h1>Django Test</h1>")


class ElectionView(viewsets.ViewSet):
    '''
    Starting and finishing elections.

    GET -> returns an election if it is_active
    Else returns {'elections': ""} which renders "No elections at the moment"

    POST body -> {token, type: 'start|vote|end', ?votes}
    @start -> starts the election in the current day, current time. Sets end to 1 month later.
        checks all elections for any that is_active
        if not creates a new Election object and set to is_active
        tells ml-lib-server to generate new initiatives
        sets those initiatives to the current election

    Uses helper functions to parse all the vote data
    '''

    def list(self, request):
        serializer = ElectionSerializer(Election.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        serializer = ElectionSerializer(Election.objects.all())
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        if data['type'] == 'start':
            elections = Election.objects.filter(is_active__exact=True)
            if elections:
                return Response(data={"error": "An election has already started"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new election
            start_time = datetime.now()
            end_time = start_time + timedelta(days=30)
            created_election = Election.objects.create(
                start=start_time, end=end_time, is_active=True)

            # Contact ml-lib
            url = "localhost:8200/initiatives/generate/"
            # may take some time if using AI backend
            generated_initiatives = requests.get(url)

            # Create initiatives and policies based on data
            # data = {initiatives: [{name, description, policies: [(policy type, policy title, policy desc, policy cost)]}]}
            initiatives = generated_initiatives
            for initiative in initiatives:
                # get name, desc
                # for now, forget about name and desc, just send back the policy type text
                name, desc, _type = initiative['name'], initiative['description'], initiative['type']
                weights = initiative['weights']
                created_initiative = Initiative.objects.create(
                    initiative_type=_type, election=created_election, policy_type_weights=weights)
                # create the policies
                for policy in initiative['policies']:
                    title = policy[0]
                    description = policy[1]
                    policy_type = policy[2]
                    policy_cost = policy[3]
                    created_policy = Policy.objects.create(
                        initiative=created_initiative, policy_type=policy_type, policy_title=title, policy_description=description, policy_cost=policy_cost)


@api_view(['post'])
def end_election(request):
    election = Election.objects.filter(is_active__exact=True).first()
    if not election:
        return Response(data={"error": "No elections active right now"}, status=status.HTTP_400_BAD_REQUEST)

        # Sum up the votes in this election -> first past the post for now
    votes = Vote.objects.filter(election=election)

    # Get number of initiatives
    initiatives = Initiative.objects.filter(election=election)

    tally = [0] * len(initiatives)
    for vote in votes:
        # get first initiative
        initiative_selected = vote.initiatives[0]
        tally[initiative_selected] += 1

    # If no votes, randomly select an winning initiative
    winning_initiative_type = np.argmax(tally)

    # Get all initiative names
    names = []
    for initiative in initiatives:
        names.append(str(initiative))

    # Delete all the initiatives that were not elected
    # Automatically deletes the policies for initiatives weren't elected
    Initiative.objects.exclude(
        initiative_type__exact=winning_initiative_type).delete()

    # Set the winner to ElectedInitiative
    ElectedInitiative.objects.delete()
    ElectedInitiative.objects.create(
        elected_initiative=initiatives[winning_initiative_type])

    # Set the election to not active
    election.is_active = False
    election.save()

    # Create an election results object
    ElectionResults.objects.create(
        election=election, n_votes_initiatives=tally, initiative_names=names)

    # Now, results should be updated in /results/
    return Response(data={"is_success": True}, status=status.HTTP_200_OK)


@api_view(['get'])
def retrieve_results(request):
    '''
    Displays the results for the most recent election.
    Sends back = {initiative_1: 20, initaitive_2: 55 ...}

    NOTE: Only allows GET.
    '''
    '''
        Returns the results for the most recent election
        '''
    most_recent_election = Election.objects.latest('election_end')
    result = ElectionResults.objects.filter(
        election=most_recent_election).first()
    # get the voting numbers
    numbers = list(result.n_votes_initiatives)
    # get the initiative names
    names = list(result.initiative_names)
    data = {}
    for prop, i in enumerate(numbers):
        data[i] = prop

    return Response(data=data, status=status.HTTP_200_OK)


class ElectionGenericView(viewsets.ModelViewSet):
    '''
    Gets and returns elections
    '''
    queryset = Election.objects.filter(is_active__exact=True)
    serializer_class = ElectionSerializer


@api_view(['get'])
def get_offers(request):
    '''
    body -> token
    '''
    token = request.data['token']
    user = get_user(token)
    if not user:
        return Response(data={"error": "No User Exists"}, status=status.HTTP_400_BAD_REQUEST)
    # filter promotions
    promotions = JobPromotion.objects.filter(user=user)

    # filter offers
    offers = JobOffer.objects.filter(user=user)

    # {promotions: [{promotion}], offers: [{offer}]}
    data = {"promotions": promotions, "offers": offers}
    return Response(data=data, status=status.HTTP_200_OK)


class ElectionResultsView(viewsets.ModelViewSet):
    queryset = ElectionResults.objects.all()
    serializer_class = ElectionResultsSerializer


class InitiativeGenericView(viewsets.ModelViewSet):
    '''
    Gets and returns Initiatives
    '''
    queryset = Initiative.objects.all()
    serializer_class = InitiativeSerializer


class DepartmentView(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PolicyView(viewsets.ModelViewSet):
    # can get currently elected initiative
    # initiative = ElectedInitiative.objects.first()
    # queryset = Policy.objects.filter(initiative=initiative)
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class ElectedInitiativeView(viewsets.ModelViewSet):
    queryset = ElectedInitiative.objects.all()
    serializer_class = ElectedInitiativeSerializer


class VoteView(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoterDetail(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer


class SentimentView(viewsets.ModelViewSet):
    queryset = Sentiment.objects.all()
    serializer_class = SentimentSerializer


class UserViewSet(APIView):
    def post(self, request, *args, **kwargs):
        '''
        Register User Function

        Request needs to contain:
        {
          "email",
          "password",
          "medicare",
          "irn",
          "driver_leicense"
        }
        '''
        print(request.data)
        password = request.data.get('password')
        hashed_password = hash_pwd(password)
        medicare_num = request.data.get('medicare')
        irn = request.data.get('irn')
        medicare = {
            'card_number': int(medicare_num),
            'IRN': int(irn)
        }
        d_license = request.data.get('driver_license')
        voter = Voter.objects.filter(
            medicare=medicare, driver_license=d_license).first()
        if voter is None:
            data = {
                "error": "Please enter correct driver license and medicare"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            u_id = getattr(voter, 'user_id')
        data = {
            'user_id': u_id,
            'email': request.data.get('email'),
            'hashed_password': hashed_password,
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            data = {
                "token": create_token(u_id)
            }
            serializer.save()
            return Response(data=data, status=status.HTTP_201_CREATED)
        print('here')
        return Response({"error": serializer.errors['email'][0]}, status=status.HTTP_400_BAD_REQUEST)


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interests.objects.all()
    serializer_class = InterestSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ResidenceViewSet(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer


class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.filter(ongoing__exact=True)
    serializer_class = PollSerializer


class PollResultViewSet(viewsets.ModelViewSet):
    queryset = PollResult.objects.all()
    serializer_class = PollResultSerializer


@api_view(['get'])
def do_gboost(request):
    '''
    Do gboost
    '''
    gboost()
    return Response(data={"status": "done"}, status=status.HTTP_200_OK)


@api_view(['post'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user is None:
        data = {
            "error": "Wrong password or email"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    if check_pwd(password, getattr(user, 'hashed_password').encode('utf-8')):
        data = {
            "token": create_token(getattr(user, 'user_id')),
        }
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {
            "error": "Wrong password or email"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
def notifications(request):
    '''
    For a given user with user_id, return anything new about them.
    Also forwards request to /gcoin microservice to get updated rates for the current hour.
    RN this includes:
        - job offers
        - promotions
    E.g.,
        {
            "job_offer": ["researcher", 5],
            "promotions": ["head researcher", 8],
        }
    '''
    # check the user's list of possible offers, if exists, add first one
    user_token = request.META['HTTP_AUTHORIZATION']
    # check if token corresponds to user_id
    user = get_user(user_token)
    if (user is None):
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    # check the user's list of possible promotions, if exists, add first one
    promotions = JobPromotion.objects.filter(user=user).first()
    offers = JobOffer.objects.filter(user=user).first()

    # package data and return
    data = {"job_promotion": [str(promotions.type), promotions.job_rank],
            "job_offer": [str(offers.job_offer), offers.job_rank]}
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['get'])
def get_userData(request):
    '''
    get user data that is available to the user
    Request should just include token
    '''
    token = request.META['HTTP_AUTHORIZATION']
    voter = get_voter(token)
    user = get_user(token)
    if voter is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        email = getattr(user, 'email')
        name = getattr(voter, 'legal_name')
        sex = getattr(voter, 'sex')
        age = getattr(voter, 'age')
        driver_license = getattr(voter, 'driver_license')
        medicare = getattr(voter, 'medicare')
        family = getattr(voter, 'n_family')
        education = str(_Education(getattr(voter, 'education_level')).label)
        residence = getattr(voter, 'residence')
        country = str(getattr(voter, 'country'))
        occupation = str(getattr(voter, 'current_occupation'))
        occupation_rank = getattr(voter, 'occupation_rank')
        income = getattr(voter, 'income')
        government_employee = getattr(voter, 'government_employee')
        skills = [str(i) for i in list(voter.skills.all())]
        interests = [str(i) for i in list(voter.interests.all())]
        contribution = getattr(voter, 'contributions')
        political_interests = getattr(voter, 'political_interest')

        data = {
            "email": email,
            "name": name,
            "sex": sex,
            "age": age,
            "driver_license": driver_license,
            "medicare": medicare,
            "family": family,
            "education": education,
            'residence': str(residence),
            'country': country,
            'current_occupation': occupation,
            'occupation_rank': occupation_rank,
            'income': income,
            'government_employee': government_employee,
            'interests': list(interests),
            'skills': list(skills),
            "contribution": contribution,
            "political_interests": political_interests
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['put'])
def change_password(request):
    token = request.META['HTTP_AUTHORIZATION']
    original_password = request.data.get('o_password')
    new_password = request.data.get('n_password')
    user = get_user(token)

    if user is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        hashed_pwd = getattr(user, 'hashed_password')
        if not check_pwd(original_password, hashed_pwd.encode('utf-8')):
            data = {
                "Error": "Password does not match"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        new_hashed_pwd = hash_pwd(new_password)
        user.hashed_password = new_hashed_pwd
        user.save()
        data = {
            "Success": "Password updated"
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['get'])
def get_interests(request):
    token = request.META['HTTP_AUTHORIZATION']
    voter = get_voter(token)

    if voter is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        interests = list(voter.interests.all())
        result = []
        for i in interests:
            interest = {'value': i.type, 'label': str(i)}
            result.append(interest)
        print(result)

        data = {
            'interests': result
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['put'])
def update_interests(request):
    token = request.META['HTTP_AUTHORIZATION']
    voter = get_voter(token)
    interests = request.data.get('interests')
    print(interests)

    if voter is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        interest_types = []
        for interest in interests:
            interest_types.append(Interests.objects.filter(
                type=interest['value']).first())
        voter.interests.clear()
        voter.interests.add(*interest_types)
        voter.save()

        data = {
            'Success': "Interests updated"
        }

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['get'])
def get_skills(request):
    token = request.META['HTTP_AUTHORIZATION']
    voter = get_voter(token)

    if voter is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        skills = list(voter.skills.all())
        result = []
        for i in skills:
            skill = {'value': i.type, 'label': str(i)}
            result.append(skill)
        data = {
            'interests': result
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['put'])
def update_skills(request):
    token = request.META['HTTP_AUTHORIZATION']
    voter = get_voter(token)
    skills = request.data.get('skills')

    if voter is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        skill_types = []
        for skill in skills:
            skill_types.append(Interests.objects.filter(
                type=skill['value']).first())
        voter.interests.clear()
        voter.interests.add(*skill_types)
        voter.save()

        data = {
            'Success': "Interests updated"
        }

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['get'])
def get_initiative(request):
    elect_id = request.GET.get('elect_id', '')
    election = Election.objects.filter(elect_id=elect_id)
    if election is None:
        data = {
            "Error": "Invalid election id"
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    else:
        initiatives = Initiative.objects.filter(election__in=election)
        result = []
        for init in initiatives:
            result.append(getattr(init, 'initiative_type'))
        result.sort()
        data = {
            "initiatives": result
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['post', 'get'])
def vote(request):
    if request.method == 'POST':
        token = request.META['HTTP_AUTHORIZATION']
        elect_id = request.data.get('elect_id')
        user = get_user(token)
        election = Election.objects.filter(elect_id=elect_id).first()
        initiatives = request.data.get('initiatives')
        if user is None:
            data = {
                "Error": "Invalid Token"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        if election is None:
            data = {
                "Error": "Election does not exist"
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        data = {
            'election': elect_id,
            'user_id': getattr(user, 'user_id'),
            "initiatives": initiatives,
        }
        serializer = VoteSerializer(data=data)
        if not serializer.is_valid():
            data = {
                "Error": serializer.errors,
            }
            print(serializer.errors)
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "success": "Successfully voted."
        }
        serializer.save()
        return Response(data=data, status=status.HTTP_200_OK)
    if request.method == 'GET':
        token = request.META['HTTP_AUTHORIZATION']
        elect_id = request.GET.get('elect_id', '')
        election = Election.objects.filter(elect_id=elect_id).first()
        user = get_user(token)
        if user is None:
            data = {
                "Error": "Invalid Token"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        if election is None:
            data = {
                "Error": "Election does not exist"
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        vote = Vote.objects.filter(user_id=user, election=election).first()
        if vote:
            data = {
                "status": "Voting completed",
                "end_date": getattr(election, 'election_end')
            }
            return Response(data=data, status=status.HTTP_202_ACCEPTED)
        data = {
            "status": "Voting needed",
            "end_date": getattr(election, 'election_end')
        }
        return Response(data=data, status=status.HTTP_200_OK)

@api_view(['post'])
def create_poll(request):
    token = request.META['HTTP_AUTHORIZATION']
    answer = request.data.get('answer')
    poll_id = request.data.get('poll_id')
    
    poll = Poll.objects.filter(id=poll_id).first()
    user = get_user(token)
    if user is None:
        data = {
            "Error": "Invalid Token"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    if poll is None:
        data = {
            "Error": "Poll does not exist"
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if type(answer) == type([]):
        answer = ','.join(answer)
    data = {
        'question_id': poll_id,
        'user_id': getattr(user, 'user_id'),
        'date_time': datetime.now(),
        'answer': answer
    }
    serializer = PollResultSerializer(data=data)
    if not serializer.is_valid():
        data = {
            "Error": serializer.errors,
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    data = {
        "success": "Successfully entered poll."
    }
    serializer.save()
    return Response(data=data, status=status.HTTP_200_OK)
