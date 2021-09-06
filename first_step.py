from multiprocessing import Pool
from random import choice
from time import sleep

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from content import list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_9, \
    list_10, list_11, list_12, list_13, list_14, list_15, list_16


def get_proxy():
    html = requests.get("https://free-proxy-list.net/").text
    soup = BeautifulSoup(html, 'lxml')
    proxies = []
    trs = soup.find('table', id="proxylisttable").find_all('tr')[1:50]
    for tr in trs:
        tds = tr.find_all('td')
        if tds[6].text.strip() == "yes":
            schema = "https://"
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies.append(proxy)

    return choice(proxies)


def get_html(url):
    p = get_proxy()
    proxies = {
        "http": "http://" + p['address'],
        "https": "https://" + p['address'],
    }
    r = requests.get(url, proxies=proxies, timeout=3)
    if r.ok:
        return r.text
    else:
        print(r.status_code)


# если будет ругаться - https://sites.google.com/a/chromium.org/chromedriver/downloads
def get_page_with_selenium(url, name):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    p = get_proxy()
    proxy = p['address']
    chrome_options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url=url)

        with open("pages/{name}.html".format(name=name), "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    grid = soup.find('body') \
        .find('div', style='transition:all 0.2s ease') \
        .find_all('div',
                  class_='Card__container__2Kvce Card__productCard__2MScM Card__direction__1UZ-g container-fluid-padded-xl')

    for card in grid:
        try:
            url_full = 'https://www.1mg.com' + str(card.find('a').get('href'))
            url_name = str(card.find('a').get('href')).split('/')[
                           2] + '_version-1'
            get_page_with_selenium(url=url_full, name=url_name)

        except:
            print('Неведомый косяк')


def make_all(url):
    while True:
        get_page_data(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            url = 'https://www.1mg.com' + str(soup.find('div', style='transition:all 0.2s ease')
                                              .find('div', class_='TherapeuticClass__buttonContainer__39WXC')
                                              .find('span', text='Next')
                                              .parent
                                              .parent
                                              .get('href'))
        except:
            print('Переход на следующую категорию')
            break


def main():
    with Pool(5) as p:
        p.map(make_all,
              list_2)


if __name__ == '__main__':
    main()
