from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re

from bs4 import BeautifulSoup

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', False) #added so that TouchActions can be used to scroll, can be added to driver as an argument


def launch_login():
    global driver
    driver = webdriver.Chrome(PATH, options=options)
    driver.get("https://app.instantscripts.com/login")

    global timer
    timer = WebDriverWait(driver, 10) #Want to use this object to get elements in cases where the page could still be loading

    login = timer.until(EC.presence_of_element_located((By.CLASS_NAME, "v-btn__content")))

    ps = driver.page_source

    #the id for the login fields seems to not be constant, therefore a search of the entire hmtl for the id is required to obtain their id
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

    driver.find_element_by_id(str(user_id)).send_keys('JimmyLam978@gmail.com') #Hidden for confidentiality
    driver.find_element_by_id(str(pass_id)).send_keys('Pussy1234@') #Hidden for confidentiality
    login.click()

def get_topics():
    #get the element for the first subject also is a check to see if the main page after login has fully loaded
    global first_topic
    first_topic = timer.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/nav/div[1]/div[2]/div/div[2]/a[1]')))

    #getting a list of all the topic titles in the pop-out navigation bar
    source = driver.page_source
    main_soup = BeautifulSoup(source, 'lxml')
    table_links = main_soup.find_all('a', class_ = "category-list-item v-list-item v-list-item--link theme--dark")
    topic_list = []

    for link in table_links:
        link_soup = BeautifulSoup(str(link), 'lxml')
        link_titles = link_soup.find('div', class_ = "v-list-item__title").text
        topic_list.append(link_titles)
    return(topic_list)

launch_login()
topics = get_topics()

for x, topic in enumerate(topics):
    if topic == 'Headlines':
        driver.quit()
        continue
    #     first_topic.click()

    #     #just for headlines, there are multiple categories so we have to close all those tabs before going on
    #     for div_path in range(1,26):
    #         head_area = timer.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="app"]/div[1]/main/div/div/div/div[1]/div/div/div/div/div[{div_path}]')))

    #         actions = ActionChains(driver)
    #         actions.move_to_element(head_area)
    #         if div_path < 15:
    #             actions.click()
    #         actions.perform()

    # else: 
    #     launch_login()
    #     #print(source)
    #     print(x)
    #     print(topic)
    #     timer1 = WebDriverWait(driver, 20)
    #     time.sleep(8)
    #     print('clicknow')
    #     topic = timer1.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="app"]/div[2]/nav/div[1]/div[2]/div/div[2]/a[{x+1}]')))
    #     actions = ActionChains(driver)
    #     actions.move_to_element(topic)
    #     actions.click()
    #     actions.perform()
    #     time.sleep(3)
    launch_login()
    print('click')
    print(topic)
    time.sleep(10)

    i = 0 
    try: 
        fill_data = list()
        ex_data = list()
        old_number = str()
        while i<30:
            source = driver.page_source
            # print(source)
            main_soup = BeautifulSoup(source, 'lxml')
            scroll_table = main_soup.find('div', class_ = "match-height scrollable px-0 px-sm-6 pb-12")

            scroll_soup = BeautifulSoup(str(scroll_table), 'lxml')
            number_tag = scroll_soup.div.div
            #get the element that are changed whenever the targeted section is scrolled too far (an tag attribute of the div)
            current_number = number_tag['style'][-len(number_tag['style']):-9]

            #If the current number is not equal to the old number means that the number was just updated and therefore the list was also updated and so we want 
            #to add that data to our set
            if current_number != old_number:
                for element in scroll_table:
                    #locating the tag that contains the two divs with the item that we want, the fill_in copy and the example copy
                    scroll_soup = BeautifulSoup(str(element), 'lxml')
                    scroll = scroll_soup.find_all('div', class_ = "measure")
                    
                    for m in scroll:
                        measure_soup = BeautifulSoup(str(m), 'lxml')
                        #print(measure_soup.prettify())
                        fill_in_copy = measure_soup.find('div',"v-list-item__title").text
                        ex_copy = measure_soup.find('div',"v-list-item__subtitle").text
                        print(fill_in_copy)
                        print(ex_copy)
                        fill_data.append(fill_in_copy)
                        ex_data.append(ex_copy)
                old_number = number_tag['style'][-len(number_tag['style']):-9]
                i = 0

            taction = TouchActions(driver)
            taction.scroll(0, 200)
            taction.perform()
            print(i)
            i += 1
            # end_card = timer.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div[1]/header/div/button[1]')))
            # actions = ActionChains(driver)
            # actions.move_to_element(end_card)
            # actions.click()
            # actions.perform()
        data = list(zip(fill_data, ex_data))
        print(data)
        with open(f'{topic}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            print('hi')
            writer.writerow(['Fill_in Copy', 'Example Copy'])
            print('hello')
            writer.writerows(data)
            print('yes')
            
    except Exception as e:
        print(e)
        driver.quit()
    finally:
        driver.quit()

driver.quit()
