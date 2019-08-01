# colonial_stamps_com
import datetime
'''
import os
import sqlite3
from fake_useragent import UserAgent
import shutil
from stem import Signal
from stem.control import Controller
import socket
import socks
import requests
'''
from random import randint, shuffle
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
'''
controller = Controller.from_port(port=9051)
controller.authenticate()

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor():
    controller.signal(Signal.NEWNYM)

def showmyip():
    url = "http://www.showmyip.gr/"
    r = requests.Session()
    page = r.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    try:
    	ip_address = soup.find("span",{"class":"ip_address"}).text()
    	print(ip_address)
    except:
    	print('IP Issue')
    
UA = UserAgent(fallback='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
count = 0

hdr = {'User-Agent': "'"+UA.random+"'",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
'''

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #hdr)
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
        stamp['title'] = name.replace('"',"'")
    except:
        stamp['title'] = None

    try:
        category = html.find_all("a", {"class":"breadcrumb-label"})[1].get_text()
        stamp['category'] = category
    except:
        stamp['category'] = None

    try:
        sku = get_info_value(html, 'SKU:')
        stamp['sku'] = sku
    except:
        stamp['sku'] = None

    try:
        grade = get_info_value(html, 'Quality:')
        stamp['grade'] = grade
    except:
        stamp['grade'] = None

    try:
        gum = get_info_value(html,'Gum:')
        stamp['gum'] = gum
    except:
        stamp['gum'] = None
    
    try:
        cert = get_info_value(html,'Certificate:')
        stamp['certificate'] = cert
    except:
        stamp['certificate']=None
        
    try:
        raw_text = html.find_all("div", {"id":"tab-description"})[0].get_text()
        raw_text = raw_text.replace('¬†','.').strip()
        stamp['raw_text'] = raw_text.replace('"',"'")
    except:
        stamp['raw_text'] = None

    try:
        temp = stamp['raw_text'].split(' ')
        scott_num = temp[0]
        SG = temp[1]
        SG = SG.replace('(','').replace(')','')
        year = temp[2]
        face_value=temp[3]
    except:
        scott_num = None
        SG = None
        year = None
        face_value=None
    stamp['scott_num']=scott_num
    stamp['SG']=SG
    stamp['year']=year
    stamp['face_value']=face_value
        
    # This website is in pounds, i.e. GBP
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []
    try:
        image_items = html.find_all('figure', {'class': 'productView-image'})
        for image_item in image_items:
            img = image_item.find('a').get('href')
            img = img.replace('?c=2&imbypass=on','').strip()
            images.append(img)
    except:
        pass
    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25,65))
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
'''
def query_for_previous(stamp):
    # CHECKING IF Stamp IN DB
    os.chdir("/Volumes/Stamps/")
    conn1 = sqlite3.connect('Reference_data.db')
    c = conn1.cursor()
    col_nm = 'url'
    col_nm2 = 'raw_text'
    unique = stamp['url']
    print (unique)
    unique2 = stamp['raw_text']
    print(unique2)
    c.execute('SELECT * FROM colonial_stamps_com WHERE url LIKE "{un}%" AND raw_text LIKE "{un2}%"'.format(un=unique, un2=unique2))
    all_rows = c.fetchall()
    print(all_rows)
    conn1.close()
    price_update=[]
    price_update.append((stamp['url'],
    stamp['raw_text'],
    stamp['scrape_date'], 
    stamp['price'], 
    stamp['currency']))
    
    if len(all_rows) > 0:
        print ("This is in the database already")
        conn1 = sqlite3.connect('Reference_data.db')
        c = conn1.cursor()
        c.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn1.commit()
        conn1.close()
        print (" ")
        #url_count(count)
        sleep(randint(10,45))
        next_step = 'continue'
        pass
    else:
        os.chdir("/Volumes/Stamps/")
        conn2 = sqlite3.connect('Reference_data.db')
        c2 = conn2.cursor()
        c2.executemany("""INSERT INTO price_list (url, raw_text, scrape_date, price, currency) VALUES(?,?,?,?,?)""", price_update)
        conn2.commit()
        conn2.close()
        next_step = 'pass'
    print("Price Updated")
    return(next_step)

def file_names(stamp):
    file_name = []
    rand_string = "RAND_"+str(randint(0,100000))
    file_name = [rand_string+"-" + str(i) + ".png" for i in range(len(stamp['image_urls']))]
    return(file_name)
'''
def get_category_items(category_url):
    items = []
    next_url = ''

    try:
        category_html = get_html(category_url)
    except:
        return items, next_url

    try:
        for item in category_html.select('h4.card-title a'):
            item_link = item.get('href') + '?setCurrencyId=3'
            items.append(item_link)
    except: 
        pass

    try:
        next_url = category_html.select('link[rel=next]')[0].get('href')
    except:
        pass
    shuffle(items)
    return items, next_url 
'''
def db_update_image_download(stamp):  
    req = requests.Session()
    directory = "/Volumes/Stamps/stamps/colonial_stamps/" + str(datetime.datetime.today().strftime('%Y-%m-%d')) +"/"
    image_paths = []
    file_name = file_names(stamp)
    image_paths = [directory + '/' + file_name[i] for i in range(len(file_name))]
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    for item in range(0,len(file_name)):
        print (stamp['image_urls'][item])
        try:
            imgRequest1=req.get(stamp['image_urls'][item],headers=hdr, timeout=60, stream=True)
        except:
            print ("waiting...")
            sleep(randint(3000,6000))
            print ("...")
            imgRequest1=req.get(stamp['image_urls'][item], headers=hdr, timeout=60, stream=True)
        if imgRequest1.status_code==200:
            with open(file_name[item],'wb') as localFile:
                imgRequest1.raw.decode_content = True
                shutil.copyfileobj(imgRequest1.raw, localFile)
                sleep(randint(18,30))
    stamp['image_paths']=", ".join(image_paths)
    #url_count += len(image_paths)
    database_update =[]

    # PUTTING NEW STAMPS IN DB
    database_update.append((
        stamp['url'],
        stamp['raw_text'],
        stamp['title'],
        stamp['scott_num'],
        stamp['SG'],
        stamp['year'],
        stamp['category'],
        stamp['sku'],
        stamp['grade'],
        stamp['gum'],
        stamp['certificate'],
        stamp['scrape_date'],
        stamp['image_paths']))
    os.chdir("/Volumes/Stamps/")
    conn = sqlite3.connect('Reference_data.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("""INSERT INTO colonial_stamps_com ('url','raw_text', 'title', 
    'scott_num','SG','year','category','sku', 'grade','gum','certificate', 'scrape_date','image_paths') 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", database_update)
    conn.commit()
    conn.close()
    print ("all updated")
    print ("++++++++++++")
    sleep(randint(120,240)) 
'''
        
# start category url 
count = 0
#connectTor()
#showmyip()
selection = input('Mint_Used or Cover_Postal_History: ')
item_dict = {'Mint_Used':'https://colonialstamps.com/mint-and-used/',
            'Cover_Postal_History':'https://colonialstamps.com/covers-and-postal-history/'}
category_url = item_dict[selection]
while(category_url):
    category_items, category_url = get_category_items(category_url)
    count += 1
    # loop through all category items
    shuffle(list(set(category_items)))
    for category_item in category_items:
        if count > randint(75,156):
            sleep(randint(500,2000))
            #connectTor()
            #showmyip()
            count = 0
        else:
            pass
        stamp = get_details(category_item)
        '''
        next_step = query_for_previous(stamp)
        if next_step == 'continue':
            print('Only updating price')
            continue
        elif next_step == 'pass':
            print('Inserting the item')
            pass
        else:
            break
        db_update_image_download(stamp)
        count += 1
        '''