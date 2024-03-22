import pandas as pd
from class_s import NcpApi
import time

access_key = "0EB7B1E00FAE950D38D5"
secret_key = "7875AE5B3AC7FC82ECEA82431B4622B60D0FBACE"             
timestamp = str(int(time.time() * 1000)) 
    
def process_excel_for_inbound_rules(file_path):
    """
    엑셀 파일을 읽어들여서 add_access_group_rule_inbound 함수에서 사용할 형식으로 데이터를 처리합니다.
    
    Args:
    - file_path (str): 엑셀 파일의 경로
    
    Returns:
    - list: ACG inbound rule 데이터를 담은 리스트
    """
    inbound_rules = []
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        rule = {
            "accessControlGroupNo": row['accessControlGroupNo'],
            "protocolType": row['protocolType'],
            "ipBlock": row.get('ipBlock', ''),  # Conditional 필드이므로 없을 수도 있음
            "accessControlGroupSequence": row.get('accessControlGroupSequence', ''),  # Conditional 필드이므로 없을 수도 있음
            "portRange": row.get('portRange', ''),  # Conditional 필드이므로 없을 수도 있음
            "accessControlGroupRuleType": row['accessControlGroupRuleType'],
            "accessControlGroupRuleDescription": row['accessControlGroupRuleDescription']
        }
        inbound_rules.append(rule)
    return inbound_rules

class NcpApi():

    def add_access_group_rule_inbound_from_excel(self, file_path):
        """
        엑셀 파일에서 ACG inbound rule을 읽어와서 추가합니다.
        
        Args:
        - file_path (str): ACG inbound rule이 정의된 엑셀 파일의 경로
        
        Returns:
        - bool: ACG inbound rule 추가 결과
        """
        inbound_rules = process_excel_for_inbound_rules(file_path)
        for rule in inbound_rules:
            # rule을 이용하여 ACG inbound rule을 추가하는 코드를 작성
            # 예를 들어, rule의 필드들을 이용하여 API 호출을 수행하는 등의 작업 수행
            print("Adding ACG inbound rule:", rule)
            # 실제로 API 호출이나 데이터 처리를 수행하는 코드를 작성해야 함
        return True  # 추가 작업이 성공했다고 가정

# 예시로 사용할 엑셀 파일 경로
excel_file_path = "/Users/mzc01-ptty/Desktop/Python/acg.xlsx"

# NcpApi 인스턴스 생성
api = NcpApi(access_key, secret_key, timestamp)

# 엑셀 파일에서 ACG inbound rule 추가
result = api.add_access_group_rule_inbound_from_excel(excel_file_path)

if result:
    print("ACG inbound rules 추가 완료")
else:
    print("ACG inbound rules 추가 실패")
