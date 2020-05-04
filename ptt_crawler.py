#從selenium引入webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#引入beautifulsoup & 時間套件
from bs4 import BeautifulSoup
import time

import os

import csv

from datetime import date
today = date.today()
search_date = today.strftime('%-m/%d')
file_date = today.strftime('%-m-%d')

#初始化選項
options = Options()
#背景執行chrome
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

driver = webdriver.Chrome(os.getcwd()+"/chromedriver", chrome_options=options)

try:
    # 存成csv檔
    with open(file_date+'data.csv','w',newline='',encoding='utf_8_sig') as csvfile:
        driver.get('https://www.ptt.cc/bbs/NBA/index.html')
        sourceCode = BeautifulSoup(driver.page_source)
        last_page = sourceCode.select('a.btn.wide')[1]
        start = last_page['href'].find('x')
        end = last_page['href'].find('.')
        index = last_page['href'][start+1:end]
        #print(index)
        
        for i in range(int(index),6495,-1):
            #取得整個網頁
            driver.get('https://www.ptt.cc/bbs/NBA/index'+ str(i) +'.html')

            #轉譯成python看得懂的
            sourceCode = BeautifulSoup(driver.page_source)
            metaSection = sourceCode.select('div.r-list-container')[0]
            sections = metaSection.select('div.r-ent')


            #print(sections)
            for section in sections:
                title = section.select('div.title')[0].text
                num = section.select('div.nrec')[0].text
                author = section.select('div.author')[0].text
                date = section.select('div.date')[0].text
                #字串處理
                title = title.strip()

                if(title.startswith('[公告]')):
                    continue

                if(num.find('爆') != -1):
                    num = '100'
                if(num.find('X') != -1 or num==''):
                    num = '0'    
                
                if(date.strip() == search_date):
                    print(title +'|'+ num + '|'+author +'|'+ date)
                    writer = csv.writer(csvfile)
                    writer.writerow([title,num,author,date])

    driver.close()
except Exception as e:
    print(e)
    driver.close()