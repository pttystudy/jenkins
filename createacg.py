import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json


def make_signature(method, uri, timestamp, access_key, secret_key):
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

if __name__ == "__main__":
    method = "GET" 
    host = "https://ncloud.apigw.ntruss.com"
    uri = "/vserver/v2/addAccessControlGroupInboundRule"
    access_key = "0EB7B1E00FAE950D38D5"              # access key id (from portal or Sub Account)
    secret_key = "7875AE5B3AC7FC82ECEA82431B4622B60D0FBACE"              # secret key (from portal or Sub Account)
    timestamp = str(int(time.time() * 1000))

    # 서명 생성
    signature_key = make_signature(method, uri, timestamp, access_key, secret_key)

    headers = {
        "Content-Type": "application/json",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": signature_key
    }

    # 요청 파라미터
    params = {
        "regionCode": "KR",
        "vpcNo": "31693",
        "accessControlGroupNo": "160910",
        "responseFormatType": "json"
    }

    # 50개의 규칙을 추가하는 요청 생성
    for i in range(1, 2):
        params[f"accessControlGroupRuleList.{i}.protocolTypeCode"] = "TCP"
        params[f"accessControlGroupRuleList.{i}.ipBlock"] = "10.0.0.0/16"
        params[f"accessControlGroupRuleList.{i}.portRange"] = "80"

        # API 호출
        url = host + uri
        response = requests.get(url, headers=headers, params=params)  # POST 메서드 사용

        # 결과 확인
        if response.status_code == 200:
            print(f"규칙 {i}이(가) 추가되었습니다.")
        else:
            print(f"규칙 {i} 추가 중 오류 발생: {response.status_code} - {response.text}")
