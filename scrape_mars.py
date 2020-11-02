from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import requests

import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # Mars_dict = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all (class_="content_title")
    title_info = soup.find_all (class_="article_teaser_body")

    news_title = title[1].find('a').text
    news_p = title_info[0].text
    # news_p = soup.find('div', class_='article_teaser_body')
    print(news_title)
    print("--------------------------------------------------------------------")
    print(news_p)

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

    # df.to_html('Mars_facts.html')
    mars_facts = df.to_html(header=True, index=True)

    geology_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(geology_url)

    html = browser.html

    geology_soup = BeautifulSoup(html, "html.parser")

    main_geology = "https://astrogeology.usgs.gov"


    class_url = geology_soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hemisphere_url = []

    for sphere in class_url:
        sphere_url = sphere.find('a')['href']
        hemisphere_url.append(sphere_url)
    
    hemisphere_image_urls = []
    for img in hemisphere_url:
        img_url = main_geology + img
    
        browser.visit(img_url)
    
        html = browser.html

        sphere_soup = BeautifulSoup(html, "html.parser")

        img_title = sphere_soup.find("h2", class_="title").text
    
        title= img_title.split(' Enhanced')[0]
      
        img_url = sphere_soup.find("li").a['href']
    
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        # print(hemisphere_image_url)


        Mars_dict = {    
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_facts": str(mars_facts),
            "mars_facts": mars_facts,
            "hemisphere_images": hemisphere_image_urls
            }

    
        
    browser.quit()
    return(Mars_dict)





        
       
