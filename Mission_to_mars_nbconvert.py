#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import requests

import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# In[ ]:

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


url = 'https://mars.nasa.gov/news/'

browser.visit(url)

html = browser.html

soup = BeautifulSoup(html, 'html.parser')


# In[ ]:


news_title = soup.find_all('div', class_='content_title')[1].text
news_p = soup.find_all('div', class_='article_teaser_body')[0].text

print(news_title)
print("--------------------------------------------------------------------")
print(news_p)


# In[5]:


jet_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

browser.visit(jet_url)

html = browser.html

img_soup = BeautifulSoup(html, 'html.parser')

# img = img_soup.find_all('img')[3]["src"]
# img= img_soup.find_all("img")[3]['src']
# featured_image_url = jet_url + img
# print(featured_image_url)


# In[6]:


img_url = img_soup.find('li', class_='slide').a['data-fancybox-href']
featured_image_url = f'https://www.jpl.nasa.gov{img_url}'
print(featured_image_url)


# In[7]:


url_facts = 'https://space-facts.com/mars/'

tables = pd.read_html(url_facts)
len(tables)


# In[8]:


print(type(tables))
print(type(tables[0]))


# In[9]:


df = tables[0]
df


# In[10]:


df.columns =['Description', 'Mars'] 


# In[11]:


df.set_index('Description', inplace=True)
df.head()


# In[12]:


df.to_html('Mars_facts.html')


# In[16]:


USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(USGS_url)
Hem_html = browser.html
hemispheres_soup = BeautifulSoup(Hem_html, 'html.parser')


# In[22]:


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
    
    print(hemisphere_image_urls)


# In[ ]:




