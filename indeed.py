import requests
from bs4 import BeautifulSoup
import time, random
import pymysql.cursors
import re
from bs4 import BeautifulSoup
import pandas as pd


session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"})
indeed_cookies = session.get("https://www.indeed.com")
view_job_url = "https://www.indeed.com/viewjob?jk="

query = "Software Engineer New Grad"
location = "United States"
stop_on_page = 8
age = 4

job_titles = []
employers = []
locations = []
scraped_apply_urls = []
scraped_job_locations = []
scraped_ratings = []

page = 0
for i in range(int(stop_on_page)):

    programmer = session.get(f"https://www.indeed.com/jobs?q={query}&l={location}&start={page}&fromage={age}")
    
    soup = BeautifulSoup(programmer.text, "html.parser")

    t = soup.findAll('a')    
    jobs = soup.findAll('a', attrs={"data-tn-element": "jobTitle"})
    #companies = soup.findAll('a', attrs={"data-tn-element": "companyName"})
    jobs_div = soup.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
    loc_div = soup.find_all('div', attrs={'class': 'recJobLoc'}) 
    for job in jobs:
        job_titles.append(job.get('title'))
    # for company in companies:
    #     employers.append(company.text.strip())

    for div in jobs_div:
        job_id = div.attrs['data-jk']
        apply_url = view_job_url + job_id
        scraped_apply_urls.append(apply_url)
        rating_span = div.find('span', attrs={'class':  "ratingsContent"})
        company = div.find('a', attrs={"data-tn-element": "companyName"})
        if rating_span:
            scraped_ratings.append(float(rating_span.text.strip().replace(',', '.')))
        else:
            scraped_ratings.append(None)

        if company:
            employers.append(company.text.strip())
        else:
            employers.append(None)

    for loc in loc_div:
        loc_attrs = loc.attrs
        scraped_job_locations.append(loc_attrs["data-rc-loc"])
    page += 10

while len(employers) != len(job_titles):
    employers.append("NaN")

job_data = pd.DataFrame({'Company': employers,
'Post': job_titles,
'Location': scraped_job_locations,
'Link' : scraped_apply_urls,
'Rating' : scraped_ratings
})


job_data.to_csv('Indeed_jobs.csv', index=0)


