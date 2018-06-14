import logging
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import os
import requests
import cssutils
import base64

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
br.open(base_url)

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
        header_img = local_soup.find('div', class_='lazy-res-photo res-photo-thumbnail')['data-original']
        filename = header_img.split('/')[-1].split('?')[0]

    with open('headerImg/{}'.format(filename), 'wb') as f:
        content = session.get(header_img).content
        f.write(content)


    title = local_soup.select_one('a.ui.large.header.left').text.strip()
    rating = local_soup.select_one('div.res-rating.pos-relative.clearfix.mb5').text.strip()

    loc = local_soup.select_one('a.left.grey-text.fontsize3').text.strip()
    loc_type = local_soup.select_one('span.res-info-estabs.grey-text.fontsize3').text.strip()

    cuisine = local_soup.select_one('div.res-info-cuisines.clearfix').text.strip()

    votes, phone, avg_costs = local_soup.find_all('span',{'tabindex':0, 'aria-label':True})[:3]
    open_hours = local_soup.select_one('div.res-info-detail div.res-info-timings div.clearfix div.medium').text.strip()
    address = local_soup.select_one('div.borderless.res-main-address div.resinfo-icon span').text.strip()

    return {
        "Name":title,
        "Location":loc,
        "Type":loc_type,
        "HeaderImg":filename if filename else "",
        "Rating":rating,
        "Reviews":votes,
        "Phone":phone,
        "Cuisine":cuisine,
        "AvgCost":avg_costs,
        "OpeningHours":open_hours,
        "Address":address,
        "MenuImgs":'1234'
    }






page_content = br.parsed


# for item in page_content.select(' div.row div.col-s-12 a.result-title.hover_feedback.zred.bold.ln24.fontsize0'):
#     item_url = item.get('href')
#     logging.debug('Now processing {} '.format(item_url))
#     info_item(item_url)
#
#     print(item)


info_item('https://www.zomato.com/melbourne/coriander-thai-kitchen-ashburton')
