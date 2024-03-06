import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json
import pandas as pd

class NcpApi():
    def __init__(self, access_key, secret_key, timestamp):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = timestamp
        
    def make_signature(self, method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_call(self): 
        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"
        uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url = host + uri          
        signature_key = self.make_signature(method, uri)  
        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,  # 여기서 self를 사용하여 인스턴스 변수에 접근합니다.
            "x-ncp-apigw-signature-v2": signature_key
        }

        body = {}

        response = requests.get(url, headers=headers)
        response = response.json()
        print(json.dumps(response, indent=2))
    

    def add_access_group_rule_inbound_from_excel(self, inboundfile):
        inboundfile = "/Users/mzc01-ptty/Desktop/Python/acg.xlsx"
        df = pd.read_excel(inboundfile)
    
        for index, row in df.iterrows():
            protocol_type = row['protocol']
            port_range = row['range']
            ipblock = row['ipblock']

            method = "POST"  
            host = "https://ncloud.apigw.ntruss.com"
            uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&vpcNo=31693&accessControlGroupNo=160910&responseFormatType=json"
            url = host + uri
            signature_key = self.make_signature(method, uri)

            headers = {
                "Content-Type": "application/json",
                "x-ncp-apigw-timestamp": self.timestamp,
                "x-ncp-iam-access-key": self.access_key,
                "x-ncp-apigw-signature-v2": signature_key
            }

            body = {
                "accessControlRuleConfigurationNo": 160910,
                "protocolType": protocol_type,
                "portRange": port_range,
                "ipBlock": ipblock
            }

            response = requests.post(url, headers=headers, json=body)
            response_data = response.json()
            print(json.dumps(response_data, indent=2))

        print("ACG inbound rules 추가 완료")
        return True
