import time
import selenium
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support import expected_conditions as EC 

chromedriver_path = "./chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver_path)
driver.get("https://map.naver.com/v5/")


### input 
run = 2
page = 6
excelFileName = '고양시_술집.xlsx'
search = "고양시 술집"


try:
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
   ) #입력창이 뜰 때까지 대기
finally:
   pass

search_box = driver.find_element(By.CLASS_NAME,"input_search")
search_box.send_keys(search)
search_box.send_keys(Keys.ENTER)

#search_button = driver.find_element(By.CLASS_NAME,"button_search")
#search_button.send_keys(Keys.ENTER)

time.sleep(2)

frame= driver.find_element(By.ID,"searchIframe")
driver.switch_to.frame(frame)


time.sleep(3)

scroll = driver.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]')
driver.execute_script("arguments[0].scrollBy(0,2000)", scroll)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll)
time.sleep(2)

### list

title_list = []
address_list = []
phone_list = []
imgURL_list = []
section_list = []


while run <= page:
   temp = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul')
   stores = temp.find_elements(By.TAG_NAME, 'li')

   for store in stores:
     
      button = store.find_element(By.CLASS_NAME,'P7gyV')    
      button.send_keys(Keys.ENTER)
      
   
      time.sleep(3)

      driver.switch_to.default_content()
      entryFrame = driver.find_element(By.ID,"entryIframe")
      driver.switch_to.frame(entryFrame)

      time.sleep(3)

      try: 
         title = driver.find_element(By.CLASS_NAME, "Fc1rA").text
      except:
         title = ''
      
      try: 
         section = driver.find_element(By.CLASS_NAME,"DJJvD").text
      except:
         section = ''

      try:
         address = driver.find_element(By.CLASS_NAME,"LDgIH").text
      except:
         address = ''

      try:   
         phone = driver.find_element(By.CLASS_NAME,"xlx7Q").text
      except:
         phone = ''

      try:
         imgURL = driver.find_element(By.CLASS_NAME,"place_thumb").get_attribute('href')
      except:
         imgURL = ''

      title_list.append(title)
      section_list.append(section)
      address_list.append(address)
      phone_list.append(phone)
      imgURL_list.append(imgURL)

      driver.switch_to.default_content()
      driver.switch_to.frame(frame)

   next_btn = driver.find_element(By.LINK_TEXT,(str(run)))
   next_btn.send_keys(Keys.ENTER)
   run += 1
   time.sleep(5)
   

result = pd.DataFrame()
result.insert(0,'회사 명',title_list)
result.insert(1,"업종",section_list)
result.insert(2,'주소',address_list)
result.insert(3,'휴대폰',phone_list)
result.insert(4,'이미지 URL',imgURL_list)
result.to_excel(excelFileName)



