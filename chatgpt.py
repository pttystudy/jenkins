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
    params = {
        "regionCode": "KR",
        "vpcNo": "31693",
        "accessControlGroupNo": "160910",
        "responseFormatType": "json"
    }
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

    body = {}

    try:
        response = requests.get(url, headers=headers, params=uri)

        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        response = response.json()
        print(json.dumps(response, indent=2))
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 오류 발생: {err}")
    except requests.exceptions.RequestException as err:
        print(f"요청 예외 발생: {err}")
    except json.decoder.JSONDecodeError as err:
        print(f"JSON 디코딩 오류: {err}")
