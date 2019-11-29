import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
path_cd = os.path.join(os.path.dirname(__file__),'chromedriver.exe')
nl='\n'

driver = webdriver.Chrome(path_cd)
driver.fullscreen_window()
driver.get("https://rostov.tele2.ru/")

assert "Tele2" in driver.title
elem = driver.find_element_by_class_name("ssc-tariff-box")

elem.click()
assert "Tele2" in driver.title

#1
if driver.find_elements_by_tag_name("b")!=0 or driver.find_elements_by_tag_name("strong")!=0:
    print("Есть жирненькое")
else: print("Жирного текста нет")

#2
driver.back()
assert "Tele2" in driver.title

for tariff in driver.find_elements_by_xpath("//div[@class='ssc-tariff-box']"):
    if len(tariff.find_elements_by_class_name("hit-image"))!=0:
        print(f'Хит продаж: {tariff.text.split(nl)[0]}')
    else: print(f'Этот не хит: {tariff.text.split(nl)[0]}')
#3
count = len(driver.find_elements_by_xpath("//div[@class='ssc-tariff-box']"))
for i in range(count):
    try:
        driver.implicitly_wait(50)
        tariff = driver.find_elements_by_class_name("ssc-tariff-box")[i]
        print(' '.join(tariff.text.split("\n")[0:4]) + ", Цена на странице тарифа: ", end='')
        tariff.click()
        time.sleep(5)
        price = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
        print(price.text)
    except: print("Не хочу работать")
    finally:
        driver.back()
        time.sleep(5) #грубо, но встроенные ожидания не работали и assert не помогали

#4 зачем мелочиться на двух?)
region = ["Москва", "Санкт-Петербург", "Екатеринбург"]
comp = []
for reg in region:
    driver.find_element_by_xpath("//a[@id='regionSearchOpener']").click()
    new_r = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск региона"]')))
    new_r.send_keys(reg)
    try:
        driver.find_element_by_class_name("region-results").find_element_by_partial_link_text("область").click()
    except NoSuchElementException:
        driver.find_element_by_class_name("region-results").find_element_by_partial_link_text("край").click()
    time.sleep(5)

    tariffs = {}
    for tariff in driver.find_elements_by_class_name("ssc-tariff-box"):
        tariffs[tariff.text.split('\n')[0]] = tariff.text.split('\n')[1:4]
    comp.append(tariffs)


for t in comp[0].items():
    res = f'В {region[0]} тариф {t[0]} стоит {"".join(t[1])}'
    count=1
    for other in comp[1:]:
        res += f'\nA в {region[count]} такой тариф стоит {"".join(other.get(t[0], "Нет такого тарифа"))}'
        count +=1
    print(res, end='\n-----------------------------------\n')

#5
driver.get("https://rostov.tele2.ru/")
assert "Tele2" in driver.title

for tariff in driver.find_elements_by_xpath("//div[@class='ssc-tariff-box']"):
    if len(tariff.find_elements_by_class_name("settings-link"))!=0:
        print(f"У тарифа: {tariff.text.split(nl)[0]} есть возможность настройки")


#6
driver.get("https://more.tele2.ru/")
assert "Tele2" in driver.title
print("Kартиночки с сайта:")
for pict in driver.find_elements_by_xpath("//picture//img"):
    print(pict.get_attribute("src"))

driver.quit()
