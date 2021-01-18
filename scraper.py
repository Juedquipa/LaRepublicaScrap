import requests
import lxml.html as html

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="V_Title" or @class="news V_Title_Img"]/text-fill/a/@href'
XPATH_TITTLE = '//h2[@style="font-size: 45px; line-height: 49px;" or @style="font-size: 44px; line-height: ' \
               '48px;"]/a/text() '
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_news)
        else:
            raise ValueError(f'Error : {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
