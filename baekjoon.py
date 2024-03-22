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
    uri = "/vserver/v2/getServerInstanceList?regionCode=KR&responseFormatType=json"
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

    response = requests.get(url, headers=headers)
    response = response.json()
    print(json.dumps(response, indent=2))