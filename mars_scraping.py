import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import requests
import datetime as dt

def news_scrape(browser):

    browser.visit("https://mars.nasa.gov/news/")
    news_soup = bs(browser.html, 'html.parser')
    results = news_soup.find_all('div', class_='slide')

    for result in results:
        try:
            news_title = result.find('div', class_="content_title").a.text
            news_p = result.find('div', class_="rollover_description_inner").text
     
        except AttributeError:
            return None

    return news_title, news_p

def mars_weather(browser):

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_soup = bs(browser.html, 'html.parser')
    weather_results = weather_soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    for result in weather_results:
        weather_text = result.span.text
    
    return weather_text

def mars_image(browser):
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    image_soup = bs(browser.html, 'html.parser')
    image_results = image_soup.find_all('li', class_="slide")

    for image in image_results:
        try:   
            image = image.img['src']
            image_url = f"https://www.jpl.nasa.gov/{image}"
        except AttributeError:
            return None

    return image_url

def hemispheres(browser):
    astrogeology_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeology_url)
    hemisphere_soup = bs(browser.html, 'html.parser')
    hemisphere_results = hemisphere_soup.find_all('div', class_="item")

    for result in hemisphere_results:
        try:
            hemisphere_title = result.find('div', class_='description').a.text
            hemisphere_url = result.find('div',class_='description').a['href']
        except AttributeError:
            hemisphere_title = None
            hemisphere_url = None
    
    hemispheres = {
                "hemisphere": hemisphere_title,
                "hemisphere_image": hemisphere_url}
    return hemispheres

def mars_fact():
    try:
        fact_df = pd.read_html("https://space-facts.com/mars/")[0]
    except AttributeError:
        return None
    fact_df.columns=['Fact', 'Value']
    fact_df.set_index('Fact', inplace=True)

    return fact_df.to_html(classes="table table-striped")


def scrape():

    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_p = news_scrape(browser)
    time.sleep(1)

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "weather": mars_weather(browser),
        "featured_image": mars_image(browser),
        "hemispheres": hemispheres,
        "facts": mars_fact(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape())

