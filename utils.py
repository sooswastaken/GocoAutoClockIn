from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

from selenium.webdriver.firefox.options import Options

try:
    with open('auth.json') as f:
        auth = json.load(f)
        username = auth['username']
        password = auth['password']
except FileNotFoundError:
    print("No auth.json file found. Please create one with your username and password.")
    exit(1)


def click_punch(test=False):
    # Specify options fo firefox
    # Define the geolocation for Virginia
    latitude = 38.8943542
    longitude = -77.439226
    accuracy = 100  # You can adjust the accuracy as needed

    # Set Firefox options
    options = Options()
    options.set_preference("geo.enabled", True)
    options.set_preference("geo.provider.use_corelocation", True)
    options.set_preference("geo.prompt.testing", True)
    options.set_preference("geo.prompt.testing.allow", True)

    # Use the manual geolocation provider with updated coordinates
    location_data = '{"location": {"lat": ' + str(latitude) + ', "lng": ' + str(longitude) + '}, "accuracy": ' + str(accuracy) + '}'

    # Use the manual geolocation provider with updated coordinates
    options.set_preference("geo.provider.network.url", f'data:application/json,{location_data}')

    driver = webdriver.Firefox(options=options)


    # Initialize the driver with the specified service and options
    # driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://secure.goco.io/companies/genesys-works/home')

    time.sleep(12)
    username_field = driver.find_element('id', 'field_1')
    username_field.send_keys(username)
    time.sleep(1)

    password_field = driver.find_element('id', 'field_2')
    password_field.send_keys(password)

    login_button = driver.find_element('class name', 'login-button')
    login_button.click()
    time.sleep(15)
    punch_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="clock-in-out"]')
    punch_button.click()

    if test:
        time.sleep(5)
        punch_button.click()
        time.sleep(5)
    driver.quit()
