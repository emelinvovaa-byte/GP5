#! /usr/bin/env python

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.request import urlretrieve
import random
import json
import os
import sys

botinki_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/botinki"
valenki_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/valenki-i-galoshi"
domashn_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/domashnyaya-obuv"
kedy_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/kedy"
krossovki_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/krossovki"
lofery_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv?attributes[muzhskaya_odezhda_obuv_tip][0]=330651"
mokasiny_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/mokasiny"
sandalii_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/sandalii"
sapogi_url = "https://youla.ru/moskva/muzhskaya-odezhda/obuv/sapogi"

f_baletki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/baletki"
f_bosonozhki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/bosonozhki"
f_botilony_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/botilony"
f_botinki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/botinki-i-polubotinki"
f_valenki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/valenki-i-galoshi"
f_domashn_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/domashnyaya-obuv"
f_dutiki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/dutiki-i-lunohody"
f_kedy_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/kedy"
f_krossovki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/krossovki"
f_lofery_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv?attributes[zhenskaya_odezhda_obuv_tip][0]=330652"
f_mokasiny_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/mokasiny"
f_polusapozhki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/polusapozhki"
f_sandalii_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/sandalii"
f_sapogi_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/sapogi"
f_slipony_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/slipony"
f_tapochki_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/tapochki"
f_tufli_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/tufli"
f_uggi_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/uggi-i-unty"
f_shlepancy_url = "https://youla.ru/moskva/zhenskaya-odezhda/obuv/shlepancy"

base_urls = [
    botinki_url,
    valenki_url,
    domashn_url,
    kedy_url,
    krossovki_url,
    lofery_url,
    mokasiny_url,
    sandalii_url,
    sapogi_url,

    f_baletki_url,
    f_bosonozhki_url,
    f_botilony_url,
    f_botinki_url,
    f_valenki_url,
    f_domashn_url,
    f_dutiki_url,
    f_kedy_url,
    f_krossovki_url,
    f_lofery_url,
    f_mokasiny_url,
    f_polusapozhki_url,
    f_sandalii_url,
    f_sapogi_url,
    f_slipony_url,
    f_tapochki_url,
    f_tufli_url,
    f_uggi_url,
    f_shlepancy_url,
]

classes = [
    "botinki",      # python ./parser.py 0 3
    "valenki",
    "domashn",

    "kedy",         # python ./parser.py 3 3
    "krossovki",
    "lofery",

    "mokasiny",     # python ./parser.py 6 3
    "sandalii",
    "sapogi",

    "f_baletki",        # python ./parser.py 9 6
    "f_bosonozhki",
    "f_botilony",
    "f_botinki",
    "f_valenki",
    "f_domashn",

    "f_dutiki",         # python ./parser.py 15 6
    "f_kedy",
    "f_krossovki",
    "f_lofery",
    "f_mokasiny",
    "f_polusapozhki",

    "f_sandalii",       # python ./parser.py 21 7
    "f_sapogi",
    "f_slipony",
    "f_tapochki",
    "f_tufli",
    "f_uggi",
    "f_shlepancy",
]

price_selector = ".sc-cZYOMl"
img_div_selector = ".sc-bWJUgm.bezZwh"
descr_selector = ".sc-cmaqmh.jHRPkw"
params_table_selector = '[data-test-component="DescriptionList"].sc-fUuaMo.hRfNAy'
button_selector = "button.sc-bbSZdi.sc-bBALqG.iymqix.jsgekI"
url_selector = "a[href*='/moskva/muzhskaya-odezhda/obuv/'], a[href*='/moskva/zhenskaya-odezhda/obuv/']"

data_dir = "data"


def find_element_reliable(driver, by, selector, timeout=10, condition="presence"):
    wait = WebDriverWait(driver, timeout)
    try:
        if condition == "presence":
            return wait.until(EC.presence_of_element_located((by, selector)))
        elif condition == "visible":
            return wait.until(EC.visibility_of_element_located((by, selector)))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable((by, selector)))
        elif condition == "all_presence":
            return wait.until(EC.presence_of_all_elements_located((by, selector)))
    except TimeoutException:
        print(f"Элемент не найден: {selector} за {timeout} секунд")
        driver.save_screenshot(f"error_{selector.replace(' ', '_')[:50]}.png")
        raise


def retrieve_shoe_info(driver, url):
    obj = {}

    driver.get(url)
    price = find_element_reliable(driver, By.CSS_SELECTOR, price_selector).text
    obj['price'] = ''.join(price.split())

    img_div = find_element_reliable(driver, By.CSS_SELECTOR, img_div_selector)
    img = find_element_reliable(img_div, By.TAG_NAME, "img")
    obj['src'] = img.get_attribute("src")

    descr = find_element_reliable(driver, By.CSS_SELECTOR, descr_selector).text
    obj['descr'] = ' '.join(descr.split())

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
    )
    driver.execute_script("arguments[0].click();", button)

    params_table = driver.find_elements(By.CSS_SELECTOR,
                                       params_table_selector)

    if len(params_table) >= 2:
        keys = list(map(lambda x: x.text, params_table[1].find_elements(By.TAG_NAME, 'dt')))
        vals = list(map(lambda x: x.text, params_table[1].find_elements(By.TAG_NAME, 'dd')))
        vals[-1] = vals[-1].split()[0]
        for k, v in zip(keys, vals):
            obj[k] = v

    return obj


def set_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0;" +\
            " Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +\
            " Chrome/120.0.0.0 Safari/537.36")
    return options


def scroll(driver):
    current_position = int(driver.execute_script(
                        "return window.pageYOffset;"))
    target_position = current_position + random.randint(1000, 1400)
    step = 200
    for position in range(current_position, target_position, step):
        driver.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(0.05)
    driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(3.0, 4.5))


def scroll_and_parse_urls(driver, max_scrolls):
    all_hrefs = set()
    for scroll_num in range(max_scrolls):
        print(f"Итерация скроллинга и сбора:" 
              f" {scroll_num + 1}/{max_scrolls}")
        try:
            wait = WebDriverWait(driver, 2)
            urls = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, url_selector)))
            for url_element in urls:
                try:
                    href = url_element.get_attribute("href")
                    if href and "youla.ru" in href:
                        all_hrefs.add(href)
                except:
                    continue
        except TimeoutException:
            print("На этом экране карточки не найдены, листаем дальше...")
        scroll(driver)
    return list(all_hrefs)


def main():
    driver = webdriver.Chrome(options=set_options())
    max_scrolls = 20

    if len(sys.argv) >= 3:
        start_i = int(sys.argv[1])
        n_elem = int(sys.argv[2])
    else:
        start_i = 0
        n_elem = len(base_urls)

    end_i = start_i + n_elem
    if end_i > len(base_urls):
        end_i = len(base_urls)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
        print("Создана папка:", data_dir)

    for i in range(start_i, end_i):
        class_url = base_urls[i]
        class_dir = data_dir + '/' + classes[i]
        class_imgs_dir = class_dir + '/imgs'
        if not os.path.exists(class_dir):
            os.mkdir(class_dir)
            print("Создана папка:", class_dir)
        if not os.path.exists(class_imgs_dir):
            os.mkdir(class_imgs_dir)
            print("Создана папка:", class_imgs_dir)

        driver.get(class_url)
        print("Переходим по ссылке:", class_url)
        time.sleep(4)

        all_hrefs = scroll_and_parse_urls(driver, max_scrolls)
        objects = []
        for j, href in enumerate(all_hrefs):
            print("Парсим ссылку:", href)
            try:
                obj = retrieve_shoe_info(driver, href)
                img_name = class_imgs_dir + f"/{classes[i]}_{j}"
                urlretrieve(obj['src'], img_name)
                print("Скачано изображение:", img_name)
                obj['img_name'] = img_name
                objects.append(obj)
                print("Получен объект:", obj)
            except:
                print("Произошла ошибка")
                continue
        json_name = class_dir + f"/{classes[i]}.json"
        with open(json_name, "w") as f:
            json.dump(objects, f)
            print("Записан файл:", json_name)

    print("Парсинг завершен")
    driver.close()


if __name__ == '__main__':
    main()
