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
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
# 1. initial set
# This timeout value will be urllib.request.urlretrieve() timeout.
socket.setdefaulttimeout(30)  # 6 seconds


url = "https://www.nsmall.com"
# url = 'https://www.puregrips.com/'
driver = webdriver.Chrome("./chromedriver.exe")
action = ActionChains(driver)

driver.set_page_load_timeout(60)
driver.get(url)
time.sleep(3)
# driver.implicitly_wait()
# firstlevel_menu = driver.find_element_by_xpath(
#     '//*[@id="ns_header"]/div[2]/div/div[1]/button')


def GetImg():
    # global imgs
    global fileNum
    global srcURL
    # global number_pages
    fileNum = 0
    srcURL = []
    # we have globalized fileNum and srcURL because we want to stack imgs
    # and save them all together
    imgs = driver.find_elements_by_css_selector(
        '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')
    print(imgs)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir)):
            os.makedirs(os.path.join(saveDir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    # This will find the number of pages of images in the current window.
    pages_count = driver.find_elements_by_xpath(
        '//*[@id="subCatenentryList"]/div[4]')
    print(pages_count)
    time.sleep(10)
    # gather img for the first page
    for img in imgs:
        fileNum += 1
        print(img)
        print(fileNum)
        src = img.get_attribute('src')
        src = src.split('N')[0]+'U.jpg'
        srcURL.append(src)
        print(src)
    # this will find if the page has more than 8~ pages to be seen
    if driver.find_elements_by_css_selector('#subCatenentryList > div.lst_paging > span > a.last'):
        pages = driver.find_elements_by_css_selector(
            '#subCatenentryList > div.lst_paging > span > a.last')

        for page in pages:
            print(page)
            number_pages = page.get_attribute('href')
            print(number_pages)

        num_pages = ''.join([n for n in number_pages if n.isdigit()])
        print('---------------------------------------------------------')
        print(int(num_pages))
        print('---------------------------------------------------------')
        # set up page list to get different page_element
        page_list = []
        for a in range(11, 10000, 10):
            page_list.append(a)
        # page_list

        # for loop click to the next page
        for pg in range(2, int(num_pages)-1):
            # try:
            print(pg)
            # now if the number of the page exceeds clickable number
            # we will click the '>' button to move to next sets of page numbers
            # eg (11~18) (19~28) etc
            if pg in page_list:
                page_to_next = 'javascript:movePage('+str(pg)+');'
                # driver.find_element_by_xpath(
                #     '//a[@href="'+page_to_next+'"]').click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//a[@href="'+page_to_next+'"]'))).click()
                time.sleep(10)
                # for further noelement problem, we can try
                # WebDriverWait - EC.presence_of_all_elements_located()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')))
                imgs = driver.find_elements_by_css_selector(
                    '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')

                print(imgs)
                for img in imgs:
                    fileNum += 1
                    print(img)
                    print(fileNum)
                    src = img.get_attribute('src')
                    src = src.split('N')[0]+'U.jpg'
                    srcURL.append(src)
                    print(src)
            # click next page button and gather imgs
            else:
                page_to_next = 'javascript:movePage('+str(pg)+'); '
                # driver.find_element_by_xpath(
                #     '//a[@href="'+page_to_next+'"]').click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//a[@href="'+page_to_next+'"]'))).click()
                time.sleep(10)

                # load = WebDriverWait(driver, 10).until(
                #     EC.visibility_of_element_located((By.CSS_SELECTOR, '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')))
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')))
                imgs = driver.find_elements_by_css_selector(
                    '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')
                print(imgs)
                for img in imgs:
                    fileNum += 1
                    print(img)
                    print(fileNum)
                    src = img.get_attribute('src')
                    src = src.split('N')[0]+'U.jpg'
                    srcURL.append(src)
                    print(src)
            # except:
            #     continue
    # click the last page
        page_to_next = 'javascript:movePage('+str(num_pages)+');'
        print(num_pages)
        # driver.find_element_by_xpath(
        #     '//a[@href="'+page_to_next+'"]').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[@href="'+page_to_next+'"]'))).click()
        time.sleep(5)
        # load = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')))
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')))
        imgs = driver.find_elements_by_css_selector(
            '#subCatenentryList > div.cont1 > div > div > ul > li > div.pic > a.ptImg > img')
        print(imgs)
        for img in imgs:
            fileNum += 1
            print(img)
            print(fileNum)
            src = img.get_attribute('src')
            src = src.split('N')[0]+'U.jpg'
            srcURL.append(src)
            print(src)


"""
# First category crawl
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
print(element)
action.move_to_element(element).perform()

# time.sleep(2)
driver.find_elements_by_xpath(
    '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[1]/li[1]')[0].click()

print(driver)
GetImg()

ctg_name = 'TV쇼핑'
print(ctg_name)
saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
try:
    if not(os.path.isdir(saveDir+ctg_name)):
        os.makedirs(os.path.join(saveDir, ctg_name))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise
for i, src in zip(range(fileNum), srcURL):
    try:
        urllib.request.urlretrieve(
            src, saveDir+ctg_name+'/'+src.split('/')[-1])
        print(src.split('/')[-1], "saved")
        print(str(i)+'/'+str(fileNum))
    except:
        continue

# 카테고리 TV 쇼핑 이후 가공식품, 건강/다이어트식품, 농수축/신선식품

# second category crawl
id = 1583608
ids = range(1583608, 1583608+7)
for ctg in range(1583612, 1583615):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[1]/li[2]')
    action.move_to_element(element).perform()
    # driver.find_elements_by_xpath(
    #    '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[1]/li['+str(i)+']')[0].click()
    # action = ActionChains(driver)
    # element2 = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, '#ns_header > div.category_menu_wrap > div > div.category_wrap > div > div > ul.cate_list_wrap.food_health > li:nth-child(2) > a')))
    # action.move_to_element(element2).perform()
    driver.find_elements_by_xpath('//*[@id="'+str(ctg)+'"]/a')[0].click()
    id += 1
    GetImg()

    ctg_name = '가공식품'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ctg))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ctg)))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ctg)+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue
# category 3
id = 1583615
for ctg in range(1, 5):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[1]/li[3]')
    action.move_to_element(element).perform()
    driver.find_elements_by_xpath('//*[@id="'+str(id)+'"]/a')[0].click()
    id += 1
    GetImg()

    ctg_name = '다이어트식품'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ctg))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ctg)))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ctg)+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 4
id = 1583619
ids = range(1583619, 1583619+3)
for ctg in range(1583621, 1583622):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[1]/li[4]')
    action.move_to_element(element).perform()
    driver.find_elements_by_xpath('//*[@id="'+str(ctg)+'"]/a')[0].click()
    id += 1
    GetImg()

    ctg_name = '농수축'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ctg))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ctg)))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ctg)+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 5
bed_ids = [1583588, 1583591, 1583589, 1583590, 1583592,
           1583593, 1588746, 1588759, 1588764, 1588788]
for ctg in range(len(bed_ids)):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[1]')
    action.move_to_element(element).perform()
    driver.find_elements_by_xpath(
        '//*[@id="'+str(bed_ids[ctg])+'"]/a')[0].click()
    id += 1
    GetImg()

    ctg_name = '가구'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(bed_ids[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(bed_ids[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(bed_ids[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 6
# ids_6 = [1583579, 1583582, 1583583, 1583587, 1583581,
#          1583585, 1595054, 1583580, 1583586, 1583584]
ids_6 = [1583583, 1583587, 1583581,
         1583585, 1595054, 1583580, 1583586, 1583584]
for ctg in range(len(ids_6)):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[2]')
    action.move_to_element(element).perform()
    driver.find_elements_by_xpath(
        '//*[@id="'+str(ids_6[ctg])+'"]/a')[0].click()
    GetImg()

    ctg_name = '가전'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_6[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_6[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_6[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 7
ids_7 = [1583626, 1583627]
ids_7 = [1583627]
for ctg in range(len(ids_7)):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[3]')

    action.move_to_element(element).perform()
    driver.find_elements_by_xpath(
        '//*[@id="'+str(ids_7[ctg])+'"]/a')[0].click()
    GetImg()

    ctg_name = '반려동물'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name + str(ids_7[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_7[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_7[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue
"""

# category 8
"""
ids_8 = [1583628, 1583629, 1583630, 1583631, 1583632]
ids_8 = [1583632]
for ctg in range(len(ids_8)):
    action = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
    action.move_to_element(element).perform()
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(
        '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[4]')

    action.move_to_element(element).perform()
    driver.find_elements_by_xpath(
        '//*[@id="'+str(ids_8[ctg])+'"]/a')[0].click()
    GetImg()

    ctg_name = '스포츠'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_8[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_8[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_8[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue
"""

"""
# category 9
ids_9 = [1583633]
for ctg in range(len(ids_9)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[5]')

        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_9[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue
    ctg_name = '렌탈'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_9[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_9[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_9[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 10
ids_10 = [1583637, 1583636, 1583640, 1583638, 1583639]
for ctg in range(len(ids_10)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[6]')

        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_10[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue
    ctg_name = '유아동'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_10[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_10[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_10[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue

"""
# category 11
ids_11 = [1583641, 1583642, 1583643, 1583644, 1583645, 1583646, 1583647]
ids_11 = [1583646, 1583647]
for ctg in range(len(ids_11)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[2]/li[7]')

        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_11[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue

    ctg_name = '주방'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_11[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_11[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_11[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue

"""

# category 12
ids_12 = [1583597, 1583599, 1583598]
for ctg in range(len(ids_12)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[3]/li[1]')
        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_12[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue
    ctg_name = '뷰티'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_12[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_12[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_12[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue


# category 13
ids_13 = [1583603, 1583600, 1583601, 1583602]
for ctg in range(len(ids_13)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[3]/li[2]')
        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_13[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue
    ctg_name = '잡화'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_13[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_13[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_13[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue

# category 14
ids_14 = [1583605, 1583604, 1583607, 1583606]
for ctg in range(len(ids_14)):
    try:
        action = ActionChains(driver)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ns_header > div.category_menu_wrap > div > div.category_wrap > button")))
        action.move_to_element(element).perform()
        action = ActionChains(driver)
        element = driver.find_element_by_xpath(
            '//*[@id="ns_header"]/div[2]/div/div[1]/div/div/ul[3]/li[3]')
        action.move_to_element(element).perform()
        driver.find_elements_by_xpath(
            '//*[@id="'+str(ids_14[ctg])+'"]/a')[0].click()
        GetImg()
    except:
        continue
    ctg_name = '패션의류'
    print(ctg_name)
    saveDir = '/home/nick/Documents/Nick/crawling/02-19/nsmall/'
    try:
        if not(os.path.isdir(saveDir+ctg_name+str(ids_14[ctg]))):
            os.makedirs(os.path.join(saveDir, ctg_name, str(ids_14[ctg])))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    for i, src in zip(range(fileNum), srcURL):
        try:
            urllib.request.urlretrieve(
                src, saveDir+ctg_name+'/'+str(ids_14[ctg])+'/'+src.split('/')[-1])
            print(src.split('/')[-1], "saved")
            print(str(i)+'/'+str(fileNum))
        except:
            continue

"""
