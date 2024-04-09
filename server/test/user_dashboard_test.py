import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

flask_url = "http://127.0.0.1:5000/user_dashboard"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()

    driver.get(flask_url)
    yield driver
    driver.quit()
    

def test_perform_date_filter(driver):
    filter_date_input = driver.find_element_by_id("filter-date")
    filter_date_input.send_keys("1992")
    
    apply_filter_button = driver.find_element_by_xpath("//button[contains(text(),'Apply Date')]")
    apply_filter_button.click()
    assert driver.find_element(By.ID, "filter-date").get_attribute('value') == "1992"

def test_perform_temperature_range_filter(driver):
    min_temperature_input = driver.find_element_by_id("min-temperature")
    min_temperature_input.send_keys("20")
    assert driver.find_element(By.ID, "min-temperature").get_attribute('value') == "20"
    max_temperature_input = driver.find_element_by_id("max-temperature")
    max_temperature_input.send_keys("30")
    assert driver.find_element(By.ID, "max-temperature").get_attribute('value') == "30"
    
    apply_temperature_button = driver.find_element_by_xpath("//button[contains(text(),'Apply Temperature')]")
    apply_temperature_button.click()


