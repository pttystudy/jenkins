import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json



class NcpApi():
    def __init__(self,access_key, secret_key, timestamp):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = timestamp

    def	make_signature(self,method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_call(self,):
        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"
        uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url = host+uri #https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList
        signature_key = self.make_signature(method, uri)

        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
        }
        body = {

        }
        response = requests.get(url, headers=headers)
        response = response.json()
        print(json.dumps(response, indent=2))

    def get_object_storage_list(self,):
        method = "GET"
        host = "https://kr.object.ncloudstorage.com"
        uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url = host+uri #https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList
        signature_key = self.make_signature(method, uri)

        headers = {
            "Authorization": "application/json",
            "Host": self.timestamp,
            "x-amz-date": self.access_key,
            "x-amz-content-sha256": signature_key,
            #"Content-Length": ,
        }
        body = {

        }
        response = requests.get(url, headers=headers)
        response = response.json()
        print(json.dumps(response, indent=2))

    def add_access_group_rule_inbound(self):
        #값을 불러서와서, API에 넣고, 리턴은 그냥 done : ok
        #결과적으로 내가만든 ACG에 룰이 잘 들어가는 것 까지 확인
        None