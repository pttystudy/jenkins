import json
import pandas as pd
import requests
import sys
import os
import hashlib
import hmac
import base64
import requests
import time

## 모든 NCP 서비스에 적용가능한 매우 효율적인 함수
def headers(access_key,secret_key,method,main_url,second_url):
    # key값 저장 및 더 짧고 편한 변수 사용
    akey="0EB7B1E00FAE950D38D5"
    skey="7875AE5B3AC7FC82ECEA82431B4622B60D0FBACE"

    # 숫자 타입으로 1000곱해줌
    timestamp=int(time.time()*1000)

    # 문자열로 변환
    timestamp=str(timestamp)

    # api 콜 방식 저장
    meth=method

    # 메인 url, 두번쨰 url
    m_url=main_url
    s_url=second_url

    # 전체 url
    a_url=main_url+second_url

    # 인증키 만들기
    message=meth+" "+s_url+"\n"+timestamp+"\n"+akey
    message=bytes(message,'UTF-8')
    skey=bytes(skey,'UTF-8')
    signkey=base64.b64encode(hmac.new(skey,message,digestmod=hashlib.sha256).digest())
    
    # 최종 헤더값
    headers={
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': akey,
        'x-ncp-apigw-signature-v2': signkey
    }
    return headers


#regionlist 불러오기 및 알맞은 region 선택 및 number 저장
def regionlist(headers,url):
    response=requests.get(url=url,headers=headers)
    json_data=json.loads(response.text)
    print(response.text)
    region_list=json_data["getRegionListResponse"]["regionList"]
    count=1
    for region in region_list:
        region_code=region["regionCode"]
        count=str(count)
        print(count+". "+region_code)
        count=int(count)
        count=count+1
    number=int(input("원하는 리전코드의 숫자를 눌러봐\n리전코드: "))
    print("\n\n")
    return region_list[number-1]["regionCode"]


#vpclist 불러오기 및 알맞은 vpcNo 선택 및 number 저장
def vpclist(headers,url):
    response=requests.get(url=url,headers=headers)
    json_data=response.json()
    vpclist=json_data.get("getVpcListResponse",{})
    vpclist=vpclist.get("vpcList",[])
    count=1
    for vpc in vpclist:
        vpc_no=vpc.get("vpcNo")
        count=str(count)
        print(count+". "+vpc.get("vpcName"))
        count=int(count)+1
    number=int(input("원하는 VPC의 넘버를 눌러봐\nvpc 넘버: "))
    print("\n\n")
    return vpclist[number-1]["vpcNo"]


#acglist 불러오기 및 알맞은 acgNo 선택 및 Number 저장
def acglist(headers,url):
    response=requests.get(url=url,headers=headers)
    json_data=response.json()
    acglist=json_data.get("getAccessControlGroupListResponse",{})
    acglist=acglist.get("accessControlGroupList",[])
    count=1
    for acg in acglist:
        acg_no=acg.get("accessControlGroupNo")
        count=str(count)
        print(count+". "+acg.get("accessControlGroupName"))
        count=int(count)+1
    number=int(input("원하는 ACG의 넘버를 눌러봐\nacg 넘버: "))
    print("\n\n")
    return acglist[number-1]["accessControlGroupNo"]


#acginbound rule 추가
def acginbound(headers,url):
    response=requests.get(url=url,headers=headers)
    print(response.text)

#엑셀에서 한행씩 읽어서 acg inbound url 생성
def inboundurl(regioncode,vpcno,acgNo):
    inboundfile=input("/Users/mzc01-ptty/Desktop/Python/acg.xlsx")
    df=pd.read_excel(inboundfile)
    s_url="/vserver/v2/addAccessControlGroupInboundRule?responseFormatType=json&regionCode="+regioncode+"&vpcNo="+vpcno+"&accessControlGroupNo="+acgNo
    count=1
    for index, row in df.iterrows():
        protocol_type=row['protocol']
        port_range=row['range']
        ipblock=row['ipblock']
        if protocol_type=="ICMP":
            s_url+="&accessControlGroupRuleList."+str(count)+".protocolTypeCode=ICMP&accessControlGroupRuleList."+str(count)+".ipBlock="+ipblock
        else:
            s_url+="&accessControlGroupRuleList."+str(count)+".protocolTypeCode="+protocol_type+"&accessControlGroupRuleList."+str(count)+".ipBlock="+ipblock+"&accessControlGroupRuleList."+str(count)+".portRange="+port_range
        count=count+1
    return s_url

    

      









