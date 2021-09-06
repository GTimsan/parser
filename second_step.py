import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from html_telegraph_poster import TelegraphPoster
import psycopg2

from googletrans import Translator

translator = Translator()


def get_full_description():
    dir_path = "./testdir"
    dir = os.listdir(dir_path)

    for page in dir:

        with open("./testdir/" + page, "r", encoding="utf-8") as file:
            html = file.read()
        soup = BeautifulSoup(html, 'lxml')
        full = soup.find('div', class_='DrugPage__main-content___MrJho')
        # Название --------------------------------------------------------------------------------
        title_desc = full.find('div', class_='DrugHeader__wrapper___ZqUzE')
        name = title_desc.find('h1', class_='DrugHeader__title-content___2ZaPo').text

        # IMAGES --------------------------------------------------------------------------------------------------------
        image_list = full.find('div', class_='slick-list').find_all('img')
        images = []
        try:
            for i in image_list:
                url_original = i.get('src')
                a = url_original.split('watermark_')
                b = url_original.split('watermark_')[1].split('.')
                image_url = '<img src=' + a[0] + b[0] + '.png' + '>'
                images.append(image_url)
        except:
            images = []
        try:
            manufacturer = title_desc.find('div', class_='DrugHeader__meta-title___22zXC',
                                           text='Manufacturer').parent.find(
                'a').text
            manufacturer_tel = '<b>Manufacturer: </b>' + manufacturer
        except:
            manufacturer = ''
            manufacturer_tel = ''

        try:
            salt_composition = title_desc.find('div', class_='DrugHeader__meta-title___22zXC', text='SALT COMPOSITION') \
                .parent.find('a').text
            salt_composition_tel = '<b>Salt composition: </b>' + salt_composition
        except:
            salt_composition = ''
            salt_composition_tel = ''

        try:
            salt_synonyms = title_desc.find('div', class_='DrugHeader__meta-title___22zXC', text='Salt Synonyms') \
                .parent.find('a').text
            salt_synonyms_tel = '<b>Salt synonyms: </b>' + salt_synonyms
        except:
            salt_synonyms = ''
            salt_synonyms_tel = ''

        try:
            storage = title_desc.find('div', class_='DrugHeader__meta-title___22zXC', text='Storage').parent. \
                find('div', class_='saltInfo DrugHeader__meta-value___vqYM0').text
            storage_tel = '<b>Storage: </b>' + storage
            storage_tel_ru = translator.translate(storage_tel, src='en', dest='ru').text

        except:
            storage = ''
            storage_tel = ''
            storage_tel_ru = ''

        #     Вступление\INTRODUCTION ----------------------------------------------------------------------------------------------
        intro = full.find('div', class_='DrugOverview__content___22ZBX').text

        intro_ru = translator.translate(intro, src='en', dest='ru').text

        # Использование\USES OF и Преимущества\BENEFITS ----------------------------------------------------------------------------
        uses_of = []
        try:
            uses_of_list = full.find('div', id='uses_and_benefits').find('ul').find_all('li')
            for i in uses_of_list:
                uses_of.append(i.find('a').text)
            # uses_of_ru = translator.translate(uses_of, src='en', dest='ru').text
        except:
            uses_of = []

        benefits_dict = {}
        benefits_list_tel = []
        benefits_list_tel_ru = []
        try:
            benefits_list = full.find('div', id='uses_and_benefits').find_all('h3')
            for i in benefits_list:
                benefits_title = i.text
                benefits = i.parent.find('div').text
                benefits_dict[benefits_title] = benefits
                benefits_list_tel.append('<b>' + benefits_title + ': </b>' + benefits)
                benefits_list_tel_ru.append(
                    '<b>' + benefits_title + ': </b>' + translator.translate(benefits, src='en', dest='ru').text)

        except:
            benefits_dict = {}
            benefits_list_tel_ru = []
        print('Использовать')

        # # Побочные эффекты\SIDE EFFECTS OF ---------------------------------------------------------------------------------------
        side_effects_list = []
        side_effects_list_ru = []
        try:
            side_effects = full.find('div', id='side_effects').find_all('li')

            for li in side_effects:
                side_effects_list.append(li.text)
                side_effects_list_ru.append(translator.translate(li.text, src='en', dest='ru').text)
        except:
            side_effects_list = []
            side_effects_list_ru = []

        #     # Как использовать\HOW TO USE
        try:
            how_to_use = full.find('div', id='how_to_use').find('div', class_='DrugOverview__content___22ZBX').text
            how_to_use_ru = translator.translate(how_to_use, src='en', dest='ru').text
        except:
            how_to_use = ''
            how_to_use_ru = ''

        # # Как работает\HOW ----------------------------------------------------------------------------------------------------------
        try:
            how = full.find('div', id='how_drug_works').find('div', class_='DrugOverview__content___22ZBX').text
            how_ru = translator.translate(how, src='en', dest='ru').text
        except:
            how = ''
            how_ru = ''

        # # Советы по безопасности\SAFETY ADVICE ----------------------------------------------------------------------------------
        safety_advice_dict = {}
        list1 = []
        list2 = []
        list3 = []
        # list4 = ['https://onemg.gumlet.io/image/upload/w_50h_50/alcohol.png', 'https://b.radikal.ru/b30/2107/03/2b51855c76d3.png', 'https://onemg.gumlet.io/image/upload/w_50,h_50/lactation.jpg', 'https://onemg.gumlet.io/image/upload/w_50,h_50/driving.jpg', 'https://onemg.gumlet.io/image/upload/w_50,h_50/kidney.jpg', 'https://onemg.gumlet.io/image/upload/w_50,h_50/liver.jpg']
        safety_advice_list_tel = []
        safety_advice_list_tel_ru = []
        try:
            safety_advice_text = full.find('div', id='safety_advice').find_all('div',
                                                                               class_='DrugOverview__content___22ZBX')
            safety_advice_title = full.find('div', id='safety_advice').find_all('div',
                                                                                class_='DrugOverview__warning-top___UD3xX')
            for i in safety_advice_title:
                list1.append(i.find('span').text)
                list2.append(i.find('div', class_='DrugOverview__warning-tag___aHZlc').text)
            for i in safety_advice_text[1:]:
                list3.append(i.text)
            for num in range(0, len(safety_advice_title)):
                safety_advice_dict[list1[num]] = [list2[num], list3[num]]
                safety_advice_list_tel.append(
                    '<br>' + '<u><b>' + list1[num] + '</b></u>' + ': ' + list2[num] + '<br>' + list3[num])
                safety_advice_list_tel_ru.append('<br>' + '<u><b>' + translator.translate(list1[num], src='en',
                                                                                          dest='ru').text + '</b></u>' + ': ' + translator.translate(
                    list2[num], src='en', dest='ru').text + '<br>' + translator.translate(list3[num], src='en',
                                                                                          dest='ru').text)
        except:
            safety_advice_dict = {}
            safety_advice_list_tel = []
            safety_advice_list_tel_ru = []

        # WHAT IF YOU FORGET TO TAKE ---------------------------------------------------------------------------------------------
        try:
            what_if_you = full.find('div', id='missed_dose').find('div', class_='DrugOverview__content___22ZBX').text
            what_if_you_ru = translator.translate(what_if_you, src='en', dest='ru').text
        except:
            what_if_you = ''
            what_if_you_ru = ''

        # #     Быстрые советы\Quick Tips -----------------------------------------------------------------------------------------
        quick_tips_list = []
        quick_tips_list_ru = []
        try:
            quick_tips = full.find('div', id="expert_advice").find('ul').find_all('li')
            for li in quick_tips:
                quick_tips_list.append(li.text)
                quick_tips_list_ru.append(translator.translate(li.text, src='en', dest='ru').text)
        except:
            quick_tips = ''

        # #     Fact Box  -------------------------------------------------------------------------------------------------------
        fact_box_list = []
        fact_box_list_tel = []
        fact_box_list_tel_ru = []
        try:
            fact_box = full.find('div', id='fact_box').find('div', class_='DrugFactBox__content___1417O')
            for i in fact_box:
                key = i.find('div', class_='DrugFactBox__col-left___znwNB DrugFactBox__black___5cVbb').text
                value = i.find('div',
                               class_='DrugFactBox__col-right___36e1P DrugFactBox__black___5cVbb DrugFactBox__bold___1fqoO').text
                fact_box_list.append({key: value})
                fact_box_list_tel.append('<b>' + key + '</b>' + ': ' + value)
        except:
            fact_box_list = []

        #       User Feedback ---------------------------------------------------------------------------------------------------
        user_feedback_dict = {}
        user_feedback_list_tel = []
        try:
            user_feedback = full.find('div', id='user_feedback').find_all('div', class_='style__container___1nARz')
            for i in user_feedback:
                title = i.find('span').text
                string_title_list = i.find_all('div', class_='style__details-text___3mMMv')
                list1 = []
                list2 = []
                for i in string_title_list:
                    string_title = i.text
                    list1.append(string_title)
                    percent = i.parent.find('div', class_='style__percentage___1FkC_').text
                    list2.append(percent)
                user_feedback_dict[title] = {list1[num]: list2[num] for num in range(0, len(string_title_list))}
        except:
            user_feedback_dict = {}
        user_feedback_dict_tel = {}
        text_tel = ''
        text_tel_ru = ''
        for key1, values in user_feedback_dict.items():
            ls_list = []
            text_tel = text_tel + '<b>' + key1 + '</b>' + '<br>'
            for key, value in values.items():
                num = int(value.strip('%'))
                a = "".join(['▮' if i < num else '▯' for i in range(1, 101, 10)])
                ls1 = [key, a, value]
                text_tel = text_tel + key + ': ' + a + ' ' + value + '<br>'
                text_tel_ru = translator.translate(text_tel, src='en', dest='ru').text + translator.translate(key,
                                                                                                              src='en',
                                                                                                              dest='ru').text + ': ' + translator.translate(
                    a, src='en', dest='ru').text + ' ' + translator.translate(value, src='en', dest='ru').text + '<br>'

                ls_list.append(ls1)

            user_feedback_dict_tel[key1] = ls_list

        # #       FAQs -----------------------------------------------------------------------------------------------------
        faq_dict = {}
        faq_list_tel = []
        faq_list_tel_ru = []
        try:
            faqs = full.find('div', id='faq').find_all('h3')
            for i in faqs:
                faq_title = i.text
                faq_disc = i.parent.find('div', class_='Faqs__ans___1uuIW').text
                faq_dict[faq_title] = faq_disc
                faq_list_tel.append('<b>' + faq_title + '</b> ' + '<br>' + faq_disc)
                faq_list_tel_ru.append('<b>' + translator.translate(faq_title, src='en',
                                                                    dest='ru').text + '</b> ' + '<br>' + translator.translate(
                    faq_disc, src='en', dest='ru').text)
        except:
            faq_list_tel = []
            faq_list_tel_ru = []
        print('Фак')

        print("Парсинг закончился, начинается создание страниц")
        #  -------------------------------------------------------------------------------------------------------

        t = TelegraphPoster(access_token="5204b97b100bdcf170a68e1fbafa384ff370d89f7c53826ca8551689e441")
        #     f'▮ ▮ ▮ ▮ ▮ ▮ ▮ ▮ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯' + '<br>' + \
        #     f'▮▮▮▮▮▮▮█░░░░░░░░░░░░░░' + '<br>' + \
        #     f'<b>███████████░░░░░░░░░░░░░░</b>' + '<br>' + \
        #     f'█ █ █ █ █ █ █ █ █  ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░' + '<br>' + \
        #     f'<b>▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯</b>' + '<br>' + \
        #     f'▮▮▮▮▮▮▮░░░░░░░░░░░░░░' + '<br>' +\
        #     f'⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀' + '<br>' +\
        #     f'⣿ ⣿ ⣿ ⣿ ⣿ ⣿ ⣿ ⣿ ⣿ ⣿ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀ ⠀' + '<br>' + \
        #     f'▮▮▮▮▮▮▮░░░░░░░░░░░░░░' + '<br>' \

        text = ''.join(images) + \
               "<br>".join(i for i in [manufacturer_tel,
                                       salt_composition_tel,
                                       salt_synonyms_tel,
                                       storage_tel]) + \
               '<br><h5>INTRODUCTION: </h5> ' + intro + \
               '<h5>Uses of: </h5>' + ", ".join(i for i in uses_of) + '<br>' + \
               '<br>'.join(i for i in benefits_list_tel) + '<br>' + \
               '<h5>Side effects of: </h5>' + ", ".join(i for i in side_effects_list) + '<br>' + \
               '<h5>How to use: </h5>' + how_to_use + '<br>' + \
               '<h5>How it works: </h5>' + how + '<br>' + \
               '<h2>Safety advice: </h2>' + ''.join(i for i in safety_advice_list_tel) + '<br>' + \
               '<h5>What if you forget to take: </h5>' + what_if_you + '<br>' + \
               '<h5>Quick Tips: </h5>' + '<br> - '.join(i for i in quick_tips_list) + '<br>' + \
               '<h5>Fact box: </h5><br>' + '<br>'.join(i for i in fact_box_list_tel) + '<br>' + \
               '<h2>User Feedback:</h2>' + '<br>' + text_tel + '<br>' + \
               '<h5>FAQ: </h5>' + '<br>'.join(i for i in faq_list_tel)

        text_ru = ''.join(images) + \
                  "<br>".join(i for i in [manufacturer_tel,
                                          salt_composition_tel,
                                          salt_synonyms_tel,
                                          storage_tel_ru]) + \
                  '<br><h5>Описание: </h5> ' + intro_ru + \
                  '<h5>Использовать при: </h5>' + ", ".join(i for i in uses_of) + '<br>' + \
                  '<br>'.join(i for i in benefits_list_tel_ru) + '<br>' + \
                  '<h5>Побочные эффекты: </h5>' + ", ".join(i for i in side_effects_list_ru) + '<br>' + \
                  '<h5>Как использовать: </h5>' + how_to_use_ru + '<br>' + \
                  '<h5>Как работает: </h5>' + how_ru + '<br>' + \
                  '<h2>Советы по безопасности: </h2>' + ''.join(i for i in safety_advice_list_tel_ru) + '<br>' + \
                  '<h5>Если пропустили прием: </h5>' + what_if_you_ru + '<br>' + \
                  '<h5>Быстрые советы>: </h5>' + '<br> - '.join(i for i in quick_tips_list_ru) + '<br>' + \
                  '<h5>Факты: </h5><br>' + '<br>'.join(i for i in fact_box_list_tel_ru) + '<br>' + \
                  '<h2>Отзывы:</h2>' + '<br>' + text_tel_ru + '<br>' + \
                  '<h5>FAQ: </h5>' + '<br>'.join(i for i in faq_list_tel_ru)

        t.post(title=name, author='pharma', text=text)
        t.post(title=name + 'ru', author='pharma', text=text_ru)

        print(t.get_page_list())
        url_telegraph = t.get_page_list()['pages'][0]['url']
        url_telegraph_ru = t.get_page_list()['pages'][0]['url'] + '_ru'
        conn = psycopg2.connect(dbname='postgres', user='postgres',
                                password='*****', host='localhost', port=5432)
        cursor = conn.cursor()

        def add_row(*args):
            sql_query = """
            INSERT INTO full_desc(name, images, manufacturer_tel, salt_composition_tel, salt_synonyms_tel,
            storage_tel, intro, uses_of, benefits_list_tel, side_effects_list, how_to_use, how,
            safety_advice_list_tel, what_if_you, quick_tips_list, fact_box_list_tel, text_tel,
            faq_list_tel, url_telegraph)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """
            values = (args)
            cursor.execute(sql_query, values)
            conn.commit()

        add_row(name, images, manufacturer_tel, salt_composition_tel, salt_synonyms_tel,
                storage_tel, intro, uses_of, benefits_list_tel, side_effects_list, how_to_use, how,
                safety_advice_list_tel, what_if_you, quick_tips_list, fact_box_list_tel, text_tel,
                faq_list_tel, url_telegraph)

        def add_row_ru(*args):
            sql_query = """
            INSERT INTO full_desc_ru(name, images, manufacturer_tel, salt_composition_tel, salt_synonyms_tel,
            storage_tel, intro, uses_of, benefits_list_tel, side_effects_list, how_to_use, how,
            safety_advice_list_tel, what_if_you, quick_tips_list, fact_box_list_tel, text_tel,
            faq_list_tel, url_telegraph)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """
            values = (args)
            cursor.execute(sql_query, values)
            conn.commit()

        add_row_ru(name, images, manufacturer_tel, salt_composition_tel, salt_synonyms_tel,
                   storage_tel_ru, intro_ru, uses_of, benefits_list_tel_ru, side_effects_list_ru, how_to_use_ru, how_ru,
                   safety_advice_list_tel_ru, what_if_you_ru, quick_tips_list_ru, fact_box_list_tel, text_tel_ru,
                   faq_list_tel_ru, url_telegraph_ru)

        sleep(1)

        cursor.close()
        conn.close()


def main():
    # url ="https://www.1mg.com/drugs/133981"
    get_full_description()


if __name__ == '__main__':
    main()
