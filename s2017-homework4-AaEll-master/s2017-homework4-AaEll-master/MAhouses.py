#!/usr/bin/python

from selenium import webdriver
from pyvirtualdisplay import Display
import time
import random
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()
driver.implicitly_wait(10)

def scrape_RedfinZipCode(zip,driver):
    url = 'https://www.redfin.com/zipcode/'+zip
    
    
    wait = WebDriverWait(driver, 10)
    
    '''
    if (random.random()>.94):
        driver.get('https://www.redfin.com')
        time.sleep(random.random()+3)
    '''

    driver.get(url)
    #time.sleep(random.random()*2+3)

    
    # if they redirected me, then skip it
    if driver.current_url != url:
        driver.delete_all_cookies()
        return(None)
    
    # if the zip has 0 homes in it, then skip it
    if driver.find_element_by_class_name('searchAboveTheFold')\
        .find_element_by_xpath(".//div[@data-rf-test-id='homes-description']")\
        .text == '0 Homes':
        driver.delete_all_cookies()
        return(None)
    
    Table = driver.find_element_by_xpath("//span[@data-rf-test-name='tableOption']")
    Table.click()
    del(Table)
    
    # this adds the links of the houses in ZIP to Webpages
    Rows = driver.find_elements_by_class_name('tableRow')
    WebPages = [] 
    for Row in Rows:
        child = Row.find_element_by_class_name('col_address')\
                .find_element_by_xpath(".//a")
        WebPages.append(child.get_attribute('href'))
    del(Rows)

    HouseList = [] # this is our main data structure to append house dictionaries
    time.sleep(.5)
    # this looks at each house's link and gets the information on it
    for Page in WebPages:
        housedic = {}
        #if (random.random()>.97):
        #    driver.get('https://www.redfin.com')
        #    time.sleep(random.random()+11)
        driver.get(Page)
        #time.sleep(random.random()*3+1)
        MainStats = driver.find_element_by_class_name("main-stats")
        
        try:
            housedic['street_address'] = MainStats.find_element_by_class_name('street-address').get_attribute('title')
        except NoSuchElementException:
            pass
        
        try:
            housedic['price'] = MainStats.find_element_by_xpath(".//span[@itemprop='price']").get_attribute('content')
        except NoSuchElementException:
            pass
        
        try:
            housedic['beds'] = driver.find_element_by_xpath("//div[@data-rf-test-id='abp-beds']")\
                .find_element_by_class_name("statsValue").text
        except NoSuchElementException:
            pass
        
        try:
            housedic['baths'] = driver.find_element_by_xpath("//div[@data-rf-test-id='abp-baths']")\
            .find_element_by_class_name("statsValue").text
        except NoSuchElementException:
            pass
        
        try:
            SqFt = driver.find_element_by_xpath("//div[@data-rf-test-id='abp-sqFt']")
            housedic['sqft'] = SqFt.find_element_by_class_name("statsValue").text
            housedic['price/sqft'] = SqFt.find_element_by_class_name("statsLabel").text
        except NoSuchElementException:
            pass
        
        KeyDetails = driver.find_element_by_class_name("keyDetailsList")

        try:
            housedic['prop type'] = KeyDetails.find_element_by_xpath(".//*[contains(text(), 'Property Type')]/following-sibling::*").text
        except NoSuchElementException:
            pass
        try:
            housedic['county'] = KeyDetails.find_element_by_xpath(".//*[contains(text(), 'County')]/following-sibling::*").text
        except NoSuchElementException:
            pass
        try:
            housedic['built'] = KeyDetails.find_element_by_xpath(".//*[contains(text(), 'Built')]/following-sibling::*").text
        except NoSuchElementException:
            pass
        try:
            housedic['community'] = KeyDetails.find_element_by_xpath(".//*[contains(text(), 'Community')]/following-sibling::*").text
        except NoSuchElementException:
            pass
            
        try:
            details = driver.find_element_by_class_name("remarks").find_element_by_xpath(".//p").text
            details =  ''.join(filter(lambda l: l.isalpha() or l==' ', details.lower().replace('-',' ')))

            if ' parking' in details or ' spot to park' in details:
                housedic['parking']=True
            if ' air conditioning' in details or ' air conditioned' in details:
                housedic['air conditioning']=True    

            details = set(details.split(' '))
            if 'kitchen' in details:
                housedic['kitchen'] = True
            if 'dishwasher' in details or 'dishwashing' in details:
                housedic['dishwasher'] = True
            if 'laundry' in details:
                housedic['laundry'] = True
            if 'heating' in details or 'heated' in details:
                housedic['heating'] = True
            if 'elevator' in details:
                housedic['elevator'] = True
        except NoSuchElementException:
            pass
        
        HouseList.append(housedic)
    driver.delete_all_cookies()
    return (HouseList)

print("Starting")

keys = ['street_address','price','beds','baths','sqft','price/sqft',\
    'prop type','county','community','built','parking','air conditioning',\
    'kitchen','dishwasher','laundry','heating','elevator']


i=-1
count_found = 0
count_failed = 0

with open('MA_houses.csv', 'a') as output_file:
    MainCSV = csv.DictWriter(output_file, keys)
    for zipcode in open('zipcodes.txt','r'):
        i+=1
        if i>512:
            #if (i%98 == 0):
            #    time.sleep(60*3+3 +random.random())
            #    print("Coffee break!")
            print(i,zipcode.strip())
            DicList = scrape_RedfinZipCode(zipcode.strip(),driver)
            if DicList != None:
                count_found = count_found+1
                MainCSV.writerows(DicList)
            else:
                count_failed = count_failed+1
    
print("finished\n","count failed:",count_failed,"\ncount found:",count_found)