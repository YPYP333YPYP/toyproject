import pandas as pd
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import warnings
from time import strftime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import requests
import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc
from datetime import datetime, timedelta
from io import BytesIO
import base64
from html2image import Html2Image
import cv2


from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

df = pd.read_excel('./corp_code.xlsx')
df_list_corp_name = pd.DataFrame(df, columns=['기업명','종목코드'])



stock_code = '330350'

def get_stock_data(stock_code):
    stock_df = pd.DataFrame()
    stock_url = 'https://finance.naver.com/item/sise_day.nhn?code={}'.format(stock_code)  

    for page in range(1, 70):
        url = '{}&page={}'.format(stock_url, page)  
        html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
        stock_df = stock_df.append(pd.read_html(html, header=0)[0])       

    stock_df = stock_df.dropna()
    stock_df = stock_df.drop_duplicates()

    stock_df = pd.DataFrame(stock_df, columns=['날짜','종가'])
    stock_df = stock_df.sort_values('날짜')
    
    

    return stock_df


def get_stock_category(stock_code):
    category_url = "https://finance.naver.com/item/main.naver?code={}".format(stock_code)
    html = requests.get(category_url,headers={'User-agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(html,'html.parser')
    div = soup.find('div', class_ = "section trade_compare")
    if div == None:
        category = None;
    else:
        category = div.find('a').text
    return category



df_category = pd.read_excel('./corp_code_up_category.xlsx')


set1 = df_category[(df_category['업종'] == '생명과학도구및서비스')]
set2 = df_category[(df_category['업종'] == '전기제품')]
set3 = df_category[(df_category['업종'] == '게임엔터테인먼트')]
set4 = df_category[(df_category['업종'] == '반도체와반도체장비')]


df_set1 = pd.DataFrame()
warnings.filterwarnings(action='ignore')

slist = []



# for v in set4['종목코드']:
#     df = get_stock_data(v)['종가']
#     slist = df.values.tolist()

#     se = pd.Series(slist)

#     df_set1[v] = se 

# df_set1.to_excel('./set4.xlsx')

df_set1 = pd.read_excel('./set4.xlsx')

ret = df_set1.pct_change(1)
ret = ret.sum(axis=1)
cum_ret = ((ret+1).cumprod()) - 1







fig = plt.figure()

plt.plot(cum_ret)

plt.xlabel('상장 이후 경과 일')
plt.ylabel("누적 수익률")
plt.title("업종 : 반도체와반도체장비 ")


tmpfile = BytesIO()
fig.savefig(tmpfile, format='png')
encoded = base64.b64encode(tmpfile.getvalue()).decode('EUC-KR')

html = f'<img src=\'data:image/png;base64,{encoded}\'>'

hti = Html2Image()
hti = Html2Image(output_path='static/image')

hti.screenshot(html_str=html, save_as='chart.png')
img = cv2.imread('static/image/chart.png')
re_img = img[10:480,10:640]
cv2.imwrite('static/image/chart.png',re_img)
