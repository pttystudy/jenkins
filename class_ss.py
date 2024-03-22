import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json
import pandas as pd

class CallNcpApi():
    # 생성자
    def __init__(self, access_key, secret_key, timestamp, vpcNo, acgNo):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = timestamp
        self.vpcNo = vpcNo
        self.acgNo = acgNo

    # Signature Key 생성
    def	make_signature(self,method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')

        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_list(self):
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
        return None
    
    def add_access_group_rule_inbound(self, vpcNo, acgNo, file_path):
        method = "POST"
        self.vpcNo = vpcNo
        self.acgNo = acgNo
        host = "https://ncloud.apigw.ntruss.com"
        uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR"
        url = host + uri

        df = pd.read_excel(file_path, engine='openpyxl')

        data = {
            "vpcNo": self.vpcNo,
            "accessControlGroupNo": self.acgNo,
            "responseFormatType": "json",
            "accessControlGroupRuleList": []
        }

        for index, row in df.iterrows():
            accessControlGroupRule = {
                "protocolTypeCode": row['Protocol'],
                "ipBlock": row['Destination'],
                "portRange": str(row['Port Range'])
            }
            data["accessControlGroupRuleList"].append(accessControlGroupRule)

        signature_key = self.make_signature(method, uri)

        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
        }

        try:
                response = requests.post(url, headers=headers, data=body)
                print(response.text)
                print(response.status_code, response.json)
        except Exception as ex:
                print(ex)