import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

def chek_load(driver, title):
    try:
        assert title in driver.title
    except:
        driver.refresh()
        driver.implicitly_wait(5)
        assert title in driver.title


path_cd = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

driver = webdriver.Chrome(path_cd)
driver.get("https://rostov.tele2.ru/")

chek_load(driver,'Tele2')

#иконка входа
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/a/span[1]"))).click()
time.sleep(3)


#фрейм входа driver.find_element_by_partial_link_text('Неверный')
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="loginDialog"]/div/div[2]/iframe'))
#переключаемся на вход с паролем
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="card-auth"]/div/div/ul/li[2]/a/span[1]'))).click()
time.sleep(2)

#Вводим данные, в обработке могут быть косяки из-за черезмерной задержки, но вроде норм
flag = True
while flag:
    login = input('Введите свой номер без 7/+7/8: ')
    passw = input('Введите пароль: ')

    tel = driver.find_element_by_id('phone-password')
    tel.click()
    tel.clear()
    tel.send_keys(login)

    pas = driver.find_element_by_id('password-field')
    pas.send_keys(passw)
    pas.send_keys(Keys.RETURN)
    time.sleep(5)
    try:
        flag = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/section/div[1]'))).text
    except:
        flag = ''

driver.implicitly_wait(10)
#Если есть связные номера - выберем тот, с которого зашли
driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/a/span/span[1]').click()
try:
    driver.find_element_by_class_name("master-account-label").click()
except: pass

print('Остатки: ', end='')
time.sleep(4)
driver.implicitly_wait(10)#не всегда срабатывает
for i in range(3):
    print(driver.find_elements_by_class_name('rate-box-lk')[i].text, end='; ')

print(f"\nБаланс: {driver.find_element_by_class_name('number').text}")

driver.find_element_by_link_text('Расходы и пополнения').click()
nl = '\n'
m=0
while m < 12:
    driver.implicitly_wait(10)
    month = driver.find_element_by_class_name('period-slider')
    print(f"Расходы за {month.text}:")
    for i in range(len(driver.find_elements_by_class_name('text-box'))):
        #Над строкой можно еще поиздеваться и более детально выводить, но надо ли?
        print(f"    {' '.join(driver.find_elements_by_class_name('text-box')[i].text.split(nl)[:2])}")

    try:
        month.find_element_by_class_name('icon-left-arrow').click()
        m += 1
    except:
        print(f'В истории доступно всего {m+1} месяцев'); m = 12

driver.close()