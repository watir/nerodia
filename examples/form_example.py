# Based on http://watir.com/guides/form-example/

from nerodia.browser import Browser
#from selenium.webdriver.common.keys import Keys #needed to send keys
from time import sleep  # needed to perform sleep
from faker import Faker  # needed for fake form data
import os # needed for file path

# Setup
browser = Browser(browser='chrome')
browser.window().maximize()

# Navigate to the Page
browser.goto('a.testaddressbook.com')

# Authenticate and Navigate to the Form
browser.link(id='sign-in').click()
browser.text_field(data_test='email').set('watir_example@example.com')
browser.text_field(data_test='password').set('password')
browser.button(name='commit').click()
browser.link(data_test='addresses').click()
browser.link(data_test='create').click()

# This uses the Faker Library to give us Random Data.
# Read more about Faker Library here: https://pypi.org/project/Faker/

fake = Faker()  # So we can use fake.name() instead of Faker().name()
browser.text_field(id='address_first_name').set(fake.first_name())
browser.text_field(id='address_last_name').set(fake.last_name())
browser.text_field(id='address_street_address').set(fake.street_address())
browser.text_field(id='address_secondary_address').set(fake.secondary_address())
browser.text_field(id='address_city').set(fake.city())
 
# Select list elements can select by either `text` or `value`
browser.select_list(id='address_state').select(fake.state())

browser.text_field(id='address_zip_code').set(fake.postcode())

# Radio buttons can be selected with `text` or `label` locators
browser.radio(text='Canada').set()

# Date Field elements accept Date objects
birthday = fake.date_of_birth()
browser.date_field(id='address_birthday').set(birthday)

age = fake.date_time_this_year().year - birthday.year
browser.text_field(id='address_age').set(age)

browser.text_field(id='address_website').set(fake.url())

# File Field elements upload file with the '#set' method, but require the full system path
file_name = 'nerodia_example.txt'
file = open(file_name, 'w+').close()
path = os.path.realpath(file_name)
browser.file_field(id='address_picture').set(path)

# Checkboxes can be selected by 'label' or 'text' locators
browser.checkbox(label='Dancing').set()
browser.checkbox(name='address[interest_climb]').set()

browser.textarea(id='address_note').set('See, filling out a form with Nerodia is as easy as with Watir!')
browser.button(data_test='submit').click()

sleep(3)

browser.quit()
