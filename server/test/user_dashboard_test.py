from selenium import webdriver
from selenium.webdriver.common.keys import Keys

flask_url = "http://127.0.0.1:5000/user_dashboard"

def run_selenium_test():
    driver = webdriver.Chrome()

    try:
        driver.get(flask_url)
        perform_date_filter(driver)
        perform_temperature_range_filter(driver)

    finally:
        driver.quit()

def perform_date_filter(driver):
    filter_date_input = driver.find_element_by_id("filter-date")
    filter_date_input.send_keys("1992-03")
    apply_filter_button = driver.find_element_by_xpath("//button[contains(text(),'Apply Date')]")
    apply_filter_button.click()

def perform_temperature_range_filter(driver):
    min_temperature_input = driver.find_element_by_id("min-temperature")
    min_temperature_input.send_keys("20")

    max_temperature_input = driver.find_element_by_id("max-temperature")
    max_temperature_input.send_keys("30")

    apply_temperature_button = driver.find_element_by_xpath("//button[contains(text(),'Apply Temperature')]")
    apply_temperature_button.click()

run_selenium_test()
