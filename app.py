import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import datetime
from email_functionality import *
import os
import time

start_time = time.time()
email = linkedin_email
password = linkedin_password

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

def fetch_data(search_url: str) -> list:
    result = []
    job_response = client.get(search_url).text
    soup = BeautifulSoup(job_response, "lxml")
    jobs = soup.find_all('div', class_='job-search-card')

    for each_job in jobs:
        stripping = each_job.text.replace("\n", "").strip()
        splitting = [x for x in re.split("\s{2,}", stripping) if x]
        splitted = splitting[1:]
        splitted.append(each_job.a['href'])
        result.append(splitted)

    return result
base_job_url = 'https://www.linkedin.com/jobs/search/?keywords='

def get_jobs(pages: int, params: str, location: str) -> list:
    if pages < 1 or len(params) == 0:
        return []
    res = []
    url = base_job_url
    for val in params.split():
        url += val + '%20'
    url = url[:-3]
    if location != "":
        url += '&location='
        for item in location.split():
            url += item + '%2C%20'
        url = url[:-6]
    for i in range(0,pages*25,25):
        search_url = url + '&start='+str(i)
        jobs_per_page = fetch_data(search_url)

        for job in jobs_per_page:
            res.append(job)

    # for each_res in res:
    #     print(each_res)
    return res


def get_jobs_with_exp(pages: int, params: str, location: str, exp: list) -> list:
    if pages < 1 or len(params) == 0 or len(exp) == 0:
        return []
    exp.sort()
    base_url = 'https://www.linkedin.com/jobs/search/'
    url = base_url+'?f_E='
    for e in exp:
        if e < 1 or e > 5:
            return []
        url += str(e) + '%2C'
    url = url[:-3]
    res = []
    for val in params.split():
        url += val + '%20'
    url = url[:-3]

    if location != "":
        url += '&location='
        for item in location.split():
            url += item + '%2C%20'
        url = url[:-6]
    print(url)
    for i in range(0,pages*25,25):
        search_url = url + '&start='+str(i)
        jobs_per_page = fetch_data(search_url)

        for job in jobs_per_page:
            res.append(job)

    for each_res in res:
        print(each_res)
    return res

jobs = get_jobs(6,"associate consultant","hyderabad")
# get_jobs(2,"python", "noida india")
# get_jobs_with_exp(1,"associate consultant","hyderabad",[1])
# get_jobs_with_exp(1,"associate consultantr","noida india",[1,2,3])

x = datetime.datetime.now()
timestamp = x.strftime("%d-%m-%Y %H-%M-%S")
file_name = 'Jobs list '+timestamp+'.xlsx'

df = pd.DataFrame(jobs,columns=['Role name', 'Company','Location','Description','Hiring Status','Post Date','Job Link',''])
writer = ExcelWriter(file_name)
df.to_excel(writer,'Sheet1',index=False)
writer.save()

email_status = send_email(timestamp, file_name)
print(email_status)

os.remove(file_name)
print("---Time taken for execution: %s seconds ---" % (time.time() - start_time))