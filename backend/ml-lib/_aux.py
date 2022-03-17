'''
Contains helper functions and values
'''

# Begin. Define values for each policy type for each initiative type
# -2 means really against idea
# 0 means doesnt really care
# 2 means really supports idea
# NOTE: right wing ideals in Australia are seen as more 'radical' in terms of policy type values


conservative_values = [-0.75, -1.25, 1, 1, -1.25, 1.25, 1, 1.5, 1.5, 1.25, -0.375, -1.125, 1.25, 0.75, -1.25, -1, 1.25]
progressive = [0.125, 1, 1.25, 0.75, 1, 1.25, 1.5, -1, 1, 0.5, 1, 1, 0, -1, 0.25, 1, -1]
libertarian_values = [-1.875, -1.375, -0.75, -1, -1, -1.25, -1.5, -1, -1.25, -0.5, -1, -1.5, -0.5, 0.25, -1.5, 1.5, -1]
activist = [-1.375, 1.25, 1.5, 0.75, -0.375, 0.5, 1.375, 0.25, 0.25, 1.125, 0.125, 1.25, -1.25, -0.75, 1.25, 0.125, -1.25]
left_libertarian = [1.75, 1.5, 1.5, 0, 1.5, 1.375, 1.5, -1.5, -0.5, -1, 1, 1.75, -0.75, -1.5, 1.5, 0, -1.75]
social_democratic = [1.5, 0, 0, 1, 0.25, 1.375, 1.5, 0, 0.5, 0.125, -0.125, 0.5, 0.5, 0.75, 1.375, 0.375, 0]
statism = [0.125, 0, 1, 1.5, -1, -0.125, 0.25, 0.5, 0.5, 1, 1.25, -0.875, 1.25, 0.5, 0.75, -0.5, 1.5]
authoritarian = [-0.125, 0.25, 0, 1.5, -0.125, 0, 0, 1, 1, 1, 1, 0, 1.5, 1.5, 1, 1.25, 1.5]

# Pt.1 Define voter features and policy types to be included


class PolicyType:
    TAXATION = 1
    LIFESTYLE_CULTURE = 2
    COMMUNITY = 3
    INFRASTRUCTURE = 4
    FOREIGN_RELATIONS = 5
    HEALTH = 6
    EDUCATION_EMPLOYMENT = 7
    NATIONAL_SECURITY = 8
    SAFETY = 9
    INDUSTRY = 10
    SCIENCE_TECHNOLOGY = 11
    ENVIRONMENT = 12
    ENERGY = 13
    ASSETS = 14
    ECONOMY = 15
    FOREIGN_TRADE = 16
    NATURAL_RESOURCES = 17

class PollType():
    MULTI_CHOICE = 1
    SCALE = 2
    SHORT_ANSWER = 3
    CHECK_BOX = 4
    DROP_DOWN = 5

class InitiativeType():
    CONSERVATIVE = 1
    PROGRESSIVE = 2
    LIBERTARIAN = 3
    ACTIVIST = 4
    LEFT_LIBERTARIAN = 5
    SOCIAL_DEMOCRATIC = 6
    STATIST = 7
    AUTHORITARIAN = 8

# female -> more liberal, more authoritarian
SEX = 1
# older -> more conservative, more authoritarian
AGE = 2
# more family -> more conservative
N_FAMILY = 3
# higher education -> more liberal
EDUCATION_LEVEL = 4
# from another country -> more conservative
COUNTRY = 5
# FINANCIAL, REAL_ESTATE, UTILITIES, MANUFACTURING, LOGISTICS, HEALTHCARE_SOCIAL, RETAIL_TRADE, WHOLESALE_TRADE, CONSTRUCTION, ACCOMODATION_FOOD, RETAIL_TRADE -> more conservative, less authoritarian
# ENVIRONMENTAL_INDUSTRY, MEDIA, PROFESSIONAL_SCIENTIFIC, ADMINISTRATIVE_SUPPORT, PUBLIC_ADMINISTRATION_SAFETY, EDUCATION_TRAINING, HEALTHCARE_SOCIAL, ARTS_RECREATION -> more liberal, more authoritarian
# NOTE: for occupation, we just assume it is in ascending order of liberal and authoritarian
OCCUPATION = 6
# higher rank -> less authoritarian
OCCUPATION_RANK = 7
# higher income -> more liberal, less authoritarian
INCOME = 8
# government emplyee -> more authoritarian
GOVERNEMNT_EMPLOYEE = 9
# more skills -> less authoritarian
SKILLS = 10
# more interests -> less authoritarian
INTERESTS = 11
# higher contribution growth -> more liberal
# higher average contribution -> more authoritarian
CONTRIBUTIONS = 12

# Another view
# SEX = [1, 2, 3]
# AGE = int()
# N_FAMILY = int()
# EDUCATION_LEVEL = int()
# COUNTRY = str()
# OCCUPATION = list(range(19))
# OCCUPATION_RANK = list(range(1,11))
# INCOME = int()
# GOVERNEMNT_EMPLOYEE = bool()
# SKILLS = str()
# INTERESTS = str()
# CONTRIBUTIONS = int()


# rank user features in order of importance
tier_1 = [INCOME, OCCUPATION_RANK, EDUCATION_LEVEL, CONTRIBUTIONS]

tier_2 = [OCCUPATION, N_FAMILY, AGE]

tier_3 = [SKILLS, INTERESTS, GOVERNEMNT_EMPLOYEE]

tier_4 = [SEX, COUNTRY]


# give each feature a scaling value for each policy type

class Scaling:
    LOW = 1
    MED = 2
    HIGH = 3

class PositiveScaling(Scaling):
    pass

class NegativeScaling(Scaling):
    pass

# Idea -> could use AI (e.g. reinforcement learning) to classify users into bins for each policy type
# RL would have to label itself through 

scaling_policy_taxation = [
    # tier 1
    {INCOME: NegativeScaling.MED, OCCUPATION_RANK: NegativeScaling.HIGH,
        EDUCATION_LEVEL: PositiveScaling.HIGH, CONTRIBUTIONS: PositiveScaling.MED},
    # tier 2
    {OCCUPATION: PositiveScaling.MED, N_FAMILY: PositiveScaling.MED, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

# 'lifestyle and culture = how much someone participates in lifestyle and culture'
scaling_policy_lifestyle_culture = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_community = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_infrastructure = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_health = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_education_employment = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_national_security = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_safety = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_industry = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_science_technology = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_environment = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_energy = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_assets = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_economy = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_foreign_trade = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

scaling_policy_natural_resources = [
    # tier 1
    {INCOME: NegativeScaling.LOW, OCCUPATION_RANK: NegativeScaling.LOW,
        EDUCATION_LEVEL: PositiveScaling.LOW, CONTRIBUTIONS: PositiveScaling.HIGH},
    # tier 2
    {OCCUPATION: NegativeScaling.MED, N_FAMILY: PositiveScaling.HIGH, AGE: NegativeScaling.MED},
    # tier 3
    {SKILLS: PositiveScaling.LOW, INTERESTS: PositiveScaling.LOW},
    # tier 4
    {SEX: PositiveScaling.LOW, SEX: PositiveScaling.LOW},
]

