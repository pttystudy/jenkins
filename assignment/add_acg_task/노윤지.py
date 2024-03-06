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
    def __init__(self, access_key, secret_key, timestamp,region_code, vpc_no, acg_no, excel_file_path):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = timestamp
        self.region_code = region_code
        self.vpc_no = vpc_no
        self.acg_no = acg_no
        self.excel_file_path = excel_file_path
        
    def make_signature(self, method, uri):
        self.secret_key = bytes(self.secret_key, 'UTF-8')
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def get_server_call(self):  # 이 부분에 self를 추가합니다.
        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"
        uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
        url = host + uri          
        signature_key = self.make_signature(method, uri)  # 여기서 self를 인자로 넘기지 않습니다.
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

    # def add_access_group_rule_inbound(self):
    #     #값을 불러와서 api에 넣고, 리턴은 done : ok
    #     #결과적으로 내가 만든 acg의 룰이 잘 들어가는 것 까지 확인
    #     None
    def add_access_group_rule_inbound(self, region_code, vpc_no, acg_no, excel_file_path):
        apicall_method = "POST"
        space = " "
        new_line = "\n"
        host = "https://ncloud.apigw.ntruss.com"
        api_url = f"/vserver/v2/addAccessControlGroupInboundRule"
        api_url += f"?accessControlGroupNo={acg_no}&regionCode={region_code}&vpcNo={vpc_no}"

        # 엑셀 파일 읽기
        df = pd.read_excel(excel_file_path)

        for idx, row in df.iterrows():
            acg_url = f"&accessControlGroupRuleList.{idx + 1}.protocolTypeCode={row['Protocol']}" \
                      f"&accessControlGroupRuleList.{idx + 1}.ipBlock={row['IPBlock']}" \
                      f"&accessControlGroupRuleList.{idx + 1}.portRange={row['PortRange']}" 
                    #   f"&accessControlGroupRuleList.{idx + 1}.Description={row['Description']}"  description적용이 반영이 안됨 ㅠㅠ

            api_url += acg_url

        message = apicall_method + space + api_url + new_line + self.timestamp + new_line + self.access_key
        message = bytes(message, 'UTF-8')

        # signature_key = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        signature_key = self.make_signature(apicall_method, api_url)    
        http_header = {
            'x-ncp-apigw-timestamp': self.timestamp,
            'x-ncp-iam-access-key': self.access_key,
            'x-ncp-apigw-signature-v2': signature_key
        }

        response = requests.post(host + api_url, headers=http_header)

        if response.status_code == 200:
            print(f"ACG Inbound Rules 추가 성공!! (ACG No: {acg_no})")
        else:
            print(f"오류 발생: {response.status_code} - {response.text}")

