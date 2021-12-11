import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
import datetime
from email_functionality import *
import os
import time
from constants import *
import lxml

start_time = time.time()
email = linkedin_email
password = linkedin_password

client = requests.Session()


html = client.get(LINKEDIN_LOGIN_URL).content
soup = BeautifulSoup(html, "html.parser")
csrf = soup.find('input', {'name': 'loginCsrfParam'}).get('value')

login_information = {
    'session_key': email,
    'session_password': password,
    'loginCsrfParam': csrf,
    'trk': 'guest_homepage-basic_sign-in-submit'
}
client.post(LOGIN_URL, data=login_information)
#feed_response = client.get('https://www.linkedin.com/feed').text

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

def add_location_to_url(url: str, location: str) -> str:
    if location != "":
        url += '&location='
        for item in location.split():
            url += item + '%2C%20'
        url = url[:-6]
    return url

def get_jobs_by_jobrole_skillset_location(pages: int, jobrole_skillset: str, location: str) -> list:
    if pages < 1 or len(jobrole_skillset) == 0:
        return []
    res = []
    url = base_job_url
    for val in jobrole_skillset.split():
        url += val + '%20'
    url = url[:-3]
    url = add_location_to_url(url, location)
    for i in range(0,pages*25,25):
        search_url = url + '&start='+str(i)
        jobs_per_page = fetch_data(search_url)

        for job in jobs_per_page:
            res.append(job)
    return res


def get_jobs_with_exp(pages: int, params: str, location: str, exp: list) -> list:
    if pages < 1 or len(params) == 0 or len(exp) == 0:
        return []
    exp.sort()
    base_url = BASE_URL_FOR_SEARCH
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

    url = add_location_to_url(url, location)
    for i in range(0,pages*25,25):
        search_url = url + '&start='+str(i)
        jobs_per_page = fetch_data(search_url)

        for job in jobs_per_page:
            res.append(job)
    return res




jobs = get_jobs_by_jobrole_skillset_location(NUMBER_OF_PAGES, JOB_ROLE, LOCATION)
# get_jobs(2,"python", "noida india")
# get_jobs_with_exp(1,"associate consultant","hyderabad",[1])
# get_jobs_with_exp(1,"associate consultantr","noida india",[1,2,3])

x = datetime.datetime.now()
timestamp = x.strftime("%d-%m-%Y %H-%M-%S")
file_name = 'Jobs list '+timestamp+'.xlsx'


def save_file(jobs,file_name):
    df = pd.DataFrame(jobs, columns=['Role name', 'Company', 'Location', 'Hiring Status', 'Description', 'Post Date',
                                     'Job Link', ''])
    writer = ExcelWriter(file_name)
    df.to_excel(writer, 'List_Of_Jobs', index=False)
    writer.save()



save_file(jobs,file_name)

email_status = send_email(timestamp, file_name)
print(email_status)

# os.remove(file_name)
print("---Time taken for execution: %s seconds ---" % (time.time() - start_time))