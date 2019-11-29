import time

from selenium import webdriver

import os
path_cd = os.path.join(os.path.dirname(__file__),'chromedriver.exe')

driver = webdriver.Chrome(path_cd)
driver.fullscreen_window()
driver.get("https://rostov.tele2.ru/")
assert "Tele2" in driver.title

driver.execute_script("window.scrollTo(0, 800);")
time.sleep(3)
driver.find_element_by_id('fl-171881').click()
assert "Tele2" in driver.title

driver.switch_to.frame('fl-171881')

#1
tel = driver.find_element_by_id('tel')
tel.send_keys('9001234567')
name = driver.find_element_by_id('name')
name.send_keys('Bla-Bla')
time.sleep(5) #время, чтобы проверить)

my_link = []
my_link.append(driver.find_element_by_link_text('правилами программы').get_attribute('href'))
my_link.append(driver.find_element_by_link_text('обработку моих персональных данных').get_attribute('href'))

driver.find_element_by_xpath('/html/body/section/section[1]/form/div[3]/button[2]').click()
driver.switch_to.default_content()

#
nd = webdriver.Chrome(path_cd)
nd.fullscreen_window()
count = 1
for link in my_link:
    nd.get(link)
    time.sleep(5)
    nd.save_screenshot(f'scr_{count}.png')
    count+=1

nd.close()
driver.close()
