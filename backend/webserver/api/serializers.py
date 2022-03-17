from rest_framework.fields import SerializerMethodField
from .models.User import User
from rest_framework import serializers
from .models.Voter import Voter
from rest_polymorphic.serializers import PolymorphicSerializer
from .models.Skill import Skill
from .models.Interests import InterestType, Interests
from .models.Residence import Residence
from .models.Occupation import Occupation
from .models.Department import Department, StateDepartment, LocalDepartment
from .models.Poll import Poll
from .models.PollResult import PollResult
from .models.Vote import Vote
from .models.Election import Election
from .models.Initiative import Initiative
from .models.Sentiment import Sentiment
from .models.Policy import Policy
from .models.ElectedInitiative import ElectedInitiative
from .models.ElectionResults import ElectionResults
from .models.JobOffer import JobOffer
from .models.JobPromotion import JobPromotion


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'email', 'hashed_password')

class JobPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPromotion
        fields = ('user', 'type', 'job_rank')

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ('user', 'job_offer', 'job_rank')


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ('user_id', 'driver_license', 'medicare', 'legal_name', 'sex', 'age', 'education_level', 'contributions', 'government_employee', 'income',
                  'skills', 'interests', 'contributions',
                  'political_interest')


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ('elect_id', 'election_start', 'election_end', 'is_active')


class ElectionResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionResults
        fields = ('election', 'n_votes_initiatives', 'initiative_names')


class ElectedInitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectedInitiative
        fields = ('elected_initiative',)


class InterestSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='get_type_display')

    class Meta:
        model = Interests
        fields = ('type', 'description', 'type_name')
    # def get_type_display(self):
    #     return str(InterestType(self.type).label)


class SkillSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='get_type_display')

    class Meta:
        model = Skill
        fields = ('type', 'description', 'type_name')


class UserPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        User: UserSerializer,
        Voter: VoterSerializer,
    }


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ('type', 'description', 'demand_level')


class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ('user_id', 'address', 'suburb',
                  'postcode', 'electoral_district')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('type', 'name', 'description', 'level')


class StateDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('type', 'name', 'description', 'level', 'state')


class LocalDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('type', 'name', 'description', 'level', 'electoral_district')


class DepartmentPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Department: DepartmentSerializer,
        StateDepartment: StateDepartmentSerializer,
        LocalDepartment: LocalDepartmentSerializer,
    }


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'question', 'ongoing', 'type',
                  'end_date', 'possible_answers', 'subject')


class PollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollResult
        fields = ('question_id', 'user_id', 'date_time',
                  'answer')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('election', 'user_id', 'initiatives')


class InitiativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiative
        fields = ('initiative_type', 'election', 'policy_type_weights')


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment
        fields = ('policy_type', 'strength')


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('initiative', 'policy_type', 'policy_title',
                  'policy_cost', 'policy_description')
