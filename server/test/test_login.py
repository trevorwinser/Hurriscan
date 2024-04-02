import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Attempt to initialize a Chrome WebDriver instance
    driver = webdriver.Chrome()
    # If successful, open a website (e.g., Google)
    driver.get("http://www.google.com")
    # Print a success message
    print("Chrome WebDriver is installed and working.")
except Exception as e:
    # If an error occurs, print the error
    print(f"An error occurred: {e}")
finally:
    # Close the browser window
    driver.quit()


@pytest.fixture
def browser():
    
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000/login')
    yield driver
    driver.quit()
    
    
def test_default_page_load(browser):
    WebDriverWait(browser, 10).until(EC.title_contains("Login"))
    assert "Login" in browser.title


def test_input_fields(browser):
    # Find the username input field by its ID and enter text
    username_input = browser.find_element(By.ID, "username")
    username_input.send_keys("testuser")

    # Find the password input field by its ID and enter text
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("testpass")

    # Optionally, you can assert that the inputs contain the expected values
    assert username_input.get_attribute('value') == 'testuser'
    assert password_input.get_attribute('value') == 'testpass'