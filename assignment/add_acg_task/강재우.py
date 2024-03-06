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
    def __init__(self, access_key, secret_key, timestamp,excel_path):
         self.access_key=access_key
         self.secret_key=secret_key
         self.timestamp=timestamp
         self.excel_path=excel_path

    def make_signature(self,method, uri):       
        if not isinstance(self.secret_key, bytes):
              self.secret_key = bytes(self.secret_key, 'UTF-8')
        # 타임스탬프 갱신
        self.timestamp = str(int(time.time() * 1000))
        message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key     
        #message = method + " " + uri + "\n" + self.timestamp + "\n" + self.access_key
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

    def my_list_data(self,df,key):
        initial_value = 0
        df_length = len(df)
        my_list_data = [initial_value for _ in range(df_length)]
        temp_count = 0
        
        for i in my_list_data:
            my_list_data[temp_count] = df.loc[temp_count, key]
            temp_count = temp_count + 1
        return my_list_data

    def acg_rule_add_inbound(self):
        #값을 불러와서 API에 넣고 리턴은 그냥 done : ok
        #결과적으로 내가 만든 ACG에 잘 들어가는 것 까지 확인
        #과제 해오면 커피 사준다고 함
        df_protocol = pd.read_excel(io=self.excel_path,sheet_name='Sheet1',skiprows=1,usecols='B,C,D,E')
        df_protocol = df_protocol.dropna()

        # my_list_data 함수 호출 , 모든 데이터 값 변수 리스트에 저장
        my_list_data_inout = self.my_list_data(df_protocol, 'in/out')
        my_list_data_protocol = self.my_list_data(df_protocol, 'protocol')
        my_list_data_sourceIP = self.my_list_data(df_protocol, 'sourceip')
        my_list_data_port = self.my_list_data(df_protocol, 'port')

        # 2. E 열의 값이 정수이면 True, 그 외 값은 False로 bool1 값에 저장.
        # 이렇게 하는 이유는 정수 값은 문자열 값으로 변환해줘야해서,,,
        bool1 = isinstance(df_protocol['port'],int)
        if bool1 == "True":
              df_protocol['port'] = df_protocol['port'].astype(int).astype(str)
		
        # 엑셀 상 source ip가 0.0.0.0이면 문자열을 0.0.0.0/0으로 변환
        for i in range(len(my_list_data_inout)):
            
            if '0.0.0.0' in str(my_list_data_sourceIP[i]):
                   my_list_data_sourceIP[i] = str(my_list_data_sourceIP[i]).replace("0.0.0.0", "0.0.0.0/0")


        # 엑셀 상 뒤에 서브넷 마스크가 있으면 패스, 그냥 IP만 있으면 /32로 문자열 변환
            elif any(subnet_mask in str(my_list_data_sourceIP[i]) for subnet_mask in ['/10', '/11', '/12', '/13', '/14','/15','/16', '/17', '/18', '/19', '/20','/21','/22','/23','/24', '/25', '/26', '/27', '/28','/29','/30','31']):
                pass
            else:
                my_list_data_sourceIP[i] = str(my_list_data_sourceIP[i]) + "/32"
            
            if my_list_data_inout[i].casefold() == "inbound":
                  # Inbound 이고, protocol이 icmp 일 때 uri에서 &accessControlGroupRuleList.1.portRange= 제외
                            if my_list_data_protocol[i].casefold() == "icmp":
                                  uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&vpcNo=45750&accessControlGroupNo=127420&accessControlGroupRuleList.1.protocolTypeCode="+str(my_list_data_protocol[i])+"&accessControlGroupRuleList.1.ipBlock="+str(my_list_data_sourceIP[i])+"&responseFormatType=json"

                            else:
                                  uri = "/vserver/v2/addAccessControlGroupInboundRule?regionCode=KR&vpcNo=45750&accessControlGroupNo=127420&accessControlGroupRuleList.1.protocolTypeCode="+str(my_list_data_protocol[i])+"&accessControlGroupRuleList.1.ipBlock="+str(my_list_data_sourceIP[i])+"&accessControlGroupRuleList.1.portRange="+str(my_list_data_port[i])+"&responseFormatType=json"
            elif my_list_data_inout[i].casefold() == "outbound":
			# Outbound이고, protocol이 icmp 일 때 uri에서 portrange 제외
                            if my_list_data_protocol[i].casefold() == "icmp":
                                  uri = "/vserver/v2/addAccessControlGroupOutboundRule?regionCode=KR&vpcNo=45750&accessControlGroupNo=127420&accessControlGroupRuleList.1.protocolTypeCode="+str(my_list_data_protocol[i])+"&accessControlGroupRuleList.1.ipBlock="+str(my_list_data_sourceIP[i])+"&responseFormatType=json"
                            else:
                                  uri = "/vserver/v2/addAccessControlGroupOutboundRule?regionCode=KR&vpcNo=45750&accessControlGroupNo=127420&accessControlGroupRuleList.1.protocolTypeCode="+str(my_list_data_protocol[i])+"&accessControlGroupRuleList.1.ipBlock="+str(my_list_data_sourceIP[i])+"&accessControlGroupRuleList.1.portRange="+str(my_list_data_port[i])+"&responseFormatType=json"
            
            # timestamp expired 에러로 인해 수동 생성

            method = "GET"
            host="https://ncloud.apigw.ntruss.com"
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
            time.sleep(15)

        None
