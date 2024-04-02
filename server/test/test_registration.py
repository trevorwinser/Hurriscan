import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    
    driver = webdriver.Chrome()
    
    # driver_path = 'C:\\Users\\ksing\\Downloads\\chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=driver_path)
    # driver.get('http://127.0.0.1:5000/temperature-predictions')
    
    driver.get('http://127.0.0.1:5000/sign-up')
    yield driver
    driver.quit()

def test_registration_page_load(browser):
    # Wait for the page title to contain "Registration"
    WebDriverWait(browser, 10).until(EC.title_contains("HurriScan Registration"))
    
    assert "Registration" in browser.title

def test_input_fields(browser):
    # Define the test data
    test_data = {
        "email": "testuser@example.com",
        "firstName": "Test",
        "lastName": "User",
        "phone": "1234567890",
        "username": "testuser",
        "password1": "password",
        "password2": "password",
    }

    # Iterate over the test data, finding each input field by its ID and entering the test data
    for field_id, value in test_data.items():
        input_field = browser.find_element(By.ID, field_id)
        input_field.send_keys(value)

        # Optionally, assert that the inputs contain the expected values
        assert input_field.get_attribute('value') == value

    # Check that all input fields have been filled
    assert browser.find_element(By.ID, "email").get_attribute('value') == test_data["email"]
    assert browser.find_element(By.ID, "firstName").get_attribute('value') == test_data["firstName"]
    assert browser.find_element(By.ID, "lastName").get_attribute('value') == test_data["lastName"]
    assert browser.find_element(By.ID, "phone").get_attribute('value') == test_data["phone"]
    assert browser.find_element(By.ID, "username").get_attribute('value') == test_data["username"]
    assert browser.find_element(By.ID, "password1").get_attribute('value') == test_data["password1"]
    assert browser.find_element(By.ID, "password2").get_attribute('value') == test_data["password2"]
