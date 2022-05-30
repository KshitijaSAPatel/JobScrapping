# importing packages
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from IPython.core.display import clear_output
from random import randint
from requests import get
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time
start_time = time()

from warnings import warn

job_id = []
post_title = []
company_name = []
post_date = []
job_location = []

driver = webdriver.Chrome()
no_of_jobs = 5
keyword = "Software New Grad"
location = "United States"

i = 0
while i < (no_of_jobs/25): 
    i += 1
    url = ("https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=103644278&keywords={}&location={}&pageNum={}".format(keyword, location, i))
    
    driver.get(url)
    sleep(3)
    action = ActionChains(driver)

    pageSource = driver.page_source
    lxml_soup = BeautifulSoup(pageSource, 'lxml')

    job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')

    print('You are scraping information about {} jobs from page {}'.format(len(job_container), i))


    for job in job_container:
        
        job_titles = job.find('span', class_ = 'screen-reader-text').text
        #print(job_titles)
       job_titles = job.find("span").text
       post_title.append(job_titles)

       #job_ids = job.find('a', href=True)['href']
       job_ids = job.find('a')['href']
       job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
       job_id.append('https://www.linkedin.com/jobs/view/' + job_ids + '/')

       company_names = job.select_one('img')['alt']
       company_name.append(company_names)

       #job_locations = job.find("span", class_="job-result-card__location").text
       job_locations = job.find("span").text
       job_location.append(job_locations)

       post_dates = job.select_one('time')['datetime']
       post_date.append(post_dates)


job_data = pd.DataFrame({'Date': post_date,
'Company': company_name,
'Post': post_title,
'Location': job_location,
'Link' : job_id
})


job_data.to_csv('LinkedIn_jobs.csv', index=0)
