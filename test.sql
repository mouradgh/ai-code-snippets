import requests
from bs4 import BeautifulSoup

url = 'https://www.linkedin.com/jobs/search/?keywords=data%20engineer&location=United%20States'

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

job_list = soup.find_all('li', {'class': 'result-card'})

for job in job_list:
    job_title = job.find('span', {'class': 'screen-reader-text'}).text.strip()
    company_name = job.find('a', {'class': 'result-card__subtitle-link'}).text.strip()
    location = job.find('span', {'class': 'job-result-card__location'}).text.strip()
    job_link = job.find('a').get('href')

    # Save job data to a database or file
