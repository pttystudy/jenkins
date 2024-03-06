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
    def __init__(self, access_key, secret_key, timestamp):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = timestamp
        self.vpcNo = None
        self.acgNo = None

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

        body = "vpcNo={0}&accessControlGroupNo={1}&responseFormatType={2}".format(self.vpcNo,self.acgNo,"json")

    
        df = pd.read_excel(file_path, engine='openpyxl')
        Protocol = df['Protocol']
        ipBlock = df['Destination']
        #df['Port_Range'] = df['Port Range'].astype(int)
        portRange = df['Port Range']
        portRange = portRange.tolist() #numpy.int64 -> int


        for i in range(0,len(Protocol)):
            acg_protocol = 'accessControlGroupRuleList.{0}.protocolTypeCode='.format(i+1) + Protocol[i]
            acg_ipBlock = 'accessControlGroupRuleList.{0}.ipBlock='.format(i+1) + ipBlock[i]
            acg_portRange = 'accessControlGroupRuleList.{0}.portRange='.format(i+1) + str(portRange[i])
            body = body + "&{0}&{1}&{2}".format(acg_protocol, acg_ipBlock, acg_portRange)

        signature_key = self.make_signature(method, uri)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded', 
            'charset': 'UTF-8', 
            'Accept': '*/*',
            
            'x-ncp-apigw-timestamp': self.timestamp,
            'x-ncp-iam-access-key': self.access_key, 
            'x-ncp-apigw-signature-v2': signature_key 
        }
        #print(body)

        #method 타입에 따라 request를 요청
        try:
            response = requests.post(url, headers=headers, data=body)
            print(response.text)
            print(response.status_code, response.json)
        except Exception as ex:
            print(ex)
