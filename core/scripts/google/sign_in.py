import core
from selenium import webdriver
import time
import json
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import core.__main__ as core

from selenium import webdriver
import geckodriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def phantomjsworks():
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
    PHANTOMJS_ARG = {'phantomjs.page.settings.userAgent': UA}
    driver = webdriver.PhantomJS(desired_capabilities=PHANTOMJS_ARG)

    url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
    driver.get(url)

    driver.find_element_by_id("Email").send_keys(os.environ.get("GOOGLE_EMAIL"))
    driver.find_element_by_id("next").click()
    driver.find_element_by_id("Passwd").send_keys(os.environ.get("GOOGLE_PASSWORD"))
    driver.find_element_by_id("signIn").click()

def firefoxdoesnwork():
    geckodriver_autoinstaller.install()

    profile = webdriver.FirefoxProfile(r'C:\Users\aethe\AppData\Roaming\Mozilla\Firefox\Profiles\nd2o9e8h.default-release')

    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    driver = webdriver.Firefox(firefox_profile=profile,
                            desired_capabilities=desired)
    
    manual_claiming_url = "https://studio.youtube.com/owner/v44qCPasIFl9dXsTbbFiqg/claims/manual?o=v44qCPasIFl9dXsTbbFiqg&filter=%5B%5D&sort=%7B%22columnType%22%3A%22video%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"
    # google = "https://www.google.com"
    
    my_account = "https://myaccount.google.com/"
    url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
    driver.get(url)
    
    email = os.environ.get("GOOGLE_EMAIL")
    password = os.environ.get("GOOGLE_PASSWORD")

    
    # time.sleep(20)

    email_x = '//*[@id="identifierId"]'
    core.wait_and_send_keys(driver, email, email_x)
    time.sleep(3)

    next_x = '//*[@id="identifierNext"]/div/button'
    core.click(driver, next_x)

    time.sleep(20)

    password_x = ''
    pw = driver.find_element(by=By.XPATH, value=password_x)
    pw.send_keys(password)

    time.sleep(20)

    # login_button_xpath = r'//*[@id="login-button"]/div[1]'
    # lb_xpath = r'//*[@id="login-button"]/span[1]/span'
    driver.find_element(by=By.ID, value="login-button").click()

    time.sleep(20)

def googledoesntwork():
    # chrome_driver_path = "path/to/chromedriver"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chrome_driver_path = f"{dir_path}/chromedriver"

    # Replace this with the path to your exported cookies file
    cookies_file_path = 'cookies.json'

    with open(cookies_file_path, 'r') as file:
        cookies = json.load(file)

    driver = uc.Chrome()

    manual_claiming_url = "https://studio.youtube.com/owner/v44qCPasIFl9dXsTbbFiqg/claims/manual?o=v44qCPasIFl9dXsTbbFiqg&filter=%5B%5D&sort=%7B%22columnType%22%3A%22video%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"
    # google = "https://www.google.com"



    my_account = "https://myaccount.google.com/"
    driver.get(manual_claiming_url)
    # google_domain = ".google.com"
    print(driver.get_cookies())

    for cookie in cookies:
        print(cookie["id"])
        # Ensure the 'sameSite' attribute is set to a valid value
        if 'sameSite' in cookie:
            cookie['sameSite'] = cookie['sameSite'].capitalize()
            if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                cookie['sameSite'] = "None"

            # Add cookies with the appropriate domain
        if 'domain' in cookie and (".myaccount.google.com" in cookie['domain']):
            cookie["domain"] = ".google.com"
            # print(cookie)
            print(cookie)
            driver.add_cookie(cookie)

    email = os.environ.get("GOOGLE_EMAIL")
    password = os.environ.get("GOOGLE_PASSWORD")

    
    # time.sleep(20)

    email_x = '//*[@id="identifierId"]'
    core.wait_and_send_keys(driver, email, email_x)
    time.sleep(3)

    next_x = '//*[@id="identifierNext"]/div/button'
    core.click(driver, next_x)

    time.sleep(20)

    password_x = ''
    pw = driver.find_element(by=By.XPATH, value=password_x)
    pw.send_keys(password)

    time.sleep(20)

    # login_button_xpath = r'//*[@id="login-button"]/div[1]'
    # lb_xpath = r'//*[@id="login-button"]/span[1]/span'
    driver.find_element(by=By.ID, value="login-button").click()

    time.sleep(20)

    # sleep(1)  # rc

    # time.sleep(100)

# firefoxdoesnwork()

# # Refresh the page to load cookies
# driver.refresh()

# # Wait for a while to check
# time.sleep(10)

# driver.quit()