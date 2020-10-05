from django.shortcuts import render
import urllib.request
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time, sys, os
from selenium.webdriver.firefox.options import Options

# Create your views here.

def insert_scraper_input(request):
    return render(request, 'giphy/index.html' )

def startscraper(request):
    #search_term = input("Please enter the search term to scrape in giphy.com\n").replace(" ", "-")
    
    search_term=input1 = request.POST['input1'].replace(" ", "-")

    #number_of_gifs = "-1"
    number_of_gifs = request.POST['input2']
    while not (number_of_gifs.isdigit() or number_of_gifs == "All"):
        number_of_gifs = input("""Please insert the number of gifs you want to scrape. Program can scrape 100 gifs every 5 minutes.
    If you want to scrape all gifs, please type "All":\n""")
    

    #Options for Firefox not to show on browser

    options = Options()
    options.headless = True

    #enable Selenium for Firefox
        #driver = webdriver.Firefox()
    driver = webdriver.Firefox(options=options,executable_path=GeckoDriverManager().install())

    driver.get('https://giphy.com/search/' + search_term)

    #wait for page to load

    time.sleep(4)

    #Calculate total elements:

    total_gifs_element = driver.find_elements_by_class_name("NumberDisplay-sc-3pgyh3")
    total_gifs_number = int(total_gifs_element[0].get_attribute('data-gif-count').replace(".", "").replace(",", ""))

    #obtain number of gifs

    if number_of_gifs=="All":
        number_of_gifs = total_gifs_number
    else: 
        number_of_gifs=int(number_of_gifs)

    #obtain gifs for the first page

    elements=[]
    elements = driver.find_elements_by_class_name("giphy-gif-img")
    gifs=[el.get_attribute('src') for el in elements]
    cleanedgifs=[gif for gif in gifs if ".gif" in gif]

    #create new folder

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, search_term)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    #save first gifs in the root folder
    count = 0
    for gif in cleanedgifs:

        if count > number_of_gifs:
            break 
        urllib.request.urlretrieve(gif, os.path.join(search_term,search_term + str(count) + ".gif"))
        count +=1

    #Start scrolling down until number of gifs have been reached

    while count <= number_of_gifs:
        if count > number_of_gifs: 
            break
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)

        #Get only gif files

        elements = driver.find_elements_by_tag_name("img")
        gifs=[el.get_attribute('src') for el in elements]
        cleanedgifs=[gif for gif in gifs if ".gif" in gif]
            
        for gif in cleanedgifs:
            if count > number_of_gifs:
                break
            urllib.request.urlretrieve(gif, os.path.join(search_term,search_term + str(count) + ".gif"))
            count +=1
    
    context = {}
    context['gifs_scraped'] = count - 1
    return render(request, 'giphy/results.html', context )


