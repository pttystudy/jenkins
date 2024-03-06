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
         self.access_key=access_key
         self.secret_key=secret_key
         self.timestamp=timestamp

    def	make_signature(self,method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_call(self):
        method = "GET"
        host="https://ncloud.apigw.ntruss.com"
        uri="/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url=host+uri #https://ncloud.apigw.ntruss.com/vserver/v2/getServerInstanceList

        signature_key = self.make_signature(method, uri)
        headers = {
            "Content-Type" : "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
            }
        #response = requests.get(url,headers=headers)
        #print(response.json())
        #print(json.dumps(response, indent=2))
        response = requests.get(url,headers=headers)
        response = response.json()
        print(json.dumps(response,indent=2))
    



    def add_access_group_rule_inbound(self):

    # API 요청에 필요한 매개변수 설정
        # excel=pd.read_excel('./inbound.xlsx')
        # print(excel)
        # excel.columns=[
        #     'regionCode',
        #     'vpcNo',
        #     'accessControlGroupNo',
        #     'protocolTypeCode',
        #     'ipBlock',
        #     'portRange'
        # ]
      
        # for index, row in excel.iterrows():
        #     params = {
        #         'regionCode': row['regionCode'],
        #         'vpcNo': row['vpcNo'],
        #         'accessControlGroupNo': row['accessControlGroupNo'],
        #         'accessControlGroupRuleList.1.protocolTypeCode': row['protocolTypeCode'],
        #         'accessControlGroupRuleList.1.ipBlock': row['ipBlock'],
        #         'accessControlGroupRuleList.1.portRange': row['portRange']
        #     }

            method = "GET"
            host="https://ncloud.apigw.ntruss.com"
            uri="/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&responseFormatType=json&vpcNo=45750&accessControlGroupNo=161127&accessControlGroupRuleList.N.protocolTypeCode=TCP&responseFormatType=json"
            url=host+uri 
            signature_key = self.make_signature(method, uri)
            
            headers = {
            "Content-Type" : "application/json",
            #self.timestamp 에서 timestamp로 변경
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
            }
            response = requests.get(url,headers=headers)
            response = response.json()
            print(json.dumps(response,indent=2))
            # time.sleep(15)
            
            #response = requests.get(url, params=params)
            
            # if response.status_code == 200:
            #     print(f'ACG 룰 적용 성공 {index+2}')
            # else:
            #     print(f'ACG 룰 적용 실패 {index+2}')
            #     print(response.text)

            if 'error' in response:
                print("ACG 룰 적용 실패:", response['error'])
            else:
                print("ACG 룰 적용 성공")
    
   

#실패...ㅠㅠ


    
