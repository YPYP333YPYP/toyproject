from urllib import response
import requests
import pandas as pd
import os
import zipfile
from bs4 import BeautifulSoup
from get_corp_code import findByCorpNum

api_key = 'fb3196b97e3d77f755d9b061764117e1fa6e3596'
url_json = "https://opendart.fss.or.kr/api/list.json"
url_xml = "https://opendart.fss.or.kr/api/list.xml"
stock_code = "064540"

corp_code = findByCorpNum("티에프이")
print(corp_code)
params1 = {
    'crtfc_key' : api_key,
    'corp_code' : corp_code,
    'bgn_de' : '20100801',
    'end_de' : '20221101'
}

response = requests.get(url_json, params=params1)
data = response.json()

data_list = data.get('list')
df_list = pd.DataFrame(data_list)

df_list = df_list[df_list['report_nm'].str.contains('증권신고서')]
row = df_list.iloc[1]
rcept_no = row.loc['rcept_no']
url = "https://opendart.fss.or.kr/api/document.xml"

params2 = {
    'crtfc_key' : api_key,
    'rcept_no' : rcept_no
}


os_path = 'document.zip'
if os.path.exists(os_path):
    os.remove(os_path)
doc_zip_path = os.path.abspath('./document.zip')

if not os.path.isfile(doc_zip_path):
    response = requests.get(url, params=params2)
    with open(doc_zip_path, 'wb') as fp:
        fp.write(response.content)

zf = zipfile.ZipFile(doc_zip_path)
zf.extractall()

file = "./"+rcept_no+".xml"



def file_open(file):
    #파일 읽기
    rawdata = open(file, 'r', encoding='utf-8' )

    data = rawdata.read()
    return data


def load_content(file):
    string = ""
    data = file_open(file)
    soup = BeautifulSoup(data, "lxml")
    data = soup.select('p')
    for item in data :
        pdata = item.text
        if pdata.find("사업") != -1:
            if pdata.find("증권") == -1:
                if pdata.find("재무") == -1:
                    if pdata.find("주주") == -1:
                        if pdata.find("투자") == -1:
                            string += str(pdata)
            
    return string

print(load_content(file))