'''
GCoin server serving crypto information on last 30 days
Intended as a microservice API for /webserver
Connects to UI along with wallet
Auto generates random gcoin values based on economic activity and sentiment
'''
from fastapi import FastAPI
from random import randint, gauss
import uvicorn
import gcoin
from gcoin import Block, Blockchain, Wallet, P2P
from pydantic import BaseModel

app = FastAPI()
value_determiner = None

# Server (core node) stores its own blockchain


class ServerStorage:
    '''
    Storage for the server.
    Uses temp.txt for pickling every time a new block is created -> temporary solution.
    '''

    def __init__(self, blockchain=Blockchain()):
        self.blockchain = blockchain
        self.total_transaction_list = []

    def add_block(self, block, validator_address, validator_signature, n_transactions):
        self.blockchain.make_block(
            block, validator_address, validator_signature, n_transactions)

    def add_transaction(self, transaction):
        self.total_transaction_list.append(transaction)

    def get_transactions(self):
        return self.total_transaction_list

    def get_blockchain(self):
        return self.blockchain


server_storage = None


@app.on_event("startup")
async def startup_event():
    global value_determiner, server_storage
    # sample activity
    activity = gen_values()
    value_determiner = ValueDeterminer(activity)
    server_storage = ServerStorage()


@app.get('/')
async def root():
    return {'gcoin_aud': value_determiner.predict_value()}


@app.get('/transactions')
async def transactions():
    '''
    Returns a list of transactions stored on the main Aeros server
    '''
    global server_storage
    return {"transactions": server_storage.get_transactions()}


@app.get('/peg/rate')
async def rate():
    return {'rate': value_determiner.get_pegged_rate()}


# Since this is a main storage node, it should not be creating new blocks
# @app.post('/block/create')
# async def create_block(gcoin_address, transaction_list, timestamp):
#     '''
#     Create a block
#     '''
#     pass

class GCoinTransaction(BaseModel):
    from_addr: str
    to_addr: str
    amount: int
    fee: int = 1


@app.post('/send')
async def send_gcoin(gcoin_transaction: GCoinTransaction):
    '''
    Create a transaction between [from_addr] -> [to_addr]
    Broadcast this message out
    '''
    global server_storage
    transaction = {"from": gcoin_transaction.from_addr, "to": gcoin_transaction.to_addr,
                   "amount": gcoin_transaction.amount, "fee": gcoin_transaction.fee}
    server_storage.add_transaction(transaction)
    return {"is_success": "true"}


@app.get('/statistics')
async def get_statistics():
    '''
    Return economic activity over past 30 days
    '''
    global value_determiner
    return {"values": value_determiner.activity}


class ValueDeterminer:
    def __init__(self, activity, strength=5, peg_value=1) -> None:
        '''
        Initialize a ValueDeterminer Object

        @peg_value = value to peg gcoin to AUD

        NOTE: peg value only works if every state/private exchange agrees with the pegged rates
        '''
        self.activity = activity
        self.strength = strength
        self.peg_value = peg_value

    def set_economic_activity(self, activity=[]):
        '''
        Set past 30 day economic activity in Australia
        Activity is defined as the average between amount in the country spent that day, worker productivity for that day 
        A = avg(conversion, #spent, #productivity)

        Activity: index 0 -> oldest, index 29 -> most recent

        @activity: LIST(INT), length should be 30
        '''
        self.activity = activity

    def add_new_activity(self, activity_value):
        if len(self.activity)-1 > 29:
            self.activity = self.activity[:len(self.activity)-1]
        self.activity.append(activity_value)

    def set_sentiment_strength(self, strength=5):
        '''
        Set the strength of mass sentiment

        @strength: INT, 1-10
        '''
        self.strength = strength

    def predict_value(self):
        '''
        Predicts the value of GCoin for the current day based on recent economic activity and strength
        Value = weighted sum(economic_activity) + strength
        '''
        w = 0
        for i in range(len(self.activity)):
            w += 0.01 * i * self.activity[i]
        value = w + self.strength

        return value

    def get_pegged_rate(self):
        return self.peg_value


# EXAMPLE: value of gcoin to aud over past 30 days -> set each hour
gcoin_values = [
    # day 0 genesis -> 24 values
    # (100,)
    # day 1
    # (69,)
    # day 2
    # (44,)
    # day 3
    # (60,)
    # day 4
    # (120,)
    # day 5
    # (200,)
    # day 6
    # (135,),
    # day 7
    # (118,)
    # WK 2 day 1
    # (119,)
]


def calculate_extra_fees(type):
    '''
    When used in transactions in > 10km radius, increase by 0.01*extra km
    When used in another state, increase by 5%
    When used internationally, increase by 15%
    '''
    if type == 0:
        return 1
    elif type == 1:
        return 1.001
    elif type == 2:
        return 1.05
    elif type == 3:
        return 1.15


def gen_values():
    '''
    Generates values based on normal distributions and does not consider previous values.
    '''
    global gcoin_values
    for _ in range(30):
        # generate a random value
        base_value = gauss(100, 70)
        # generate 24 random values
        todays_values = [gauss(base_value, 5) for _ in range(24)]
        gcoin_values.append(todays_values)
    
    return gcoin_values


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)
