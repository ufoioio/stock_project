
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep    
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
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

def parser():
    parser = argparse.ArgumentParser(description = 'text')
    parser.add_argument('--start_d', type=str, required=True)
    parser.add_argument('--end_d' ,type =str, required=True)
    parser.add_argument('--stock', type = str, required=True)

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


driver.get('https://finance.naver.com/news/news_search.nhn')
print(driver.current_url)
driver.implicitly_wait(3)
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



title_rep ={"“": '', "”": ''}
title_rep = dict((re.escape(k), v) for  k, v in title_rep.items())
title_pattern = re.compile('|'.join(title_rep.keys()))

time_rep = {'\t':'', '\n': ' '}
time_rep = dict((re.escape(k), v) for  k, v in time_rep.items())
time_pattern = re.compile('|'.join(time_rep.keys()))


cols = ['title', 'url', 'press', 'summary', 'date']



def append_csv(df, csv_path):
    if not os.path.isfile(csv_path):
        df.to_csv(csv_path, mode='a', index=False)
    else:
        df.to_csv(csv_path, mode='a', index=False, header=False)
        
        
def driver_page_craw(p_source, start_d, end_d, kind):
#     html = driver.page_source
    # soup에 넣어주기
#     print(p_source)
    soup = BeautifulSoup(p_source, 'html.parser')
#     print(soup)
    # print(soup.text)
    
#     news_subject = soup.select('div.newsSchResult > dl.newsList > dd.articleSubject')
#     news_summary = soup.select('div.newsSchResult > dl.newsList > dd.articleSummary' )
    news_subject = soup.find_all(['dd','dt'], attrs = {'class' :'articleSubject' })
    news_summary = soup.find_all(['dd','dt'], attrs = {'class' :'articleSummary' })
#     articleSummary
    
#     if len(new_subject
#     print(news_subject)
#     print(news_summary)
#     print(news_summary.text)
#     print(news_subject.text)
    
    res_li = [newsparser(sub, summary) for k,(sub,summary) in enumerate(zip(news_subject, news_summary))]
    df = pd.DataFrame(res_li, columns=cols)
    df = df.sort_values(by= ['date'], axis =0, ascending=True)

    if not os.path.exists('./stock/sam/seed'):
        os.makedirs('./stock/sam/seed')

    append_csv(df, './stock/sam/seed/{}-{}.csv'.format(start_d, end_d))
#     df.to_csv('./samsung-0602-0503.csv', mode='a', header=False)
    print("save -{}-{}-{}.csv".format(kind, start_d, end_d))
    
    
    
def newsparser(news_sub, news_summ):
    try:
        url_ = news_sub.select('a')[0]['href']
    except:
        url_=None
    try:
        title_ = news_sub.select('a')[0].text.strip()
        title_ = title_pattern.sub(lambda m : title_rep[re.escape(m.group(0))], title_)
    except:
        title_ = None
    try:
        press_ = news_summ.select('span.press')[0].text.strip()
    except:
        press_=None
    try:
        date_ = news_summ.select('span.wdate')[0].text.strip()
        date_ = time_pattern.sub(lambda m : time_rep[re.escape(m.group(0))], date_)
    except:
        date_ = None
    try:
        
        summary_ = news_summ.text.strip().split('\n')[0].strip()
    except:
        summary_ = None
    
    
    print(url_)
    print(title_)
#     print(press_)
#     print(date_)
#     print(summary_)
    
    data = [title_, url_, press_,summary_, date_]
    return data

def day_crawler(start_d, end_d, kind):
    while True:
        try:
            random_time = np.round(np.random.uniform(1,2),np.random.randint(1,5))
            time.sleep(random_time)
            elements_len = driver.find_elements_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td/a')
            current_pos = driver.find_element_by_css_selector('#contentarea_left > table > tbody > tr > td.on > a')
            current_idx = elements_len.index(current_pos)
            print(current_idx)
            last_large_page = True
            last_small_page = True
            try:
                driver.find_element_by_class_name('pgR')

                pass
            except NoSuchElementException as e:
                print('pgr indicator not in')
                pass

            try:
                driver.find_element_by_class_name('pgRR')
                print('PGRR indicator not in')
                pass
            except NoSuchElementException as e:
                pass

    #         if ((current_idx==len(elements_len)-1 )and ()) or (current_idx==len(elements_len)-2):

    #             print('pgr indicator')
    #             print('PPGR indicator')
    #             continue
            first_large_page = False
            first_small_page = False
            try:
                driver.find_element_by_class_name('pgL')

                pass
            except NoSuchElementException as e:
                first_large_page = True
                print('pgL indicator Not in')
                pass

            try:
                driver.find_element_by_class_name('pgLL')

                pass
            except NoSuchElementException as e:

                print('PPLL indicator Not in')
                pass

            html = driver.page_source
    #         print('HTML')
    #         print(html)
            driver_page_craw(html , start_d, end_d, kind)
    #         print('SSSS')
            if (current_idx==2) and (first_large_page ==False):
                elements_len[current_idx-1].click()
                pos_end = driver.find_elements_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td/a')[-3]
                pos_end.click()
                continue
            elif (first_large_page ==True) and (current_idx==0):
                print('Last page')
#                 driver.quit()
                break



            elements_len[current_idx-1].click()
        except (TimeoutException, WebDriverException) as e:
            print('Last page reached')
            driver.quit()
            break
        except (KeyboardInterrupt) as e:
            print('Interrupt')
            driver.quit()
            break
        except Exception as ex:
            print(ex)
            driver.quit()
            break



def main(kind, t_start, t_end):
#     delta = datetime.timedelta(days=1)
    mydates = pd.date_range(t_start, t_end).tolist()
    
    for ddate in mydates:
        
        
        craw_d = datetime.strftime(ddate ,'%Y-%m-%d')
        print(craw_d)
        page_setting(start_d =craw_d , end_d = craw_d, keyword = kind)
        day_crawler(start_d = craw_d, end_d =craw_d, kind = kind)
        print('END - {} - {} '.format(craw_d, kind))
        print('!'*100)
    print('End TOTAL')
    driver.quit()
if __name__ == '__main__':
    parse = parser()
    name =  stock_name[parse.stock]
    print(name)
    main(name, parse.start_d, parse.end_d)
    
# while True:
#     try:
#         random_time = np.round(np.random.uniform(2,6),np.random.randint(1,5))
#         time.sleep(random_time)
#         elements_len = driver.find_elements_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td/a')
#         current_pos = driver.find_element_by_css_selector('#contentarea_left > table > tbody > tr > td.on > a')
#         current_idx = elements_len.index(current_pos)
#         print(current_idx)
#         last_large_page = True
#         last_small_page = True
#         try:
#             driver.find_element_by_class_name('pgR')
            
#             pass
#         except NoSuchElementException as e:
#             print('pgr indicator not in')
#             pass
        
#         try:
#             driver.find_element_by_class_name('pgRR')
#             print('PGRR indicator not in')
#             pass
#         except NoSuchElementException as e:
#             pass
        
# #         if ((current_idx==len(elements_len)-1 )and ()) or (current_idx==len(elements_len)-2):
            
# #             print('pgr indicator')
# #             print('PPGR indicator')
# #             continue
#         first_large_page = False
#         first_small_page = False
#         try:
#             driver.find_element_by_class_name('pgL')
            
#             pass
#         except NoSuchElementException as e:
#             first_large_page = True
#             print('pgL indicator Not in')
#             pass
        
#         try:
#             driver.find_element_by_class_name('pgLL')
            
#             pass
#         except NoSuchElementException as e:
            
#             print('PPLL indicator Not in')
#             pass
        
#         html = driver.page_source
# #         print('HTML')
# #         print(html)
#         driver_page_craw(html)
# #         print('SSSS')
#         if (current_idx==2) and (first_large_page ==False):
#             elements_len[current_idx-1].click()
#             pos_end = driver.find_elements_by_xpath('//*[@id="contentarea_left"]/table/tbody/tr/td/a')[-3]
#             pos_end.click()
#             continue
#         elif (first_large_page ==True) and (current_idx==0):
#             print('Last page')
#             driver.quit()
#             break
            
            
            
#         elements_len[current_idx-1].click()
#     except (TimeoutException, WebDriverException) as e:
#         print('Last page reached')
#         driver.quit()
#         break
#     except (KeyboardInterrupt) as e:
#         print('Interrupt')
#         driver.quit()
#         break
#     except Exception as ex:
#         print(ex)
#         driver.quit()
#         break

