#dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #us mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_result = soup.find('div',class_='list_text')
    
    try:
        title = latest_result.find('div', class_='content_title').text
        paragraph = latest_result.find('div', class_='article_teaser_body').text
    except:
        title = ""
        paragraph = ""
        print("missing info")
        
    #featured mars images
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html2 = browser.html
    soup = BeautifulSoup(html2, "html.parser")

    featured_result = soup.find('article', class_="carousel_item")["style"]
    path = featured_result.split("'")[1]

    featured_url = "https://www.jpl.nasa.gov"+path
    
    #mars facts
    table = pd.read_html("https://space-facts.com/mars/")
    
    quick_facts = table[0]
    quick_facts_html = quick_facts.to_html(index=False, header=False)

    #mars hemispheres
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_hemispheres = []
    hemisphere_results = soup.find_all('div', class_="item")

    for results in hemisphere_results:
        hemisphere_title = results.find('h3').text
        hemisphere_image_url = "https://astrogeology.usgs.gov" + results.find('a')['href']

        browser.visit(hemisphere_image_url)
        html = browser.html

        soup = BeautifulSoup(html, "html.parser")
        hemisphere_image_url_new = soup.find('div', class_="downloads").find('a')['href']

        hemisphere_dictionary = {
            "title":hemisphere_title,
            "url":hemisphere_image_url_new
        }
        mars_hemispheres.append(hemisphere_dictionary)
        
    browser.quit()
        
    Mars_Data = {
        "title":title,
        "paragraph":paragraph,
        "featured_image_link":featured_url,
        "quick_facts":quick_facts_html,
        "hemispheres":mars_hemispheres
    }
    
    return Mars_Data
