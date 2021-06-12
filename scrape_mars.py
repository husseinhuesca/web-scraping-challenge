# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    ## SetUp browser ##
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ###NASA MARS NEWS ###
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)
    mars_html = browser.html
    mars_soup = bs(mars_html, 'html.parser')
    latest_title = mars_soup.find_all('div', class_= 'content_title')[0].text
    teaser_body = mars_soup.find_all('div', class_= 'article_teaser_body')[0].text
    browser.quit()
    
    ## SetUp browser ##
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    ### JPL MARS SPACE IMAGES - FEATURES IMAGE ###
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    browser.quit()
    featured_image_url = image_soup.find_all('img', class_= 'headerimage fade-in')
    featured_image_urlvf = 'https://spaceimages-mars.com/'+featured_image_url[0]['src']
    
    ## SetUp browser ##
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    ###MARS FACTS###
    marsfact_url = 'https://galaxyfacts-mars.com/'
    marsprofile = pd.read_html(marsfact_url)
    marsprofile
    marsfacts=marsprofile[0]
    marsfacts=marsfacts.rename(columns={0:"Description",1:"Values Mars", 2:"Values Earth"},errors="raise")
    marsfacts.set_index("Description",inplace=True)
    marsfacts = marsfact.to_dict()
    
    
    
    ### MARS HEMISPHERES ###
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    url_hemisphere_data = []
    marshemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheresvf = marshemispheres.find_all('div', class_='item')

    for cont in mars_hemispheresvf:
    # Tiitle and Image
        mhem = cont.find('div', class_="description")
        title = mhem.h3.text
        mhemisphere_link = mhem.a["href"]    
        browser.visit(hemispheres_url + mhemisphere_link)
        marsimage_html = browser.html
        marsimage_soup = bs(marsimage_html, 'html.parser')
    
        marsimage_link = marsimage_soup.find('div', class_='downloads')
        marsimage_url = marsimage_link.find('li').a['href']
        marsimage_url_vf = hemispheres_url + marsimage_url
    
        #Append the dictionary with the image url string and the hemisphere title to a list. 
        #This list will contain one dictionary for each hemisphere.
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = marsimage_url_vf
        url_hemisphere_data.append(image_dict)

    url_hemisphere_data
    

    marschallenge_dict = {
        "latest_title": latest_title,
        "teaser_body": teaser_body,
        "featured_image_url": featured_image_urlvf,
        "fact_html_table": marsfacts,
        "hemisphere_images": url_hemisphere_data
    }

    # Close the browser after scraping
    browser.quit()

    return marschallenge_dict