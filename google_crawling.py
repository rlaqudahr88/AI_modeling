import sys
import os
import requests
import random
import time
import urllib
import urllib.request
import socket

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parallel_sync import wget
from selenium.webdriver.common.keys import Keys
from socket import timeout

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait

# 1. initial set
# This timeout value will be urllib.request.urlretrieve() timeout.
socket.setdefaulttimeout(6)  # 6 seconds

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# browser = webdriver.Chrome('./chromedriver.exe',
#                            options=chrome_options)
# folder = ".image/"

url = "https://www.google.com/search"

# searchItems = ['선글라스','선풍기','세제','세탁기 냉장고',\
#     '수납장','스탠드 조명','식탁','신발','안마의자','운동기구','주얼리',\
#     '청소기','클렌저','타올','화장품','후라이팬','휴지겹']
# '건강식품','냄비','마스크','면도기','믹서기',\ '밥솥','백','생고기','샴푸','생고기',
# searchItem = '백'
# searchItems = ['과자','과일']
# searchItems = ['양말','침대','식품','샤프란','치약','물병','슬리퍼','패션','쌀','의자','가습기','바지','화장품']
size = 300
searchItems = ['background']
params = {
    "&tbm": "isch", "tbs": "ic:trans", "sa": "X"
}

# 2. enable browser

# url = url+"?"+urllib.parse.urlencode(params)
# https://www.google.com/imghp?tbm=isch&tbs=ic:trans&hl=ko&sa=X&ved=
# if this is inside the for loop, new browser

browser = webdriver.Chrome("./chromedriver.exe")

# will repeatedly generated
for i in range(len(searchItems)):
    # requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
    # requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
    url = "https://www.google.com/search"
    url = url+"?q="+searchItems[i]+'&tbm=isch&tbs=ic:trans&hl=ko&sa=X'
    # url = url+"?"+"q="+searchItems[i]+urllib.parse.urlencode(params)
    time.sleep(1)
    browser.get(url)
    time.sleep(3)
    html = browser.page_source


# 3. get number of image for a page

    soup_temp = BeautifulSoup(html, 'html.parser')
    img4page = len(soup_temp.findAll("img"))

# page down

    elem = browser.find_element_by_tag_name("body")
    imgCnt = 0
    while imgCnt < size:
        elem.send_keys(Keys.PAGE_DOWN)
        rnd = random.random()
        print(imgCnt)
        time.sleep(rnd)
        imgCnt += img4page


# find click images to save and save them
    imgs = browser.find_elements_by_css_selector(
        '#islrg > div.islrc > div > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img')
    saveDir = '/home/nick/Documents/Nick/crawling/'+searchItems[i]

# islrg > div.islrc > div:nth-child(1) > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img

# islrg > div.islrc
# subCatenentryList > div.cont1 > div > div > ul > li:nth-child(1) > div.pic > a.ptImg > img
# islmp

# islrg > div.islrc > div:nth-child(1) > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img

    try:
        if not(os.path.isdir(saveDir)):
            os.makedirs(os.path.join(saveDir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    fileNum = 0
    srcURL = []
    print(f"fileNum: {fileNum}")
    print(f"length of: imgs {len(imgs)}")
    for img in imgs:
        # try:
        # print(img)
        img.click()
        time.sleep(2)
        #html = browser.page_source
        # WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div[1]/div/div[2]/a/img')[0]))
        # alpha_img = browser.find_elements_by_xpath(
        #    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')[0]
        alpha_img = browser.find_elements_by_css_selector(
            '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > div > div.v4dQwb > a > img')[0]
        print(alpha_img.get_attribute('src'))
        srcURL.append(alpha_img.get_attribute('src'))
        print(srcURL)
        print(fileNum, ":", alpha_img.get_attribute('src'))
        fileNum += 1
        print(fileNum)
        # except:
        #     continue

    print('fileNum', fileNum)

    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(src, saveDir+"/"+str(i)+".png")
            print(i, "saved")
        except:
            continue
