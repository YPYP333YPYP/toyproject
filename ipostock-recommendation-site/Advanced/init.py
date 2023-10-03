from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os
import re
import json

api_key = "fb3196b97e3d77f755d9b061764117e1fa6e3596"
url = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}'.format(api_key)

""" 
고유번호 개발가이드 
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018 
"""

# 압축 해제 과정
with urlopen(url) as zipres:
    with ZipFile(BytesIO(zipres.read())) as zf:
        zf.extractall('corp_num')

# CORPCODE.xml 파일 읽기
tree = ET.parse('./corp_num/CORPCODE.xml')
root = tree.getroot()

def findByCorpNum(find_name):
    for country in root.iter("list"):
        if country.findtext("corp_name") == find_name:
            return country.findtext("corp_code")

# corp_name = input()
corp_name = '산돌'
report_nm = "투자설명서"
corp_code = findByCorpNum(corp_name)


"""
투자설명서 - 재무제표 개발가이드
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
"""



# 기업 rcept_no 
rcept_no_url = 'https://opendart.fss.or.kr/api/list.json?crtfc_key={}&corp_code={}&bgn_de=20100101&page_no=1'.format(api_key,corp_code)
response = requests.get(rcept_no_url)
wp = response.content.decode('utf-8')

report_nm_list = re.findall(r'report_nm":"(.*?)"',wp)
rcept_no_list = re.findall(r'rcept_no":"(.*?)"',wp)
dict(zip(report_nm_list, rcept_no_list))

# 기업 dcm_no 
dcm_no_list =[]
for rcept_no in rcept_no_list:
    resp_dcm = requests.get("http://dart.fss.or.kr/dsaf001/main.do?rcpNo={}".format(rcept_no))
    wp_dcm = resp_dcm.content.decode('utf-8')
    dcm_no = re.findall(r"{}','(.*?)',".format(rcept_no),wp_dcm[0])
    dcm_no_list.append(dcm_no)

URL = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json'
PARAMS = {
  'crtfc_key': api_key, # API 인증키
  'corp_code': corp_code, # 삼성전자 고유번호
  'bsns_year': '2022', # 사업연도(4자리)
  'reprt_code': '11011', # 사업보고서
}

resp = requests.get(url = URL, params = PARAMS)
data_json = resp.json()

df = pd.json_normalize(data_json)
print(df)