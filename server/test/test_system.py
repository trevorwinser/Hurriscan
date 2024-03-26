import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    # Setup: this part runs before each test
    driver = webdriver.Chrome()  # adjust this based on your WebDriver
    yield driver
    # Teardown: this part runs after each test
    driver.quit()

def test_home_page_title(browser):
    browser.get('http://127.0.0.1:5000/')  
    assert 'App Title' in browser.title
