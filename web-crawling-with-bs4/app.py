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


def get_stock():
    stock_df = pd.DataFrame()
    stock_url = 'https://finance.naver.com/item/sise_day.nhn?code=011200'  
    for page in range(1, 7):
        url = '{}&page={}'.format(stock_url, page)  
        html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
        stock_df = stock_df.append(pd.read_html(html, header=0)[0])       

    stock_df = stock_df.dropna()
    stock_df.iloc[0:30]
    stock_df = stock_df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
    stock_df = stock_df.sort_values('Date')
    stock_df['Date'] = stock_df['Date'].str.replace(pat='.',repl='',regex=False)
    plot_df = stock_df[['Open', 'High', 'Low', 'Close', 'Volume']]




    fig = plt.figure(figsize=(10,7))
    fig.set_facecolor('w')
    gs = gridspec.GridSpec(2,1,height_ratios=[3,1])

    axes = []
    axes.append(plt.subplot(gs[0]))
    axes.append(plt.subplot(gs[1], sharex=axes[0]))
    axes[0].get_xaxis().set_visible(False) 

    x = np.arange(len(plot_df.index))
    ohlc = plot_df[['Open', 'High', 'Low', 'Close']].astype(int).values
    dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))
    candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')
    axes[1].bar(x, plot_df.Volume, color='g', width=0.6, align='center')
    axes[0].set_title('HMM Stock Chart')

    xticks = []
    xlabels = []

    for x, d in zip(x, stock_df.Date.values):
        if x % 3 == 0:
            xticks.append(x)
            xlabels.append(datetime.strptime(str(d), '%Y%m%d').strftime('%m/%d'))

    axes[1].set_xticks(xticks)
    axes[1].set_xticklabels(xlabels, rotation=45 )

    plt.tight_layout()

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('EUC-KR')

    html = f'<img src=\'data:image/png;base64,{encoded}\'>'

    hti = Html2Image()
    hti = Html2Image(output_path='static/image')
    
    hti.screenshot(html_str=html, save_as='chart.png')
    img = cv2.imread('static/image/chart.png')
    re_img = img[10:700,10:1000]
    cv2.imwrite('static/image/chart.png',re_img)


def get_investor():
    investor_url = 'https://finance.naver.com/item/main.naver?code=011200'
    html = requests.get(investor_url,headers={'User-agent': 'Mozilla/5.0'}).content
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('div',class_="sub_section right")
    tb = table.find_all('th')
    date =[]
    for v in tb:
        date.append(v.get_text())
    date = date[5:11]


    val = []
    val = table.select('em')
    data = []
    for v in range(0,len(val)):
        if (v) % 4 != 1: 
            i = (val[v].text).strip('\n,\t')
            data.append(i)
    price = []
    foreigner = []
    agency = []
    for i in range(0,len(data),3):
        price.append(data[i])
        foreigner.append(data[i+1])
        agency.append(data[i+2])

    df = pd.DataFrame({'Date':date,'Price':price,'Foreigner':foreigner,'Agency':agency})
    investor_df = pd.DataFrame(df,columns=['Date','Price','Foreigner','Agency'])
    return investor_df
   
   
  
def get_shortsell():
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    now = datetime.now()
    dif = now - timedelta(weeks=4)
    gen_otp_data = {
        'locale': 'ko_KR',
        'tboxisuCd_finder_srtisu0_0': '011200/HMM',
        'isuCd': 'KR7011200003', 
        'codeNmisuCd_finder_srtisu0_0': 'HMM', 
        'share': '1,',
        'money': '1',
        'strtDd': dif.strftime('%Y%m%d'),
        'endDd': now.strftime('%Y%m%d'),
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/srt/MDCSTAT30001'
    }

    headers = {'Referer':'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'}
    otp = requests.post(gen_otp_url,gen_otp_data, headers=headers).text

    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    down_short = requests.post(down_url, {'code':otp}, headers=headers)
    excelread_df = pd.read_csv(BytesIO(down_short.content), encoding='EUC-KR', thousands=',')
    excelread_df = excelread_df.rename(columns={'공매도 수량_거래량_전체':'거래량','공매도 수량_잔고수량':'잔고수량','공매도 금액_거래대금_전체':'거래대금','공매도 금액_잔고금액':'잔고금액'})
    date_df = excelread_df[['일자']]
    ex_df = excelread_df[['거래량','잔고수량','거래대금','잔고금액']]
    
    for v in ex_df:
       ex_df[v].loc[:] = ex_df[v].map('{:,d}'.format)
    
    shortsell_df = pd.concat([date_df,ex_df],axis=1)
    shortsell_df = shortsell_df.loc[0:10]
       
    return shortsell_df

  
