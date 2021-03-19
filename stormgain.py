from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
import json
from random import randint

PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=PATH)

options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

with open('settings.json') as config_file:
    config = json.load(config_file)
stormgainemail = config['stormgain2_email']
stormgainpw = config['stormgain2_pw']
fromA = config['stormgainsleepMIN']
toB = config['stormgainsleepMAX']
path = '/usr/local/bin/chromedriver'


class browserstarter:

    def start(self):
        self.driver = webdriver.Chrome(executable_path=path)
        print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), "- browser started!")
        start.stormgain()

    def startup(self):
        start.start()

    def stormgainsleeper(self):
        sleeptime = randint(fromA, toB)
        self.driver.close()
        print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), "- miner is active! next claim in",
              str(datetime.timedelta(seconds=sleeptime)), "hh:mm:ss")
        time.sleep(sleeptime)
        start.start()

    def shortsleep(self):
        eta = self.driver.find_element_by_xpath('//*[@id="region-main"]/div/div[2]/div/div[3]/div/div[1]/span[2]').get_attribute('innerHTML')
        print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- time left:', eta, 'hh:mm:ss')
        h, m, s = eta.split(':')
        seceta = (int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds()))
        print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- short sleep triggered! - closing browser!')
        self.driver.close()
        ran = randint(seceta+200, seceta+1000)
        print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- sleep:',
              str(datetime.timedelta(seconds=int(ran))), 'hh:mm:ss')
        time.sleep(ran)
        start.start()

    def claimusdt(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        except Exception as e:
            print(e)

    def checkusdt(self):
        try:
            html = self.driver.find_element_by_xpath(
                '//*[@id="region-main"]/div/div[2]/div/div[2]/div/div/div[1]/div[2]/span[1]').get_attribute('innerHTML')
            usdt = html.replace('≈', '')
            print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- you have mined ' + str(usdt) + ' $')
            if float(usdt) >= float(10):
                print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), "- more than 10 USDT, claim it now!")
                start.claimusdt()
        except Exception as e:
            print(e)

    def stormgain(self):
        try:
            self.driver.get("https://app.stormgain.com/#modal_login")
            time.sleep(randint(3, 6))
            self.driver.find_element(By.ID, "email").send_keys(stormgainemail)
            self.driver.find_element(By.ID, "password").send_keys(stormgainpw)
            time.sleep(randint(3, 6))
            self.driver.find_element(By.CSS_SELECTOR, ".btn-login").click()
            time.sleep(randint(3, 6))
            self.driver.get('https://app.stormgain.com/crypto-miner/')
            time.sleep(randint(3, 15))
            # self.driver.switch_to.frame(0)
            print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), "- checking for earnings")
            start.checkusdt()
            self.driver.refresh()
            time.sleep(randint(3, 10))
            # self.driver.switch_to.frame(0)
        except:
            start.shortsleep()

        try:
            self.driver.find_element(By.CSS_SELECTOR, ".font-medium > .text-17").click()
            time.sleep(randint(3, 6))
            print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- miner activated!')
            start.stormgainsleeper()
        except:
            print(time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()), '- something wrong, getting short sleep!')
            start.shortsleep()


start = browserstarter()
start.start()
