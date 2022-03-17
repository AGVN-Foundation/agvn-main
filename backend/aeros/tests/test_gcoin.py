'''
Tests for GCoin backend
'''
from ..gcoin import Block, Blockchain, Wallet, P2P


def test_basic_instantiation():
    block = Block([], '121412', None, 'address_1', 'signed')
    blockchain = Blockchain()
    wallet = Wallet()
    network = P2P()


def test_blockchain():
    blockchain = Blockchain()
    block = blockchain.make_block(validator_address='21421421',
                                  validator_signature='signed2')

    assert block == []


def test_wallet():
    wallet = Wallet()
    address = wallet
    wallet.make_transaction('1cassafs', 50, 'afq0022f12')
