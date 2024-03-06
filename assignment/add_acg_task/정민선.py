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


    def make_signature(self,method,uri):
        if isinstance(self.secret_key, str):  # self.secret_key가 문자열인 경우에만 인코딩을 수행합니다.
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
        
        
        signature_key = self.make_signature(method,uri)

        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
        }
        body ={
        }
        response = requests.get(url, headers=headers)
        response = response.json()
        print(json.dumps(response, indent=2))


    def add_access_group_rule_inbound(self,):
        ## 수행 필요 내용 ##
        #값을 불러서와서, API에 넣고, 리턴은 그냥 done : ok
        #결과적으로 내가만든 ACG에 룰이 잘 들어가는 것 까지 확인

      
        myvpc = '44159'
        groupNo = '122641'
        bundle = [              ## 값 불러오는 부분 재작성 필요
                ('TCP', '10.10.10.10/32', 5),
                ('TCP', '10.11.10.10/32', 5),
                ('TCP', '10.12.10.10/32', 5),
                ('TCP', '10.13.10.10/32', 5),
                ('TCP', '10.14.10.10/32', 5),
                ('TCP', '10.15.10.10/32', 5),
                ('TCP', '10.16.10.10/32', 5),
                ('TCP', '10.17.10.10/32', 5),
                ('TCP', '10.18.10.10/32', 5),
                ('TCP', '10.19.10.10/32', 5),
                ('TCP', '10.20.10.10/32', 5),
                ('TCP', '10.21.10.10/32', 5),
                ('TCP', '10.22.10.10/32', 5),
                ('TCP', '10.23.10.10/32', 5),
                ('TCP', '10.24.10.10/32', 5),
                ('TCP', '10.25.10.10/32', 5),
                ('TCP', '10.26.10.10/32', 5),
                ('TCP', '10.27.10.10/32', 5),
                ('TCP', '10.28.10.10/32', 5),
                ('TCP', '10.29.10.10/32', 5),
                ('TCP', '10.30.10.10/32', 5),
                ('TCP', '10.31.10.10/32', 5),
                ('TCP', '10.32.10.10/32', 5),
                ('TCP', '10.33.10.10/32', 5),
                ('TCP', '10.34.10.10/32', 5),
                ('TCP', '10.35.10.10/32', 5),
                ('TCP', '10.36.10.10/32', 5),
                ('TCP', '10.37.10.10/32', 5),
                ('TCP', '10.38.10.10/32', 5),
                ('TCP', '10.39.10.10/32', 5),
                ('TCP', '10.40.10.10/32', 5),
                ('TCP', '10.41.10.10/32', 5),
                ('TCP', '10.42.10.10/32', 5),
                ('TCP', '10.43.10.10/32', 5),
                ('TCP', '10.44.10.10/32', 5),
                ('TCP', '10.45.10.10/32', 5),
                ('TCP', '10.46.10.10/32', 5),
                ('TCP', '10.47.10.10/32', 5),
                ('TCP', '10.48.10.10/32', 5),
                ('TCP', '10.49.10.10/32', 5),
                ('TCP', '10.50.10.10/32', 5),
                ]

        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"

        for index, rule in enumerate(bundle,start=1):
            protocolTypeCode, ipBlock, portRange = rule
            print("bundle {}: Protocol Type = {}, IP Block = {}, Port Range = {}".format(index, protocolTypeCode, ipBlock, portRange))  

            #인바운드 생성
            uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&responseFormatType=json&vpcNo=" + str(myvpc) + "&accessControlGroupNo=" + str(groupNo) + "&accessControlGroupRuleList.1.protocolTypeCode=" + protocolTypeCode + "&accessControlGroupRuleList.1.ipBlock=" + ipBlock  + "&accessControlGroupRuleList.1.portRange=" + str(portRange) 

            #인바운드 삭제
            #uri = "/vserver/v2/removeAccessControlGroupInboundRule?regionCode=KR&responseFormatType=json&vpcNo=" + str(myvpc) + "&accessControlGroupNo=" + str(groupNo) + "&accessControlGroupRuleList.1.protocolTypeCode=" + protocolTypeCode + "&accessControlGroupRuleList.1.ipBlock=" + ipBlock  + "&accessControlGroupRuleList.1.portRange=" + str(portRange) 

            url = host + uri    

            signature_key = self.make_signature(method, uri)
            
            headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
            }
            
            reponse = requests.get(url, headers=headers)
            res_json = json.dumps(reponse.json(), ensure_ascii=False, indent=4)
            print(res_json) 
            time.sleep(7)


        ####### 추가 확인 필요 내용 ###########
        # 1. 엑셀을 통해 값을 불러오는 방법
        # 2. 수량 증가되어도 겹치지 않게 생성되는 방법
        
        ######### 시간 간격을 안두면 아래와 같은 메세지 발생 ############
        # "responseError": {
        # "returnCode": "1007009",
        # "returnMessage": "If Acg settings are changing, you cannot change other settings at the same time."
        # }

