from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import requests

import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape ():
    browser = init_browser()
    Mars_dict = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
  
    info_soup = BeautifulSoup(html, 'html.parser')

    news_title = info_soup.find_all('div', class_='content_title')[1].text
    news_p = info_soup.find_all('div', class_='article_teaser_body')[0].text

    # print(news_title)
    # print("--------------------------------------------------------------------")
    # print(news_p)


    jet_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jet_gov = "https://www.jpl.nasa.gov/"

    browser.visit(jet_url)

    html = browser.html

    img_soup = BeautifulSoup(html, 'html.parser')


    img_url = img_soup.find('li', class_='slide').a['data-fancybox-href']
    featured_image_url = jet_gov + img_url
    # print(featured_image_url)

    
    url_facts = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_facts)

    # print(type(tables))
    # print(type(tables[0]))

    df = tables[0]
    
    df.columns =['Description', 'Mars'] 
    df.set_index('Description', inplace=True)

    mars_facts = df.to_html('Mars_facts.html')


    USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_url)
    Hem_html = browser.html
    hemispheres_soup = BeautifulSoup(Hem_html, 'html.parser')


    hemisphere_image_urls = []

    products = hemispheres_soup.find("div", class_ = "collapsible results" )
    hemisphere = products.find_all("div", class_="item")


    for img in hemisphere:
        title = img.find("h3").text
    #     title = title.replace("Enhanced", "")
        large_link = img.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + large_link    
        
        browser.visit(img_link)
    
        HM_html = browser.html
        HM_soup = BeautifulSoup(HM_html, 'html.parser')
        
        enlarge_img = HM_soup.find("div", class_="downloads")
        hemisphere_url = enlarge_img.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": hemisphere_url})

    Mars_dict = {    
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": str(mars_facts),
        "hemisphere_images": hemisphere_image_urls}
        
    browser.quit()
    return Mars_dict




        
       
