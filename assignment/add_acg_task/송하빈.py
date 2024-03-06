import sys
import os
import hashlib
import hmac
import base64
import requests
import time
import json

class NcpApi():
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timestamp = str(int(time.time() * 1000))

    def make_signature(self, method, uri):
        if not isinstance(self.secret_key, bytes):
            self.secret_key = bytes(self.secret_key, 'UTF-8')

        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(self.secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def add_access_group_rule_inbound(self, protocol, ip_block, port_range=None):
        method = "GET"
        host = "https://ncloud.apigw.ntruss.com"

        # URI 조합
        uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&vpcNo=45750&accessControlGroupNo=127420"
        uri += "&accessControlGroupRuleList.1.protocolTypeCode=" + str(protocol)
        uri += "&accessControlGroupRuleList.1.ipBlock=" + str(ip_block)

        if port_range is not None:
            uri += "&accessControlGroupRuleList.1.portRange=" + str(port_range)

        uri += "&responseFormatType=json"

        url = host + uri
        signature_key = self.make_signature(method, uri)

        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature_key
        }

        response = requests.get(url, headers=headers)
        response = response.json()
        print(json.dumps(response, indent=2))
        time.sleep(15)