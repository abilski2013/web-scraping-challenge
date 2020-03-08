
from bs4 import BeautifulSoup
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov'
    original = '/spaceimages/?search=&category=Mars'
    browser.visit(url + original)
    browser.click_link_by_partial_text('FULL')
    browser.click_link_by_partial_text("more info")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('img', class_="main_image")
    link = content['src']
    featured_image_url = f'{url}{link}'

    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(mars_twitter_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text

    url_2 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_2)

    df = tables[0]
    df = df.rename(columns={0:"Category", 1:"Attribute"})

    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_3 = 'https://astrogeology.usgs.gov'
    original = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_3 + original)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', class_="collapsible results")

    images = content.find_all(class_="item")

    click_links = []
    for item in images:
        html = item
        content = html.find('a', class_="itemLink product-item")
        link = content['href']
        click_links.append(url_3 + link)

    titles = []
    full_image_links = []
    for item in click_links:
        browser.visit(item)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_="title").text
        full_image_link = soup.find('div', class_="downloads")
        image_links = full_image_link.find('li')
        image_links1 = image_links.find('a')["href"]
        full_image_links.append(image_links1)
        titles.append(title)
        browser.visit(url_3)


    df2 = pd.DataFrame(full_image_links, titles).reset_index()
    df2 = df2.rename(columns={"index":"title",0:"img_url"})

    dict1 = df2.to_dict('records')
    hemisphere_image_urls = dict1

    final_dictionary = {"latest_article_title": news_title,
                        "latest_article_text": news_p,
                        "featured_img_url": featured_image_url,
                        "mars_weather": mars_weather,
                        "html_data_frame": html_table,
                       "hemisphere_image_dict": hemisphere_image_urls }

    return final_dictionary

