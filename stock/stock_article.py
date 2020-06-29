
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep    
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
# import datetime
from datetime import datetime
import numpy as np
import time
from tqdm import tqdm
from stock_list import stock_name
# import sys
# # reload(sys)
# sys.setdefaultencoding('utf-8')
import re
import os
import argparse
import gc

def parser():
    parser = argparse.ArgumentParser(description = 'text')
    parser.add_argument('--start_d', type=str, required=True)
    parser.add_argument('--end_d' ,type =str, required=True)
    parser.add_argument('--stock', type = str, required=True)
    parser.add_argument('--batch', type = int, required=True)

    args = parser.parse_args()
    return args



chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')

chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-dev-shm-usage')



# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")
# UserAgent값을 바꿔줍시다!
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
chrome_options.add_argument("lang=ko_KR") # 한국어!
driver = webdriver.Chrome('C:/Users/ufoio/Documents/Kiwoom_project/chromedriver_win32/chromedriver.exe', chrome_options=chrome_options)


driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
# lanuages 속성을 업데이트해주기
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

url_head = 'https://finance.naver.com/'
driver.get('https://finance.naver.com/news/news_search.nhn')
print(driver.current_url)
#driver.implicitly_wait(3)
# driver.quit()









# keyword='삼성전자'

# keyword=args.stock
# import datetime
# # start_d = '2020-05-01'
# # end_d = '2020-06-04'

# start_d = args.start_d
# end_d = args.end_d
# # end_d = datetime.datetime.now().strftime('%Y-%m-%d')
# print(start_d,'\n',
#      end_d)



# html = driver.page_source
# # soup에 넣어주기
# soup = BeautifulSoup(html, 'html.parser')
# print(soup.text)


def page_setting(start_d, end_d, keyword):
    print(start_d)
    print(end_d)
    
    driver.find_element_by_name('q').send_keys(Keys.CONTROL, 'a')
    driver.find_element_by_name('q').send_keys(Keys.BACKSPACE)
    driver.find_element_by_name('q').send_keys(keyword)
    
    


    driver.find_element_by_name('stDateStart').send_keys(Keys.CONTROL, 'a')
    driver.find_element_by_name('stDateStart').send_keys(Keys.BACKSPACE)
    driver.find_element_by_name('stDateStart').send_keys(start_d)


    driver.find_element_by_name('stDateEnd').send_keys(Keys.CONTROL, 'a')
    driver.find_element_by_name('stDateEnd').send_keys(Keys.BACKSPACE)
    driver.find_element_by_name('stDateEnd').send_keys(end_d)


    ### 검색 클릭
    driver.find_element_by_xpath('//*[@id="contentarea_left"]/form/div/div/div/input[2]').click()
    ### 맨뒤로 이동
#     driver.find_element_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td[12]/a').click()
    driver.find_element_by_css_selector(' #contentarea_left > table > tbody > tr > td.pgRR > a').click()
    
    
    
#     //*[@id="contentarea_left"]/table/tbody/tr/td[7]/a
#     #contentarea_left > table > tbody > tr > td.pgRR > a
    


# driver.find_element_by_name('q').send_keys(keyword)


# driver.find_element_by_name('stDateStart').send_keys(Keys.CONTROL, 'a')
# driver.find_element_by_name('stDateStart').send_keys(Keys.BACKSPACE)
# driver.find_element_by_name('stDateStart').send_keys(start_d)


# driver.find_element_by_name('stDateEnd').send_keys(Keys.CONTROL, 'a')
# driver.find_element_by_name('stDateEnd').send_keys(Keys.BACKSPACE)
# driver.find_element_by_name('stDateEnd').send_keys(end_d)


# ### 검색 클릭
# driver.find_element_by_xpath('//*[@id="contentarea_left"]/form/div/div/div/input[2]').click()
# ### 맨뒤로 이동
# driver.find_element_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td[12]/a').click()



head_rep ={"“": '', "”": ''}
head_rep = dict((re.escape(k), v) for  k, v in head_rep.items())
head_pattern = re.compile('|'.join(head_rep.keys()))

text_rep ={"  ": '\n'}
text_rep = dict((re.escape(k), v) for  k, v in text_rep.items())
text_pattern = re.compile('|'.join(text_rep.keys()))


# cols = ['title', 'url', 'press', 'summary', 'date']
cols = ['head','text']



def append_csv(df, csv_path):
    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, mode='a', index=False)
    else:
        df.to_csv(csv_path, mode='a', index=False, header=False)
        
        
def driver_news_craw(p_source):
    head_soup = BeautifulSoup(p_source, 'html.parser')
    text_soup = BeautifulSoup(p_source, 'html.parser')

    head_line = head_soup.select('div.articleCont > strong')
#     print('!'*50)
#     print(head_line)
#     print('#'*50)
    text_line = text_soup.find('div' ,class_ = 'articleCont')
#     print(text_line)
    for child in text_line.find_all('a'):
        child.decompose()
    for child in text_line.find_all('div'):
        child.decompose()
    for child in text_line.find_all('strong'):
        child.decompose()
    for child in text_line.find_all('b'):
        child.decompose()
    for child in text_line.find_all('span'):
        child.decompose()
#     print(text_line)
    
    text_line = [text_line]
    print("raw value")
    print(head_line)
    print(text_line)
    print((len(head_line)))
    print((len(text_line)))
    
    res_li  = [newsparser(head_line, text_line)]
    
    
#     res_li = [newsparser(head, text) for k,(head,text) in enumerate(zip(head_line, text_line))]
    print(res_li)
    df = pd.DataFrame(res_li, columns=cols)
    return df
    
    
    
def newsparser(head_line=None, text_line=None):
#     print(head_line[0])

    print("value In")
    print(head_line)
    print(text_line)
    try:
        head_  = head_line[0].text.strip()
        head_ = head_pattern.sub(lambda m : head_rep[re.escape(m.group(0))], head_)
    except:
        head_ = None
        
    try:
#     print(text_line)
        text_ = text_line[0].text.strip()
        print(text_)
        text_ = text_pattern.sub(lambda m : text_rep[re.escape(m.group(0))], text_)
        print(text_)
    except:
        text_ = None
        

#     head_  = head_line.text.strip()
#     head_ = head_pattern.sub(lambda m : head_rep[re.escape(m.group(0))], head_)

    print(head_)
    print(text_)
    print('!!!!!!!!')

#     text_ = text_line.text.strip()
#     text_ = text_pattern.sub(lambda m : text_rep[re.escape(m.group(0))], text_)

    
    data = [head_, text_]
    return data



def day_crawler(df):
    res_df= None
    for r_idx in range(df.shape[0]):
        random_time = np.round(np.random.uniform(1,2),np.random.randint(1,5))
        time.sleep(random_time)
        seed_df = df.iloc[r_idx]
#         print(seed_df['url'])
        print('START')
        print(url_head + seed_df['url'])
        driver.get(url_head + seed_df['url'])
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "spiLayer")))
        
        
        #driver.implicitly_wait(10)
        html = driver.page_source
        print(driver.current_url)
#         try:
        df_text = driver_news_craw(html)
#         except Exception as ex:
#             print(html)
#             print(ex)
#             driver.quit()
#             break
            
        df_text['url'] = seed_df['url']
    #     df_

        res_df = pd.concat([res_df,df_text ], axis =0, ignore_index=True)
    return res_df



def main(kind, t_start, t_end,batch_size):
#     delta = datetime.timedelta(days=1)
    mydates = pd.date_range(t_start, t_end).tolist()
    
    for ddate in mydates:
        
        try:
            craw_d = datetime.strftime(ddate ,'%Y-%m-%d')
            print(craw_d)

            if not os.path.exists('./stock/sam/seed'):
                os.makedirs('./stock/sam/seed')

            file_name = './stock/sam/seed/{}-{}.csv'.format(craw_d, craw_d)
            print(file_name)
            df = pd.read_csv(file_name)
            
            n = batch_size  #chunk row size
            df = [df[i:i+n] for i in range(0,df.shape[0],n)]
            try:
                for chunk_idx,chunk in enumerate(df):
                    res_df = day_crawler(chunk)
                    append_csv(res_df, '/notebook/stock/sam/article/{}-{}.csv'.format(craw_d, craw_d))
                    print("Day - {} Chunk - {}".format(craw_d, chunk_idx))
                    gc.collect()
            except Exception as ex:
                print('CHunk Error')
                print(ex)
                print("Error - {} - {}".format(craw_d, chunk_idx))
                break
            
            
            gc.collect()
            
            print('END - {} - {} '.format(craw_d, kind))
            print('!'*100)
        except (KeyboardInterrupt) as e:
                print('Interrupt')
                driver.quit()
                break
        
    print('End TOTAL')
    driver.quit()
if __name__ == '__main__':
    parse = parser()
    name =  stock_name[parse.stock]
    print(name)
    main(name, parse.start_d, parse.end_d, parse.batch)

