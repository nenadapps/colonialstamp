import datetime
from random import randint
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_details(url):
    
    stamp = {}

    try:
       html = get_html(url)
    except:
       return stamp

    try:
        price = html.find_all("span", {"class":"price--withoutTax"})[0].get_text()
        price = price.replace(",", "")
        stamp['price'] = price.replace('£','') # This website is in Pounds so need to use this symbol
    except:
        stamp['price'] = None

    try:
        name = html.find_all("h1", {"class":"productView-title"})[0].get_text()
        stamp['title'] = name
    except:
        stamp['title'] = None

    try:
        sku = get_info_value(html, 'SKU:')
        stamp['sku']=sku
    except:
        stamp['sku']=None

    try:
        grade = get_info_value(html, 'Quality:')
        stamp['grade']=grade
    except:
        stamp['grade']=None

    try:
        raw_text = html.find_all("div", {"id":"tab-description"})[0].get_text()
        stamp['raw_text'] = raw_text.replace('¬†','.').strip()
    except:
        stamp['raw_text'] = None

    # This website is in pounds, i.e. GBP
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []
    try:
        image_items = html.find_all('figure', {'class': 'productView-image'})
        for image_item in image_items:
            img = image_item.find('a').get('href')
            images.append(img)
    except:
        pass

    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    sleep(randint(25,65)) #Waiting 25-65s before next request
    return stamp

def get_info_value(html, info_name):
    info_value = ''
    items = html.find_all('dt', {'class': 'productView-info-name'})
    for item in items:
        item_heading = item.get_text().strip()
        item_next = item.find_next().get_text().strip()
        if(item_heading == info_name):
            info_value = item_next
            break
    
    return info_value
        

url = 'https://colonialstamps.com/Great-Britain-Scott-40-Gibbons-87-Used-Stamp-65248/'
stamp = get_details(url)
print(stamp)
         