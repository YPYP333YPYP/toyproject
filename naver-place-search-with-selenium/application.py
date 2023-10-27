import time
import selenium
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support import expected_conditions as EC 
import tkinter as tk
from tkinter import messagebox, filedialog
import threading



chrome_path = "./chrome-win64/chrome.exe"
chromedriver_path = "./chromedriver-win64/chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path


driver = None
value = None

def scraping(input, start, page_num, count):
    global driver
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get("https://map.naver.com/v5/")
    global is_scraping
    is_scraping = True

    run = start
    page = page_num
    search = f'{input}'
    
    

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
        ) 
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

    cnt = 0
    while run <= page:
        temp = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul')
        stores = temp.find_elements(By.TAG_NAME, 'li')
        
        
        for store in stores:
            if cnt == count:
                break
            button = store.find_element(By.CLASS_NAME,'tzwk0') #P7gyV    
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
            cnt+=1
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
    

    is_scraping = False
    return result


def start_scraping():
    global value
    global is_scraping
    if is_scraping:
        messagebox.showinfo("작업 중", "이미 스크래핑 작업이 실행 중입니다.")
        return
    input_num = num_entry.get()
    search_query = search_query_entry.get()
    
    if not input_num or not search_query:
        messagebox.showerror("입력 오류", "모든 칸을 입력하세요.")
        return
    
    scraping_button.config(state=tk.DISABLED)
    
    end_page = int(input_num) // 50
    is_scraping = True

    status_label.config(text="스크래핑 진행 중 (생성된 chrome 창을 닫지 말아주세요)")
    root.after(10, lambda: start_scraping_thread(search_query, 2, end_page+2, int(input_num)))

   

def start_scraping_thread(search_query, start, page_num, count):
    global value
    result = scraping(search_query, start, page_num, count)
    value = result
    update_gui_after_scraping()

def update_gui_after_scraping():
    global is_scraping
    is_scraping = False
    scraping_button.config(state=tk.NORMAL)
    
    status_label.config(text="스크래핑 완료")
    messagebox.showinfo("완료", "스크래핑이 완료되었습니다.")    
    

def save_to_excel():
    global value
    if value is None:
        messagebox.showinfo("스크래핑 결과 없음", "스크래핑 작업을 먼저 실행하세요.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel 파일", "*.xlsx")])
    if file_path:
        
        df = pd.DataFrame(value)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("완료", f"데이터가 {file_path}에 저장되었습니다.")
    else:
        messagebox.showinfo("취소", "파일 저장이 취소되었습니다.")   

def reset_chrome():
    global driver
    driver.quit()
    messagebox.showinfo("완료", "Chrome 초기화가 완료되었습니다.")

def exit_app():
    global is_scraping
    if is_scraping:
        messagebox.showinfo("작업 중", "스크래핑 작업이 진행 중입니다. 작업을 중지하고 종료하세요.")
    else:
        root.quit()

root = tk.Tk()
root.title("스크래핑 도구")
is_scraping = False

num_label = tk.Label(root, text="추출할 내용 개수:")
num_label.pack()
num_entry = tk.Entry(root)
num_entry.pack()


search_query_label = tk.Label(root, text="가게 이름:")
search_query_label.pack()
search_query_entry = tk.Entry(root)
search_query_entry.pack()

scraping_button = tk.Button(root, text="스크래핑 시작", command=start_scraping)
scraping_button.pack()

reset_button = tk.Button(root, text="Chrome 초기화", command=reset_chrome)
reset_button.pack()

save_button = tk.Button(root, text="엑셀로 저장", command=save_to_excel)
save_button.pack()

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

exit_button = tk.Button(root, text="종료", command=exit_app)
exit_button.pack()

root.mainloop()

