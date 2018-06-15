import logging
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import os
import requests
import csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_url = ' https://www.zomato.com/melbourne/dinner-in-ashburton'


headers = {
    'user-agent': (
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        'Gecko/20100101 Firefox/55.0'
    )
}

session = requests.session()
br = RoboBrowser(user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)', tries=2, parser='lxml',session = session)
# br.open(base_url)

if not os.path.exists('headerImg'):
    os.mkdir('headerImg')
if not os.path.exists('menuImg'):
    os.mkdir('menuImg')


def info_item(item_url):
    item_content = session.get(item_url)
    item_content.raise_for_status()
    local_soup = BeautifulSoup(item_content.content, 'lxml')

    header_img = local_soup.find('div', class_='mb0 ui segment wrapper progressive_img hero--restaurant')['data-url']
    if header_img:
        filename = header_img.split('/')[-1].split('?')[0]
    else:
        header_img = local_soup.find('div', class_='lazy-res-photo res-photo-thumbnail')
        header_img = header_img['data-original'] if header_img else ""
        filename = header_img.split('/')[-1].split('?')[0] if header_img else ""

    if filename:
        with open('headerImg/{}'.format(filename), 'wb') as f:
            content = session.get(header_img).content
            f.write(content)


    title = local_soup.select_one('a.ui.large.header.left').text.strip()
    rating = local_soup.select_one('div.res-rating.pos-relative.clearfix.mb5').text.strip()

    loc = local_soup.select_one('a.left.grey-text.fontsize3').text.strip()
    loc_type = local_soup.select_one('span.res-info-estabs.grey-text.fontsize3').text.strip()

    cuisine = local_soup.select_one('div.res-info-cuisines.clearfix').text.strip()

    votes, phone, avg_costs = local_soup.find_all('span',{'tabindex':0, 'aria-label':True})[:3]
    votes, phone, avg_costs = votes.text.strip(), phone.text.strip(), avg_costs.text.strip()

    open_hours = [' '.join(a.strings) for a in local_soup.select_one('#res-week-timetable').find_all('tr')]
    open_hours = ','.join(open_hours)
    address = local_soup.select_one('div.borderless.res-main-address div.resinfo-icon span').text.strip()


    with open('zomato-v5b-test.csv','a+') as myfile:
        wr = csv.writer(myfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        l = []
        for img in local_soup.find_all('img',{'class':'lazy-menu-load'}):
            image_url = img['data-original'].split('?')[0]
            filename = image_url.split('/')[-1]
            logging.info('saved with {}'.format(filename))
            # myfile.write(',{}'.format(filename))
            # wr.writerow([filename])
            l.append(filename)
            content = session.get(image_url).content
            with open('menuImg/{}'.format(filename),'wb') as f:
                f.write(content)

        wr.writerow([title, loc, loc_type, header_img, filename, rating, votes, phone, cuisine, avg_costs, open_hours, address,
             item_url, *l])


i = 1
while i < 9:
    br.open("https://www.zomato.com/melbourne/dinner-in-ashburton?page={}".format(i))
    page_content = br.parsed
    for item in page_content.select(' div.row div.col-s-12 a.result-title.hover_feedback.zred.bold.ln24.fontsize0'):
        item_url = item.get('href')
        logging.debug('Now processing {} '.format(item_url))
        info_item(item_url)
    i+=1






