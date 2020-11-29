#!/usr/bin/env python
# encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

import os
import sys
import json
import time
import re

INT_RE = "^[-+]?[0-9]+$"

# 讀取檔案裡的參數值
basis = ""
CONST_APP_VERSION = "1.0"
Root_Dir = ""
HomePage = "https://www.ruten.com.tw/"
LoginPage = "https://member.ruten.com.tw/user/login.htm"
CartPage = "https://mybid.ruten.com.tw/deliver/list_cart.php"


def clear_cart():
    driver.get(CartPage)
    time.sleep(1.0)
    while (check_exists_by_class("delete-button")) :
        try :
            driver.find_element_by_class_name("delete-button").click()
            driver.find_element_by_class_name("rt-button-important").click()
        except ElementClickInterceptedException:
            time.sleep(1.0)
            driver.find_element_by_class_name("rt-button-outline")[1].click()



def check_exists_by_class(className):
    time.sleep(1.0)
    try:
        driver.find_element_by_class_name(className)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_id(elementId):
    time.sleep(1.0)
    try:
        driver.find_element_by_id(elementId)
    except NoSuchElementException:
        return False
    return True



def get_original_price_from_str():
    str = driver.find_element_by_id("item_price").text
    str = str.replace('\n', '').replace('$', '').replace(',', '')
    str = re.findall(INT_RE, str)[0]
    price = int(str)
    return price

def get_price_from_str():
    str = driver.find_element_by_id("item_discounted_price").text
    str = str.replace('\n', '').replace('$', '').replace(',', '')
    str = re.findall(INT_RE, str)[0]
    price = int(str)
    return price


def check_price_and_input_Id():
    time.sleep(1)
    originalPrice = get_original_price_from_str()
    price = get_price_from_str()
    while (originalPrice == price):
        price = get_price_from_str()

    reload_conut = 0
    time.sleep(1)
    price = get_price_from_str()
    while (budget < price):
        print ('price too high, try reload page to get new price')
        print('budget', budget)
        print('price', price)
        reload_conut = reload_conut + 1
        driver.refresh()
        time.sleep(1.0)
        price = get_price_from_str()
        while (originalPrice == price):
            price = get_price_from_str()
        print('reload : ' + str(reload_conut) + ' times')
    driver.find_element_by_id('idno').send_keys(personID)

if hasattr(sys, 'frozen'):
    basis = sys.executable
else:
    basis = sys.argv[0]
app_root = os.path.dirname(basis)
config_filepath = os.path.join(app_root, 'settings.json')
config_dict = None

if os.path.isfile(config_filepath):
    with open(config_filepath) as json_data:
        config_dict = json.load(json_data)

if not config_dict is None:
    # read config.
    if 'productUrl' in config_dict:
        productUrl = config_dict["productUrl"]
    if 'personID' in config_dict:
        personID = config_dict["personID"]

        order_Count = ""
    if 'orderCount' in config_dict:
        orderCount = str(config_dict["orderCount"])

    if 'account' in config_dict:
        account = str(config_dict["account"])

    if 'password' in config_dict:
        password = str(config_dict["password"])

    if 'budget' in config_dict:
        budget = int(str(config_dict["budget"]))


    # output config:
    print("version", CONST_APP_VERSION)
    print("productUrl", productUrl)
    print("personID", personID)
    print("orderCount", orderCount)
    print("budget", budget)
    print("account", account)
    print("password loaded")


    chrome_options = webdriver.ChromeOptions()
    # for navigator.webdriver
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {"profile.password_manager_enabled": False,
                                                     "credentials_enable_service": False,
                                                     'profile.default_content_setting_values': {'notifications': 2}})
    chromedriver_path = Root_Dir + "webdriver/chromedriver"
    caps = chrome_options.to_capabilities()
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path=chromedriver_path)
else:
    print('Config Error')

driver.get(LoginPage)
driver.find_element_by_id('userid').send_keys(account)
driver.find_element_by_id('userpass').send_keys(password)
driver.find_element_by_id('btnLogin').send_keys(Keys.ENTER)
clear_cart()
driver.get(productUrl)
driver.find_element_by_id('buy_count').send_keys(Keys.BACKSPACE)
driver.find_element_by_id('buy_count').send_keys(orderCount)
driver.find_element_by_class_name('item-purchase-action').click()
time.sleep(1.0)
driver.find_element_by_class_name('rt-button-large').click()
while(not check_exists_by_id("item_discounted_price")):
    print ("loadding .......")

check_price_and_input_Id()

