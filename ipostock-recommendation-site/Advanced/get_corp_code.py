from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import xml.etree.ElementTree as ET
import pandas as pd

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

