from tronapi import keys
from tronapi.keys import PrivateKey
from tronapi.defaults import conf_for_name
import requests
import json
from tronapi import TRX

DEFAULT_CONF = {
    'fee_limit': 10_000_000,
    'timeout': 10.0,  # in second
}


class Tronapi(object):
    conf = {
        'fee_limit': 10_000_000,
        'timeout': 10_000_000,
        'fullnode': "https://api.trongrid.io",
    }
    network = ""

    def __init__(self, network: str = "mainnet", priv_key: str = None, owner: str = None):
        self.conf = DEFAULT_CONF
        self.conf['fullnode'] = conf_for_name(network)['fullnode']
        if priv_key is not None:
            self.priv_key = PrivateKey(bytes.fromhex(priv_key))
        if owner is not None:
            self.owner = owner
        # print(conf_for_name(network))

    # 冻结 文档 https://cn.developers.tron.network/reference#%E5%86%BB%E7%BB%93%E8%B4%A6%E6%88%B7
    def freeze_balance(self, owner: str = None, amount: int = 1, resource: str = "ENERGY", receiver: str = None):
        payload = {
            "frozen_balance": amount * TRX,
            "frozen_duration": 3,
            "resource": resource,
        }

        if owner is not None:
            payload["owner_address"] = keys.to_hex_address(owner)
        else:
            payload["owner_address"] = keys.to_hex_address(self.owner)

        if receiver is not None and keys.to_hex_address(receiver) != payload["owner_address"]:
            payload["receiver_address"] = keys.to_hex_address(receiver)
        response = self.build(action="/wallet/freezebalance", data=payload)
        return response

    # 解冻
    def unfreeze_balance(self, owner: str = None, resource: str = "ENERGY", receiver: str = None):
        payload = {
            "resource": resource,
        }

        if owner is not None:
            payload["owner_address"] = keys.to_hex_address(owner)
        else:
            payload["owner_address"] = keys.to_hex_address(self.owner)

        if receiver is not None:
            payload["receiver_address"] = keys.to_hex_address(receiver)
        response = self.build(action="/wallet/unfreezebalance", data=payload)
        return response

    # trx转账
    def sendTrx(self, owner: str= None, amount: int=0, receiver: str = None):
        payload = {
            "amount": amount * TRX,
            "to_address": keys.to_hex_address(receiver),
        }

        if owner is not None:
            payload["owner_address"] = keys.to_hex_address(owner)
        else:
            payload["owner_address"] = keys.to_hex_address(self.owner)

        response = self.build(action="/wallet/createtransaction", data=payload)
        return response

    # 投票
    def vote_witness_account(self, owner: str = None, vote_address: str = None,vote_count:int=1):
        payload = {
            "votes": [
                {
                    "vote_address": keys.to_hex_address(vote_address),
                    "vote_count": vote_count,
                }
            ]
        }
        if owner is not None:
            payload["owner_address"] = keys.to_hex_address(owner)
        else:
            payload["owner_address"] = keys.to_hex_address(self.owner)
        response = self.build(action="/wallet/votewitnessaccount", data=payload)
        return response

    # 获取账号 getaccount
    def getaccount(self, owner: str = None):
        payload = {
            "address": keys.to_hex_address(self.owner),
        }
        if owner is not None:
            payload["address"] = keys.to_hex_address(owner)
        response = self.request(action="/wallet/getaccount", data=payload)
        return response

    # 查看一个账户给哪些账户代理了资源.
    def GetDelegatedResourceAccountIndex(self, ):
        payload = {
            "value": keys.to_hex_address(self.owner),
        }
        response = self.request(action="/wallet/getdelegatedresourceaccountindex", data=payload)
        return response

    # 查看一个账户代理给另外一个账户的资源情况.
    def GetDelegatedResource(self, toAddress:str):
        payload = {
            "fromAddress": keys.to_hex_address(self.owner),
            'toAddress':keys.to_hex_address(toAddress),
        }
        response = self.request(action="/wallet/getdelegatedresource", data=payload)
        return response

    # GetAccountResource  查询账户的资源信息（带宽，能量）
    def getaccountresource(self,owner: str = None ):
        payload = {
            "address": keys.to_hex_address(self.owner),
        }
        if owner is not None:
            payload["address"] = keys.to_hex_address(owner)
        response = self.request(action="/wallet/getaccountresource", data=payload)
        return response

    def getConfirmedCurrentBlock(self, ):
        response = self.request(action="/walletsolidity/getnowblock",data={})
        return response

    def getWalletsolidityBlockByNum(self,num ):
        response = self.request(action="/walletsolidity/getblockbynum", data={'num': num})
        return response

    def build(self, action: str, data: None):
        response = self.request(action, data=data)
        if response.get("Error"):
            return {'response': response}
        response = self.sign(response)
        broadcast = self.broadcast(response)
        return {'response': response, 'broadcast': broadcast}

    # 签名
    def sign(self, request: None):
        sig = self.priv_key.sign_msg_hash(bytes.fromhex(request['txID']))
        request['signature'] = sig.hex()
        return request

    # 广播
    def broadcast(self, request: None):
        return self.request(action="/wallet/broadcasttransaction", data=request)

    def request(self, action: str, data: None):
        response = requests.post(self.conf['fullnode'] + action, json=data)
        return response.json()
