import time

from selenium import webdriver

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

driver.find_element_by_xpath(
    '//*[@id="root"]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[3]/a/span[1]').click()
time.sleep(2)
I = len(driver.find_element_by_class_name('main-mobile-menu').find_elements_by_tag_name('a'))

driver.find_element_by_xpath('//*[@id="modalMenu"]/div/div[1]/span').click()
time.sleep(2)
count=0
i, j, k = 0, 0, 0

while i < I: #вроде обошелся одним циклом. Если с сетью все нормально. алгоритм не крашится. Иногда бывают загоны, и приходится перезапускать
    driver.execute_script("window.scrollTo(0, 0);") # странича вниз, бывает, сползает
    try: #пытаемся нажать кнопку меню
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[3]/a/span[1]').click()
        time.sleep(2)
    except:
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div[2]/div[3]/a/span[1]').click()

    try: # ох уж это всплывающее окно
        pm = driver.find_element_by_class_name('main-mobile-menu').find_elements_by_tag_name('a')[i].text
        driver.find_element_by_class_name('main-mobile-menu').find_elements_by_tag_name('a')[i].click()
    except:
        try:
            driver.switch_to.frame('fl-241715')
            driver.find_element_by_class_name("PushTip-close").click()
            driver.switch_to.default_content()
        except:
            print("Не всплывающее окно")
        pm = driver.find_element_by_class_name('main-mobile-menu').find_elements_by_tag_name('a')[i].text
        driver.find_element_by_class_name('main-mobile-menu').find_elements_by_tag_name('a')[i].click()

    time.sleep(2) #Не красивая штука, конечно, но втроенные таймауты не срабатывают(
    if j < len(driver.find_elements_by_class_name('regular')):
        J = len(driver.find_elements_by_class_name('regular'))
        if k < len(driver.find_elements_by_class_name('regular')[j].find_elements_by_tag_name('a')):
            K = len(driver.find_elements_by_class_name('regular')[j].find_elements_by_tag_name('a'))

            pr = driver.find_elements_by_class_name('regular')[j].find_elements_by_tag_name('a')[0].text
            link = driver.find_elements_by_class_name('regular')[j].find_elements_by_tag_name('a')[k].text

            driver.find_elements_by_class_name('regular')[j].find_elements_by_tag_name('a')[k].click()
            time.sleep(4)
            try: # ох уж это всплывающее окно)
                driver.switch_to.frame('fl-241715')
                driver.find_element_by_class_name("PushTip-close").click()
                driver.switch_to.default_content()
            except: pass

            count += 1
            # Небольшой лог)
            print(f"Пункт меню: {pm} -> подраздел: {pr} -> ссылка: {link}; Cчетчик: {count}")
            k+=1


            if (i==0 and j==1): #в пункте "переход в теле2" меню не стандартное, приходится выходить
                driver.get("https://rostov.tele2.ru/")
                time.sleep(5)
                chek_load(driver,'Tele2')
            elif (i==2 and j==1 and 1<k<4): #ну а тут вообще ссылки на договоры, поэтому приходиться возвращаться.
                driver.get("https://rostov.tele2.ru/")
                time.sleep(5)
                chek_load(driver,'Tele2')


            if k == K: j += 1; k = 0
        if j == J: i += 1; j = 0

driver.quit()
