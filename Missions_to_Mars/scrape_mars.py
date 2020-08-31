
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # I import the code for mission_to_mars.ipynb
    #inital the connection to chrome browser
    browser = init_browser()

    #initial the diction for mongo DB
    marsData={}
    url = 'https://mars.nasa.gov/news/'
    #retrieve the webpage
    response = requests.get(url)
    #BeautifulSoup object
    soup = bs(response.text, 'html.parser')

    #Retrieve the latest subject and content from the Mars website
    news_title = soup.find('div', class_="content_title").find('a').text
    news_p = soup.find('div', class_="rollover_description_inner").text
    print("The new titel is: " + news_title)
    print("-----------------------------------------------------------------")
    print("The content is: " + news_p)
    print("-----------------------------------------------------------------")
    #assign the value to diction
    marsData['latest_news'] = news_title
    marsData['latest_news_content'] = news_p

    # ## JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    #retrieve the webpage
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    #Concatenate sublink and base url
    splinter_url = base_url + soup.find('a', class_="button fancybox")['data-link']
    print("The splinter site url is: " + splinter_url)
    print("-----------------------------------------------------------------")

    #connect url by splinter
    browser.visit(splinter_url)

    base_url = 'https://www.jpl.nasa.gov'
    #splinter
    html = browser.html
    #Parse HTML object with BeautifulSoup
    soup = bs(html, 'html.parser')
    #Concatenate sublink and base url
    featured_image_url = base_url + soup.find('img', class_="main_image")['src']
    print("The featured image link is: " + featured_image_url)
    print("-----------------------------------------------------------------")
    marsData['featured_image_url'] = featured_image_url
    browser.quit()

    # ## Mars Facts
    # *Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # *Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'
    #using table data frame from Mars webpage
    tables = pd.read_html(url)
    tables

    #initial the first column
    df = tables[0]
    #rename column names
    df.columns = ['Facts', 'Value']
    #set the index
    df.set_index('Facts', inplace=True)
    df

    #create HTML table and the bold border 
    html_table = df.to_html(border=3)
    #Remove enter characters 
    marsData['mars_facts_html'] = html_table.replace('\n', '')
    print(marsData['mars_facts_html'])


    # ## Mars Hemispheres
    # *Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # *Use Pandas to convert the data to a HTML table string.

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = "https://astrogeology.usgs.gov"
    #retrieve the webpage
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    #Retrieve all image url to a list
    results = soup.find_all('a', class_="itemLink product-item")
    full_resolution_image_url = []
    for result in results:
        #Concatenate sublink and base url
        full_resolution_image_url.append(base_url + result['href'])
        
    print(full_resolution_image_url)

    #inital the list for the dicton
    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'

    for url in full_resolution_image_url:
        #retrieve the webpage from the new website
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        #Retrieve url to full resolution image
        image_url = soup.find('div', class_="downloads").find('ul').find('li').find('a')['href']
        #Retrieve the subject
        title = soup.find('h2', class_="title").text
        #initial diction and put into list
        resolution_dict = { "title":title,"img_url": image_url }
        hemisphere_image_urls.append(resolution_dict)
        print(title)
        print(image_url)
        print("----------------------------------------------------------------")
    print(hemisphere_image_urls)
    marsData['hemisphere_image_urls'] = hemisphere_image_urls
    #print all data from diction 
    print(marsData)
    # return the data to app.py
    return marsData



