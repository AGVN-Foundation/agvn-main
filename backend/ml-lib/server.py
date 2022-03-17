'''
Server for machine learning modules
Includes:
    - APIs to generate a poll
    - APIs to run classic automated pipelines involving ML, to reweigh the weights for each policy topic
    - APIs to generate initiatives and the policies for each initiative based on previous polls and recent sentiment (api to push election basically generates initiatives)
    - APIs to post an action prompt and return an 'action description'
    - APIs for government employees to post an 'official recommendation' and change policy weights, or introduce completely new policy 'types'.
'''
from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
from generate_blog import gen_sentences, gen_blog_pipeline
import random
import requests
from pydantic import BaseModel
from generate_poll import gen_question
from behavioral import predict_behavior
import re
import base64
from ml_api import hyperml

app = FastAPI()


@app.get("/")
async def ml_home():
    return {"message": "Hi"}


class Sentiment(BaseModel):
    policy_type: int
    strength: int


@app.post("/sentiment/recent")
async def set_recent_sentiment(sentiment: Sentiment):
    # NOTE: even though sending sentiment to /scraper is possible, we can do it here too
    '''
    Directly set a sentiment for direct use on ML

    Algorithm:
        - for sentiment.policy_type
        - set it to sentiment.strength where +2 -> enthusiastic, -2 -> revolting
    '''
    url = "http://localhost:8000/api/v1/sentiment"
    requests.post(
        url, data={"policy_type": sentiment.policy_type, "strength": sentiment.strength})


@app.get("/polls/generate")
async def gen_polls():
    '''
    Returns polls in the style required by the frontend. Mainly based on recent sentiment.
    Generates 0 or more polls based on the policy types with the highest changed sentiment.

    ML implementation:
    - every 2 weeks, dump all the voter and poll data into csvs. Then time mark the csvs like 'voter-2021-01-01.csv'
    - look at database of voter data over past 30 days. Take the difference between each numerical feature and create a new dataframe with the differences
    - look at database of recent sentiment
    - for each policy
        - check if the words expressed by social media and news media matches the type
        - check what sentiment (positive, neutral, negative) they are stating and scale to [-2, 2]
        - determine what poll types (MC, short answer, etc) are available (hardcoded) for the policy type
        - generate a random poll type. Use the words expressed as prompts for GPT to autocomplete
    '''
    pass
    # For now, look at each sentiment
    # IF sentiment ~ 0.0 => [-0.5, +0.5] then skip that
    # If sentiment is high, push a positive poll for that policy type
    # If sentiment is low, push a negative poll


@app.get("/poll/generate")
async def gen_poll(policy_type: str):
    '''
    Generates a single poll based on a policy type and sentiment
    Used for demonstration purposes

    policy_type ->
    '''
    # If sentiment is high, return a positive poll for that policy type
    # If sentiment is low, return a negative poll
    res = gen_question(policy_type)
    question = res[0]
    possible_answers = res[1]
    poll_type = res[2]

    return {"question": question, "possible_answers": possible_answers, "type": poll_type}


@app.get("/poll/sentiment")
async def gen_poll(policy_type: str, sentiment: str):
    '''
    Generates a single poll based on a policy type and sentiment
    Used for demonstration purposes
    '''
    # If sentiment is high, return a positive poll for that policy type
    # If sentiment is low, return a negative poll
    res = gen_question(policy_type, sentiment)
    question = res[0]
    possible_answers = res[1]
    poll_type = res[2]

    return {"question": question, "possible_answers": possible_answers, "type": poll_type}


class Result(BaseModel):
    k: int


@app.get("/poll/sentiment")
def do_hyperml(q_id: int, results: Result):
    '''
    Runs the HyperML pipeline.
    '''
    res = hyperml()
    return {"d1": res[0], "initiatives": res[1], "d2": res[2]}


def get_initiatives(n=7):
    '''
    Returns a list of initiatives
    name, desc, policies[]
    '''
    # RN, just generate random intiatives
    initiatives = []
    for i in range(n):
        data_struct = {"name": "initiative" + i,
                       "description": "description" + i, "type": i}
        policy_type_weights = [random.uniform(-2, 2) for _ in range(17)]
        data_struct['weights'] = policy_type_weights
        # data_struct["policies"] = []
        policies = []
        for j in range(random.randint(1, 20)):
            # generate random key value pairs
            policy_idea = "policy idea" + j
            policy_desc = "policy desc" + j
            policy_type = random.randint(1, 17)
            policy_cost = random.gauss(100000000, 5000)
            policies.append((policy_type, policy_idea,
                            policy_desc, policy_cost))

        data_struct["policies"] = policies
        initiatives.append(data_struct)

    return initiatives


@app.get("/initiatives/generate")
async def gen_initiatives():
    '''
    Returns a JSON list of initiatives
        {"initiatives": [
            {name, type, description, weights, policies: [("6", "...free healthcare", "Universal Access to Healthcare", "5000000")...]},
        ]}

    ML implementation: 
    - cluster everyone into at least 4 different groups. No more than 15.
    - set each group to an initiative
    - average the weights of all 4 different groups and put it as the weight for the initiative
    - use the following hueristic:
        - match each initiative to the closest ideology (base weights)
        - once an initiative has matched to an ideology, remove the ideology
    - for each initiative:
        - for each policy type:
            - if the weight diverges more than 0.5 from the base weight, set that as a 'new policy'
    - return list of initiatives and embedded lists of new policies
    '''
    initiatives = get_initiatives()
    return {"initiatives": initiatives}


class Action(BaseModel):
    prompt: str


@app.get("/action")
def gen_action(action: str):
    '''
    Call generate_blog with the prompt
    '''
    res = gen_blog_pipeline(action)
    return {"text": res}


class Policy(BaseModel):
    recommendation: str


@app.get("/policy/recommend")
async def recommend_policy(policy: str):
    '''
    Recommend a policy by writing a short prompt
    Uses generate_blog to generate a policy based on that prompt
    '''
    res = gen_blog_pipeline(policy)
    return {"text": res}


class Image(BaseModel):
    image: str


@app.post("/behavioral")
async def behavioral_analysis(img: Image):
    '''
    Analyze the image for good behavior -> res = analyze_behavior(img.file)
    If determined to be good, return True
    Else False
    '''
    img_dict = re.match(
        "data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", img.image).groupdict()

    with open("temp.jpeg", "wb") as fh:
        fh.write(base64.b64decode(img_dict['data'].encode()))

    result = predict_behavior("temp.jpeg")

    return {"label": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8200)
