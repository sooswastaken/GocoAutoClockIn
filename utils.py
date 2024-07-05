from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

try:
    with open('auth.json') as f:
        auth = json.load(f)
        username = auth['username']
        password = auth['password']
except FileNotFoundError:
    print("No auth.json file found. Please create one with your username and password.")
    exit(1)


def click_punch(test=False):
    driver = webdriver.Chrome()
    driver.get('https://secure.goco.io/companies/genesys-works/home')

    time.sleep(6)
    username_field = driver.find_element('id', 'field_1')
    username_field.send_keys(username)
    time.sleep(1)

    password_field = driver.find_element('id', 'field_2')
    password_field.send_keys(password)

    login_button = driver.find_element('class name', 'login-button')
    login_button.click()
    time.sleep(10)
    punch_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="clock-in-out"]')
    punch_button.click()

    if test:
        time.sleep(5)
        punch_button.click()
        time.sleep(5)
