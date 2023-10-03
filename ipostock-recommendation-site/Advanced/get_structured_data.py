import requests
import pandas as pd
from bs4 import BeautifulSoup

corp_code = "419080"

def getListCorp(corp_code):
    url = "http://test.38.co.kr/forum2/dart.php?code={}".format(corp_code)

    html = requests.get(url,headers={'User-agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(html,'html.parser')
    table = soup.select('tbody>tr>td')


    slist = []
    for v in table:
        str = v.get_text()
        string = str.replace(u'\xa0', u'')
        string = string.replace(u'\u3000', u'')
        string = string.replace(u' ', u'')
        string = string.replace(u'연결포괄손익계산서',u'포괄손익계산서')
        string = string.replace(u'연결자본변동표',u'자본변동표')
        slist.append(string)

    return slist

def getDfFs(slist):

    index = []
    val = []
    k=0 

    fs_start_point = slist.index("자산")
    fs_end_point = slist.index("포괄손익계산서")
    fs_list = slist[fs_start_point:fs_end_point]

    
    for v in range(0,len(fs_list),3):
        index.append(fs_list[v])
        val.append(fs_list[v+1])
        val.append(fs_list[v+2])
        
    df_fs = pd.DataFrame(columns = ['해당연도','이전연도'])

    k=0
    for v in range(0,len(val),2):
        df_fs.loc[k] = [val[v], val[v+1]]
        k +=1
    df_fs.index = index

    return df_fs


  
def getDfIs(slist):
   
    index = []
    val = []
    k = 0

    is_start_point = slist.index("I.매출액")
    is_end_point = slist.index("자본변동표")
    is_list = slist[is_start_point:is_end_point]

    for v in range(0,len(is_list),3):
        index.append(is_list[v])
        val.append(is_list[v+1])
        val.append(is_list[v+2])

    df_is = pd.DataFrame(columns = ['해당연도','이전연도'])
    k=0
    for v in range(0,len(val),2):
        df_is.loc[k] = [val[v], val[v+1]]
        k +=1
    df_is.index = index

    return df_is
   



df_set2= getDfFs(getListCorp(corp_code))
df_set3=getDfIs(getListCorp(corp_code))
df_set2.to_excel('./엔젯_재무상태표.xlsx')
df_set3.to_excel('./엔젯_손익계산서.xlsx')
