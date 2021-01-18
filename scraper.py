import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title" or @class="news V_Title_Img"]/text-fill/a/@href'
XPATH_TITTLE = '//text-fill[@style="font-size: 45px; line-height: 49px;" or @style="font-size: 44px; line-height: ' \
               '48px;"]/a/text() '
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                tittle = parsed.xpath(XPATH_TITTLE)[0]
                tittle = tittle.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                author = parsed.xpath(XPATH_AUTHOR)
            except IndexError:
                return print("Ta mal")

            with open(f'{today}/{tittle}.txt', 'w', 'utf-8') as f:
                f.write(tittle)
                f.write('\n\n')
                f.write(author)
                f.write('\n')
                f.write(summary)
                f.write('\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
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
                os.mkdir(today)

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
