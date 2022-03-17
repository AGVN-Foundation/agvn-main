'''
GCOIN

contains:
- blockchain
- wallet
- network protocol (p2p at TCP port 69000)
- direct pyqt5 bindings to Wallet
'''
import hashlib

from numpy import byte_bounds
import bitcoin
import json
import pickle
from datetime import datetime
import os
import random

MAX_TRANSACTIONS = 512
MESSAGE_TYPES = ['ASCEND', 'NEW', 'DELEGATE']


class Block:
    '''
    A transaction looks like:
    {
        timestamp: datetime.datetime,
        from: gcoin_address,
        to: gcoin_address,
        value: int, # value in gcoin
        transaction_fee: int,
    }
    '''

    def __init__(self, prev_hash, transactions, merkle_root, timestamp, validator_address, signature):
        self.prev_hash = prev_hash
        self.transaction_list = transactions
        # TO implement in the header:
        # previous block's hash -> string
        # hash the transaction list with a merkle tree -> store the root
        # validator address
        # signature of validator
        # timestamp of forging
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.validator_address = validator_address
        self.signature = signature

        # TO implement in the body:
        # transaction list, list of strings
    def get_transaction_list(self):
        return self.transaction_list

    def get_timestamp(self, transaction):
        '''
        Get the timestamp of a transaction in the block.
        '''
        return self.transaction_list.get(transaction)['timestamp']


class Blockchain:
    '''
    Implementation of a blockchain, i.e. decentralized ledgering system
    '''

    def __init__(self):
        self.blockchain = []
        self.transaction_pool = []
        self.all_transactions = []

    def tampering_checks(self):
        '''
        When receive a new block, check if the merkle root actually does match the one you have
        '''
        pass

    def set_transaction_list(self, transactions):
        '''
        Add transactions to transactions list
        @transactions -> list of transactions
        '''
        self.transactions += transactions

    def make_block(self, validator_address, validator_signature, n_transactions=MAX_TRANSACTIONS):
        '''
        No hardcore cryptographic schemes required, but will use SHA-2 for now.
        Just hash all the transactions into a merkle root and include the transaction list and total block reward (sum up individual transaction rewards)

        A gcoin address requires 1500 votes to create a block.
        When a gcoin address is elected to be a validator for the next block,
        it will call this function. E.g., from the wallet system.
        '''
        transactions_to_process = self.choose_transactions(n_transactions)
        actual_len = len(transactions_to_process)
        # if even, hash everything like normal
        # if odd, duplicate the last transaction
        if actual_len % 2 == 1:
            duplicate = transactions_to_process[-1]
            transactions_to_process.append(duplicate)
            actual_len += 1

        # treat as tree -> 1D indexing
        merkle_list = []

        # in pairs [i, i+1], hash the transaction list
        for i in actual_len:
            if actual_len/i == 2:
                break

            current = json.dump(transactions_to_process[i])
            next = json.dump(transactions_to_process[i+1])
            combine = current + next
            merkle_list[i] = hashlib.sha256(combine).hexdigest()

        merkle_root = merkle_list[-1]
        prev_block = self.blockchain[-1]
        if prev_block:
            prev_hash = prev_block.merkle_root
        else:
            prev_hash = ""
        new_block = Block(prev_hash, transactions_to_process, merkle_root, datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), validator_address, validator_signature)

        return new_block

    def choose_transactions(self, n_transactions=MAX_TRANSACTIONS):
        '''
        Choose the transactions with the highest reward
        Extension: make it based on timestamp as well
        Returns a list of transactions like:
        {
            timestamp: datetime.datetime,
            from: gcoin_address,
            to: gcoin_address,
            value: int, # value in gcoin
            transaction_fee: int,
        }
        '''
        # sort transaction list in order of transaction fee
        sorted(self.all_transactions, key=lambda x: x['value'], reverse=True)
        # take n highest transaction fees
        return self.all_transactions[:n_transactions]

    def get_block(self, index=None, block_hash=None):
        '''
        @param - index INT, from 0..n-1 beginning to end
        '''
        if not index and not block_hash:
            # return the latest one
            return self.blockchain[-1]

        if index:
            return self.blockchain[index]

    def remove_block(self, block_index, cascade=True):
        '''
        Removes a block from the blockchain.
        If a block is nested between other blocks,
        the blocks succeeding it will also be destroyed if cascade = True
        '''
        if block_index > len(self.blockchain) - 1:
            return False

        if cascade:
            self.blockchain = self.blockchain[:block_index]
        else:
            # remove a block, update its successor's prev block hash
            self.blockchain.pop(block_index)
            self.blockchain[block_index].prev_hash = self.blockchain[block_index-1].merkle_root

        return True


class Credential:
    # contains gcoin addresses, public keys, and private keys

    def __init__(self, gcoin_address, public_key, private_key):
        self.credential = []
        self.credential.append((gcoin_address, public_key, private_key))


class Wallet:
    # Extension: complete the methods
    def __init__(self, network_port=21079):
        self.gcoin_addresses = [{self.create_gcoin_address(): 0}]
        self.blockchain = Blockchain()
        self.network = P2P(network_port)
        self.stake_pool = []

    def get_addresses(self):
        '''
        Get all gcoin addresses with the amount
        '''
        return self.gcoin_addresses

    def create_gcoin_address(self, password: str):
        '''
        Create a new GCoin address
        If conflicts with existing addresses (<0.00001% chance), then create another one until no conflict
        '''
        # Algorithm
        # 1. generate a public-private key pair
        # 2. hash the public key with sha256
        # 3. hash the hashed key with ripemd160
        # 4. add the result to gcoin_addresses

        private_key = hashlib.sha256(password)
        public_key = bitcoin.privtopub(private_key)
        new_address = bitcoin.pubtoaddr(public_key)

        address_object = {new_address: 0}

        if not self.gcoin_addresses[new_address]:
            self.gcoin_addresses.append(new_address)
            print(
                "DEBUG: new gcoin address successfully created!\nNew address:", new_address)
            # ? store public and private keys as well?
        else:
            self.create_gcoin_address(password)
            print("DEBUG: Something very rare just happened... creating another address")

    def make_transaction(self, sender_address, amount, receiver_address):
        '''
        Send a specified amount to a specific address
        This address can be one of your other addresses or someone else's
        '''
        # Algorithm:
        #   Send a comma separated string containing transaction amount, sender addr, receiver addr
        #   Hash the string with your private key so that it can be decrypted with your public key
        #   Broadcast the message with 'New Transaction {datetime.now}'
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"New Transaction {current_time},{amount},{sender_address},{receiver_address}"
        encrypted_message = hashlib.sha256(message).hexdigest()
        self.network.broadcast_neighbors(sender_address, encrypted_message)

    def remove_address(self, gcoin_address):
        '''
        Remove a gcoin address from your wallet
        Makes a transaction to your next address with all your current UTXO from the old address
        If you have no other address, make a new one and send it there
        '''
        self.gcoin_addresses.remove(gcoin_address)

    def edit_stakepool(self, gcoin_address, contribution, contribution_growth, stake, add=True):
        '''
        Add or Remove a gcoin address, contribution, contribution growth and stake from your stakepool.
        Normally, a node will listen on messages with 'ASCEND'. 
        '''
        if not add:
            # find the item with gcoin address
            for s in self.stake_pool:
                if gcoin_address in s:
                    self.stake_pool.remove(s)
        else:
            self.stake_pool.append(
                (gcoin_address, contribution, contribution_growth, stake))

    def validate_block(self, gcoin_address, transactions_to_include=512):
        '''
        Validate the next block in the blockchain.

        NOTE: blocks may be rejected if a new block contains a transaction belonging to previous blocks in the blockchain. 
        Since validators validate in a committee setting, they are incentivized to do the right thing and make non-conflicting or malicious blocks.
        If validators broadcast messages with bad blocks, the majority of other nodes can simply reject it and hence the validator has wasted opportunity.

        For now, generate a digital signature of your message and pass it into the block.
        '''
        message = "NEW," + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ","
        signature = hashlib.sha256(message).hexdigest()
        new_block = self.blockchain.make_block(
            gcoin_address, signature, transactions_to_include)
        # serialize the block into a string of bytes
        message += pickle.dumps(new_block)

        # broadcast new block over P2P to connected nodes
        res = self.network.broadcast_neighbors(gcoin_address, message)

        # return status, successful or unsuccessful broadcast
        return res

    # To implement:
    # method to check proof of 'contribution' -> choose validators to forge new blocks based on people's stake
    # if nodes detect some malice or tampering, they will slash a validators stake
    # can be hooked onto by the official agvn web app or anything else
    def proof_of_contribution(self, other_stakes, voter_address):
        '''
        Aggregate other nodes' contribution score and stake. This is done locally with the nodes closest to you -> Idea, people in other states with higher stakes and contributions don't get to hog the validation.

        The users with the highest %percentage staked are automatically nominated.

        Using random heuristic -> choose a validator with the highest stake, contribution growth, time staked.

        Return chosen validator's address.
        '''
        message = f'DELEGATE'
        # for nodes in stakepool, tally up their contribution and growth and staked coin and some number you want
        weights = []
        # for now, use k1-4 as 0.3, 0.3, 0.1, 0.1
        k = [0.3, 0.3, 0.1, 0.1]
        for s in self.stake_pool:
            p = k[0] * s[1] + k[1] * s[2] + k[2] * s[3] + k[3]
            weights.append(p)

        chosen_validator = random.choices(
            self.stake_pool, weights=weights, k=1)[0]
        return message + f',{chosen_validator},{voter_address}'

        '''
        This method determines who should be the validator for the next block from the stake_pool.
        Broadcast this signal out to nearby nodes.

        Nearby nodes also broadcast their choice of validator, and the validator that first gets over 1500 votes gets to make a block.
        Votes do not reset. Nodes that have been in the system for longer should have accumulated more votes and eventually everyone can be a validator for a block.

        The validator must call make_block().
        '''

    def ascend(self, gcoin_address, stake):
        '''
        Stake your coins in order to become a validator candidate. Joins the stake pool for your address.
        Creates a message of type 'ASCEND' with your gcoin address and amount to be staked.
        '''
        message = f'ASCEND,{gcoin_address},{stake}'
        return message


class P2P:
    '''
    Implementation of a Peer-to-Peer object system.
    '''

    def __init__(self, connected_nodes=[], port=69000):
        '''
        Initialize P2P object with connected node public IPv4 addresses
        '''
        self.connected_nodes = connected_nodes
        self.port = port

    def link_node(self, gcoin_address):
        '''
        Link to another node's GCoin address
        '''
        self.connected_nodes.append(gcoin_address)

    def del_node(self, gcoin_address):
        '''
        Remove a gcoin address from linked nodes
        '''
        self.connected_nodes.remove(gcoin_address)

    def set_port(self, port):
        '''
        Set a new port to communicate on
        '''
        self.port = port

    def send_dcp(self, from_address, to_address, byte_message):
        # Send a Dcp message (linux script) with the message and your network public key (not gcoin public key)
        # Extension: check send status and extend method
        os.system('p2p-send.sh ' + byte_message)

    def broadcast_neighbors(self, from_address, message):
        '''
        Converts string message to bytestream and sends the message to each connected node
        IN - from_address: address to identify with
           - message: str
        '''
        message = bytes(message)
        for connected_node in self.connected_nodes:
            self.send_dcp(from_address, connected_node, message)
