from requests_html import HTMLSession
import scraperwiki
base_url = ' https://www.zomato.com/melbourne/dinner-in-ashburton'

headers = {
    "Host": "www.zomato.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "en-GB,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1"
}

session = HTMLSession()
r = session.get(base_url, headers = headers)
r.html.render()
print(r.ok, r.status_code)
