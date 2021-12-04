import requests
from bs4 import BeautifulSoup
from config import *

email = email_value
password = password_value

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/lg/login-submit'

html = client.get('https://www.linkedin.com/login?').content
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find('input', {'name': 'loginCsrfParam'}).get('value')

login_information = {
    'session_key': email,
    'session_password': password,
    'loginCsrfParam': csrf,
    'trk': 'guest_homepage-basic_sign-in-submit'
}
client.post(LOGIN_URL, data=login_information)
feed_response = client.get('https://www.linkedin.com/feed').text
#

job_response = client.get('https://www.linkedin.com/jobs/search/?keywords=software%20engineer').text
soup = BeautifulSoup(job_response, "lxml")
jobs = soup.find_all('div',class_='job-search-card')
res = []
for each_job in jobs:
    res.append(each_job.text.replace("\n","").strip())

for each_res in res:
    print(each_res)