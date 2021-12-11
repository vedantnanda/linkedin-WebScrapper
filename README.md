# linkedin-WebScrapper
This is a simple linkedin webscrapper which enables you to automate job searching by sending required list of jobs as an excel to your gmail.

Features:

* Search job as per role name
* Search job as per skillset
* Search job as per role name/skill set + location
* Search job as per role name/skill set + location + experience level
* Send fetched results in excel to desired gmail account

Further scope of this project is to deploy the solution to Azure function which will auto trigger at a specific time each day.

### Snapshot of generated excel
![image](https://user-images.githubusercontent.com/28773842/145672530-c81c13da-27eb-4747-a153-5d5cd7fc2cf7.png)

### Snapshot of delivered email
![image](https://user-images.githubusercontent.com/28773842/145672696-cc4b598d-a1c2-45c0-862b-79bb44ebb80f.png)

## Install following packages:

pip3 install beautifulsoup4

pip3 install lxml

pip3 install pandas

pip3 install openpyxl

## Create config.py file
Add following values:

linkedin_email = ""

linkedin_password = ""

gmail_address = ""

gmail_password = ""

receiver_address = ""

##### Modify below variables as required

NUMBER_OF_PAGES = "5"

JOB_ROLE = "Associate consultant"

LOCATION = "Hyderabad"
