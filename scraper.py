import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

# XPATH_TITLE = '//text-fill[@style="font-size: 45px; line-height: 49px;" or @style="font-size: 44px; line-height: ' \
#               '48px;"]/a/text()'

#               Por un error de la libreria se usará la URL para sacar el titulo en vez del código HTML
XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title" or @class="news V_Title_Img"]/text-fill/a/@href'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'


def get_title(link):
    url = link.split('/')[-1]
    title_list = url.split('-')[:-1]
    title = " ".join(title_list)  # Créditos a https://platzi.com/p/alonmar/

    return title


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = get_title(link)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                author = parsed.xpath(XPATH_AUTHOR)[0]
            except IndexError:
                return print("Error, no se puedo escribir el .txt")

            with open(f'Datos recogidos/{today}/{title}.txt', 'w') as f:
                f.write(title)
                f.write('\n\n')
                f.write(author)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n\n')
        else:
            raise ValueError(f'Error : {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%d-%m-%y')
            if not os.path.isdir(today):
                os.mkdir(f'Datos Recogidos/{today}')

            for link in links_to_news:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error : {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
