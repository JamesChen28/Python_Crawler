# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 23:48:52 2021

@author: James
"""

# import packages
import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import json


# 非函數測試
'''
url = 'https://www.ptt.cc/bbs/Steam/index.html'
keyword = '心得'
previousPage = 5

# def 1

# 爬網頁
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# 美化網頁架構
print(soup.prettify())

# 找網址、標題、日期
cell = soup.select('div.r-ent')

hrefList = []
titleList = []
dateList = []

for item in cell:
    
    try:
        # href
        href = 'https://www.ptt.cc' + item.select_one('a').get('href')
        
        # title & date
        titletext = item.text
        title = re.split('\n', titletext)[3].strip()
        date = re.split('\n', titletext)[14].strip()
        
        # 找限免
        if keyword in title:
            
            hrefList.append(href)
            titleList.append(title)
            dateList.append(date)
            
            print(title, date)
    
    except AttributeError:
        # deleted article
        titletext = item.text
        deleteTitle = re.split('\n', titletext)
        
        deleted = [x.strip() for x in deleteTitle if '(本文已被刪除)' in x]
        deletedDate = deleteTitle[11]
        
        print(deleted, deletedDate)

if len(titleList) == 0:
    print('no article')
else:
    print("that's all")


# 往前一頁搜尋
btn = soup.select('div.btn-group > a')
prev_page_href = btn[3]['href']
prev_page_url = 'https://www.ptt.cc' + prev_page_href

'''



# load json config
with open('pttCrawler_config.json', encoding = 'utf-8') as jsonfile:
    config_data = json.load(jsonfile)

board = config_data['board']
keyword = config_data['keyword']
previousPage = int(config_data['previousPage'])

url = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)

# define config

# board = 'Steam'
# url = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)
# keyword = '限免'
# previousPage = 10


# def get_url 得到當前頁面的keyword網址
def get_url(url, keyword):
    
    print('\nthis page url is', url)

    # 爬網頁
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 美化網頁架構
    # print(soup.prettify())
    
    # 找網址、標題、日期
    cell = soup.select('div.r-ent')
    
    hrefList = []
    titleList = []
    dateList = []
    
    for item in cell:
        
        try:
            # href
            href = 'https://www.ptt.cc' + item.select_one('a').get('href')
            
            # title & date
            titletext = item.text
            title = re.split('\n', titletext)[3].strip()
            date = re.split('\n', titletext)[14].strip()
            
            # 找限免
            if keyword in title:
                
                hrefList.append(href)
                titleList.append(title)
                dateList.append(date)
                
                print(title, date)
        
        except AttributeError:
            # deleted article
            titletext = item.text
            deleteTitle = re.split('\n', titletext)
            
            deleted = [x.strip() for x in deleteTitle if '(本文已被刪除)' in x]
            deletedDate = deleteTitle[11]
            
            # print(deleted, deletedDate)
    
    if len(titleList) == 0:
        print('this page no "{}" article'.format(keyword))
    
    # 往前一頁搜尋
    btn = soup.select('div.btn-group > a')
    prev_page_href = btn[3]['href']
    prev_page_url = 'https://www.ptt.cc' + prev_page_href
    
    return hrefList, titleList, dateList, prev_page_url


# def prev_page_search 往前頁搜尋
def prev_page_search(url, keyword, previousPage):
    
    print('search start', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    
    hrefList = []
    titleList = []
    dateList = []
    for page in range(0, previousPage):
        href, title, date, prev_page_url = get_url(url, keyword)
        
        hrefList.append(href)
        titleList.append(title)
        dateList.append(date)
        
        url = prev_page_url
        
        time.sleep(5)
        
    print('\nsearch end', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        
    return hrefList, titleList, dateList


hrefList, titleList, dateList = prev_page_search(url, keyword, previousPage)


# 將結果list鋪平，轉成dataframe
flat_hrefList = [item for sublist in hrefList for item in sublist]
flat_titleList = [item for sublist in titleList for item in sublist]
flat_dateList = [item for sublist in dateList for item in sublist]

df_output = pd.DataFrame(list(zip(flat_hrefList, flat_titleList, flat_dateList)), columns = ['網址', '標題', '日期'])

df_output.to_csv('PTT_{}版_關鍵字_{}_網址搜尋_{}.csv'.format(board, keyword, time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())), index = False, encoding = 'big5')



