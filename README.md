# JobScrapping
Had written these scripts last year to find the most recently posted jobs within the last one or two days - as some job postings would be taken down if the number of applications reached the required count. 

Reference : https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b

### Indeed 

Referencing the above mentioned blog post I had used BeautifulSoup. The query, location and age (no of days) variables would have to be changed based on what you want. To auto-run the script at required frequency you can use crontab

![Example of CSV created](/assets/images/tux.png)


### LinkedIn

Using the same format, and referring to other online resources, I had tried web-scrapping LinkedIn. The GeoId for location is a part of LinkedIn's URL, and thus the entire URL will have to be changed to run this script. The script will also require some changes if LinkedIn's URL design and/or HTML format has changed - so I am not sure if it is currently functional or not!
