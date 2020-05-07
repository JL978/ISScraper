from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://app.instantscripts.com/login")

time.sleep(2)
ps = driver.page_source

user_re = re.compile(r'id="input-(\d)?(\d)?(\d)?" placeholder="Email"')
user_search = user_re.search(ps)
user_re = re.compile(r'input-(\d)?(\d)?(\d)?')
user_search = user_re.search(user_search.group())
user_id = user_search.group()

pass_re = re.compile(r'id="input-(\d)?(\d)?(\d)?" placeholder="Password"')
pass_search = pass_re.search(ps)
pass_re = re.compile(r'input-(\d)?(\d)?(\d)?')
pass_search = pass_re.search(pass_search.group())
pass_id = pass_search.group()

print(str(user_id))
print(str(pass_id))
driver.find_elements_by_id(str(user_id))[0].send_keys(***REMOVED***)
driver.find_elements_by_id(str(pass_id))[0].send_keys(***REMOVED***)
driver.find_elements_by_class_name("v-btn__content")[0].click()
