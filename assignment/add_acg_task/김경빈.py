import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json

class NcpApiStudy():
    def __init__(self, access_key, secret_key, timestamp):
        self.access_key =access_key
        self.secret_key = secret_key
        self.timestamp = timestamp

    def make_signature(self, method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new( self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_call(self):

        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"
        uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url = host+uri
        #? uri = https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json
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
        
    def add_access_group_rule_inbound(self):  
        
        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"
        vpcNo = str(43900)
        acgNo = str(121834)
        protocolType = "TCP"
        ip = "8.29.230.224/32"
        
        #for port in range(1, 51):
        for port in range(1, 5):             #* 테스트
            uri = ( "/vserver/v2/addAccessControlGroupInboundRule"
                    "?regionCode=KR"
                    "&vpcNo=" + vpcNo +
                    "&accessControlGroupNo=" + acgNo + 
                    "&accessControlGroupRuleList.1.protocolTypeCode=" + protocolType +
                    "&accessControlGroupRuleList.1.ipBlock=" + ip +
                    "&accessControlGroupRuleList.1.portRange=" + str(port) +
                    "&responseFormatType=json" ) 
            url = host + uri

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

            time.sleep(15) 
