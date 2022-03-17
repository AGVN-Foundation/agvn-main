'''
Helper function module
'''
from .models.Initiative import Initiative
from .models.ElectedInitiative import ElectedInitiative
from .models.Policy import Policy
from .models.JobPromotion import JobPromotion
from .models.JobOffer import JobOffer
from .models.Occupation import Occupation
from .models.Poll import Poll
from .models.Voter import Voter
from .models.User import User
import bcrypt
import jwt
import uuid
from datetime import date, datetime, timedelta
import requests

'''
We can change the secret and algorithm in the future
'''
SECRET = 'secret'
ALGORITHM = 'HS256'
EXPIRE = 1      # token expire in an hour

AGVN_GCOIN_ADDRESS = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCIBesUB/eF99DcdbktEuhJMT/6\
Ziw38CMqUnpB6ShUYpV8xs92L1XEWR7xH0/sCb3zoOChSFEHpQVhQxsD4Wn3sUiX\
CHo8QjVCSDaEJgqU/5u4HLooeMxQprGvQ8IiDPQwRoHNhQtVDgCZmTzQ+VOGE+SD\
HMees6LEQ1jRtcwVxwIDAQAB'
AGVN_GCOIN_SECRET = 'MIICXQIBAAKBgQCIBesUB/eF99DcdbktEuhJMT/6Ziw38CMqUnpB6ShUYpV8xs92\
L1XEWR7xH0/sCb3zoOChSFEHpQVhQxsD4Wn3sUiXCHo8QjVCSDaEJgqU/5u4HLoo\
eMxQprGvQ8IiDPQwRoHNhQtVDgCZmTzQ+VOGE+SDHMees6LEQ1jRtcwVxwIDAQAB\
AoGAa1/woBFh7ZkggMdVdCVWxGBiVrHM+iNQPxp4dAsv0N05kBQItQzMsYCAkmrb\
VkKide1rJSXHATfdNVgZvUh1svBxhA5okWcDk2nZFA6/Y/C4P6PXkvHnxzlrfEjW\
0k0TpJAs37i4CqcexbIMkJIDSY/xhEj4tGwZkwD4qe7E6HECQQDE0PGGpivIFucI\
4elSuQWOCcUox7cRI7cnfCZMNn0+mq+Z6ZclMv1LQxRZhwpbe0L+/GPhelIpVach\
NsGVx5zlAkEAsO0USDxlq6q68TPvnK5jguN3jzYsMwYg44oGefCigCfK+ukb87bL\
vD2wjZivpze9BhDs39nOeyEll6YpJZ1pOwJAM5Z42ExSCX5HTIK6f55ToGlbLlc6\
2tk7trPJ7gwSRAiTooohvfRhhAqvGNBWnKfwZZmOLJm9U2xKBGCv2SybKQJBAJZy\
s6mNemNVBiyvnlTc0g/uP6/PQByPXI5Aw6sTngteSzO74CIJUgwbZTOzH8MRGbK7\
18Guo+9+S0o+aITs6xsCQQCc4VmWtXIxEPjC+NUEG3J8B2Jy9R6kTzcJEoDw4wn6\
bUZamFC8U6XV39ySx0t0IIm5U0drSM7B9CxUSIOzebFN'


def place_on_spectrum():
    '''
    Places everyone on (-2,2) per policy type.
    Done when a voter is added to database or on yearly tick

    RN, depends mostly on income, education, occupation, sex
    Needs to also depend on interests, skills and residence
    Needs to also depend on polling and voting data

    @user -> Voter object

    NOTE: reply from policy/user needs to be in the style of an array from 0-16
            in order of policy type
    '''
    url = 'http://localhost:8200/policy/user'
    try:
        users = User.objects.all()
        #   get their income, education, occupation, sex
        for user in users:
            income = user.income
            education_lvl = user.education_level
            occupation_rank = user.occupation_rank
            contributions = user.contributions

            occupation = user.occupation
            n_family = user.n_family
            age = user.age

            skills = user.skills
            interests = user.interests

            sex = user.sex
            country = user.country

            # call ML on these features to weight for one user
            # use microservice for now
            res = requests.post(url, data={
                "income": income,
                "education_level": education_lvl,
                "occupation_rank": occupation_rank,
                "contributions": contributions,
                "occupation": occupation,
                "n_family": n_family,
                "age": age,
                "skills": skills,
                "interests": interests,
                "sex": sex,
                "country": country,
            })

            # assume request is perfect, if not, continue
            if res.status_code != 200:
                continue
            data = res.json()

            # reweigh the user's policy types
            user_policy_views = user.policy_interest

            # use those factors as weights to put them somewhere in the normalized coordinate spectrum => (-2,2) per policy type
            for weight, i in enumerate(data['weights']):
                user_policy_views[i] = weight

    except Exception as e:
        print("NOTICE: No users exist within database")


def check_offers_promotions(user_id):
    '''
    # For a given user, check whether their eligible for a government sponsored position or a promotion.

    If a user is already a government employee, just check whether they can be promoted.

    This depends on their contribution gain over the past month.
    ! RN, if there contribution gain >= 1000, they get to be promoted

    NOTE: if user accepts, then they basically send to /api/v1/promotions their token, id, new occupation, new occupation_rank
    '''
    def check_occupations_in_demand():
        # filter demand_level of at least 5
        occupations = Occupation.objects.filter(demand_level__gte=5)
        occ_in_demand = list(
            map(lambda x: (x.type, x.demand_level), occupations))
        # return [(type, demand_level)]
        return occ_in_demand

    try:
        voter = Voter.objects.get(user_id=user_id)
        # Algorithm:
        # check date since voter was created. If created < 30 days ago, then use that as date. Else use date = 30
        contributions = voter.contributions
        len_contrubutions = len(contributions)
        # check if contribution[date] - contribution[0] >= 1000
        if contributions[len_contrubutions] - contributions[0] >= 1000:
            # check if any occupations are in demand
            occupations = check_occupations_in_demand()
            # sort offers by demand_level
            occupations.sort(key=lambda x: x[1], reverse=True)

            # check their skills and current occupation to see whether it matches any of the specified occupations
            skills = voter.skills
            possible_offers = []
            for occ in occupations:
                skill_types = skills.objects.filter(type__exact=occ[0])
                # if true, then assign
                possible_offers.append(skill_types[0])

            voter_occupation = voter.occupations
            if voter_occupation in list(map(lambda x: x[0], occupations)):
                possible_offers.insert(voter_occupation, 0)

            voter_occupation_level = voter.occupation_level
            new_occ_level = voter_occupation_level + \
                1 if voter_occupation_level < 10 else 10

            # check if voter is already a government employee, if so, send back as "promotion": "occupation_type"
            # else send back as "position": "occupation_type"
            if voter.government_employee:
                # if voter is already level 10, then dont increase
                res = {"promotion": possible_offers[0], "level": new_occ_level}
            else:
                res = {"position": possible_offers[0], "level": new_occ_level}

            #   return the occupation type that is most in demand and they have some skill for it -> for now, just return a random one
            return res

    except Exception as e:
        print("ERROR: user with id {user_id} does not exist")

    return None


def handle_daily_tick():
    '''
    Checks contribution growth for job offers and promotions.
    Idea -> Every day, call this function -> time.sleep(86400)
    - For each poll, check if datetime.now() > end_date. Set ongoing=False if true. When a poll is finished, use all the poll results to adjust user's political interests.
    - For each user, remove their earliest contribution field.
    - Call check_promotions(user) for each user. If return a non None tuple, then take the first item[0] and append to offers. If second tuple[1] is non None, append to promotions.
    '''
    # for each user
    voters = Voter.objects.all()
    #   move all contribution indexes back one step -> can do this manually for now
    voter_promotions = []
    for voter in voters:
        contributions = voter.contributions[:15]
        voter.contributions = contributions
        #   set contribution[0] = 0
        voter.contributions.insert(0, 0)
        #   check_promotions
        promotions = check_offers_promotions(voter.user_id)
        if promotions:
            promotions["user_id"] = voter.user_id
            voter_promotions.append(promotions)
            # add promotions to JobPromotion or JobOffer
            if promotions['promotion']:
                type = promotions['promotion']
                user_id = voter.user_id
                user = User.objects.get(user_id=user_id)
                rank = promotions['level']
                JobPromotion.objects.create(
                    user=user, type=type, job_rank=rank)
            else:
                type = promotions['promotion']
                user_id = voter.user_id
                user = User.objects.get(user_id=user_id)
                rank = promotions['level']
                JobPromotion.objects.create(
                    user=user, job_offer=type, job_rank=rank)

    # for each poll
    polls = Poll.objects.all()
    # todays date
    today_date = date.today()
    for poll in polls:
        if poll.end_date >= today_date:
            poll.ongoing = False


def gboost():
    '''
    - Give everyone +X GCoin
    '''
    GBOOST_AMOUNT = 50

    voters = Voter.objects.all()
    for voter in voters:
        transaction = {"from": AGVN_GCOIN_ADDRESS, "to": voter.gcoin_address,
                       "amount": GBOOST_AMOUNT, "fee": 1}
        requests.post("http://localhost:4200/send/", data=transaction)


def handle_monthly_tick():
    '''
    GBoost, etc.
    '''
    gboost()


def handle_yearly_tick():
    '''
    Updates for yearly-based events
    - Re-place all voters on the political spectrum

    Ticks done when server is on -> uses timer module (sleep-wake) -> time.sleep(31536000)
    can be called when daily-tick detects a new year
    '''
    place_on_spectrum()


def elect(new_initiative):
    '''
    When initiatives are generated, they do not have any policies.
    The old initiative removes all their old policies upon election,
    and generates new ones based on their old initiatives, etc.

    Elect an initiative.
    '''
    # remove old initiative
    elected_initiative = ElectedInitiative.objects.first()
    # if old initiative = new initiative, then just delete everyone elses policies
    if elected_initiative == new_initiative:
        Policy.objects.exclude(initiative=new_initiative).delete()
        return

    Policy.objects.exclude(initiative=new_initiative).delete()
    ElectedInitiative.objects.delete()

    # add new initiative
    ElectedInitiative.objects.create(new_initiative)


def sum_budget():
    '''
    Sum up the budget based on each policy's value
    '''
    sum = 0.0

    # get the elected initiative
    elected_initiative = ElectedInitiative.objects.first()
    # for all policies
    policies = Policy.objects.filter(
        initiative__exact=elected_initiative).first()
    for policy in policies:
        sum += policy.policy_cost

    return sum


def hash_pwd(pwd):
    '''
    Takes in a string, return a string of hashed password
    '''
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode()


def check_pwd(pwd, hashed_pwd):
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed_pwd)


def create_token(uid):
    '''
    Create a token that expires in an hour
    '''
    if type(uid) == uuid.UUID:
        uid = str(uid)

    payload = {
        'user_id': uid,
        'exp': datetime.utcnow()+timedelta(hours=EXPIRE)
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def get_user_id(token):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])['user_id']
    except:
        return None

def get_user(token):
    '''
    Use token to get the corresponding User model
    None if not found
    '''
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    return User.objects.filter(user_id=decoded['user_id']).first()


def get_voter(token):
    '''
    Use token to get the corresponding Voter model
    None if not found
    '''
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id = decoded['user_id']
    except jwt.ExpiredSignatureError:
        return None
    return Voter.objects.filter(user_id=user_id).first()


class BlackList:
    '''
    Used to blacklist invalid tokens (e.g. logged out),
    called by django crontab every 30 min to remove any expired tokens altogether
    '''

    def __init__(self, blacklist=[]):
        self.blacklist = blacklist

    def add_token(self, token):
        self.blacklist.append(token)

    def check_in_blacklist(self, token):
        return token in self.blacklist

    def remove_from_blacklist(self, token):
        self.blacklist.remove(token)
