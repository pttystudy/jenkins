import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json

# API 엔드포인트 및 인증 정보

def make_signature(method, uri, timestamp, access_key, secret_key):
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

if __name__ == "__main__":
    method = "GET"
    host = "https://ncloud.apigw.ntruss.com"
    uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&vpcNo=31693&accessControlGroupNo=160910&responseFormatType=json"
    url = host + uri
    access_key = "0EB7B1E00FAE950D38D5"              # access key id (from portal or Sub Account)
    secret_key = "7875AE5B3AC7FC82ECEA82431B4622B60D0FBACE"              # secret key (from portal or Sub Account)
    timestamp = str(int(time.time() * 1000))
    signature_key = make_signature(method, uri, timestamp, access_key, secret_key)
    headers = {
        "Content-Type": "application/json",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature_key
    }
    
    accessControlGroupRuleList = []
for i in range(50):
    accessControlGroupRuleList.append({
        "accessControlGroupConfigurationNo": "160910",
        "protocol": "tcp",
        "portRange": "1-65535",
        "action": "accept",
        "ipBlock": "0.0.0.0/0",
        "priority": i
    })

# 요청 헤더 생성
headers = {
    "Content-Type": "application/json",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": signature_key
}

# 50개의 Inbound Rule을 10개씩 나누어 요청 보내기
batch_size = 10
for i in range(0, len(accessControlGroupRuleList), batch_size):
    batch_rules = accessControlGroupRuleList[i:i+batch_size]
    data = json.dumps({
        "region": "KR",
        "accessControlGroupInboundRuleList": batch_rules
    })

    # API 호출
    response = requests.post(url, headers=headers, data=data)

    body = {}

    response = requests.get(url, headers=headers)
    response = response.json()
    print(json.dumps(response, indent=2))
    
