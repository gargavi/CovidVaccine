from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import datetime
from twilio.rest import Client 
import multiprocessing
import time
import argparse
import smtplib
from multiprocessing import Pool, cpu_count


chromeOptions = webdriver.ChromeOptions()
chromedriver = "./chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)


client = Client("AC63e2bb6218122994deedf573efbd6e6d", "fa754cd367fb787f1e78342f9916cf92" )



def check_status(cvs = True, myturn = True): 
    if cvs:
        driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")
        driver.find_element_by_link_text('California').click()
        print("clicked on california")
        status = driver.find_element_by_xpath("/html/body/div[2]/div/div[13]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr[3]/td[2]/span").text
        now = datetime.datetime.now()
        print(now.strftime('%H:%M:%S on %A, %B the %dth, %Y'), status)

        if (status != "Fully Booked" and status != "" and status != " "):
            client.messages.create( to = "+19256998052", from_ = "+15706309420", body = f"CVS {now.strftime('%H:%M:%S on %A, %B the %dth, %Y')}, {status}" )
    if myturn:
        driver.get("https://myturn.ca.gov/")
        time.sleep(2)
        driver.find_element_by_tag_name("button").click()
        allchecks = driver.find_elements_by_tag_name("input")
        for a in allchecks[:4]:
            a.click()

        driver.find_element_by_id("q-screening-eligibility-age-range-16 - 49").click()
        driver.find_element_by_id("q-screening-underlying-health-condition-No").click()
        driver.find_element_by_id("q-screening-disability-No").click()
        sel = Select(driver.find_element_by_id("q-screening-eligibility-industry"))
        #select by select_by_visible_text() method
        sel.select_by_visible_text("Education and childcare")
        sel2 = Select(driver.find_element_by_id("q-screening-eligibility-county"))
        #select by select_by_visible_text() method
        sel2.select_by_visible_text("Alameda")
        driver.find_element_by_xpath('//*[@id="root"]/div/main/div/form/div/button[1]').click()
        time.sleep(2)
        driver.find_element_by_id("location-search-input").send_keys("94704")
        driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[5]/button[1]').click()
        time.sleep(10)
        try:
            info = driver.find_element_by_tag_name('h2').text
            if info != "No appointments are available, we can’t schedule your COVID-19 vaccination yet.":
                client.messages.create( to = "+19256998052", from_ = "+15706309420", body = f"My Turn: {now.strftime('%H:%M:%S on %A, %B the %dth, %Y')}, {status}" )
        except Exception as e:
            print(e)


while True: 
    try:
        check_status(cvs = False)
    except Exception as e:
        print(e)
    time.sleep(300)
    