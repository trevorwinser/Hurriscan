import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    # Initialize WebDriver needed for Selenium web automation tests
    driver = webdriver.Chrome()  
    driver.get('http://127.0.0.1:5000/data-visualization/94/8')
    yield driver
    driver.quit()

def test_default_page_load(browser):
    # Ensures the "Monthly Weather Data" page is correctly loaded.
    assert "Monthly Weather Data" in browser.title

def test_chart_data(browser):
    # Interact with the year and month dropdowns
    Select(browser.find_element_by_id('year')).select_by_visible_text('1994')
    Select(browser.find_element_by_id('month')).select_by_visible_text('August')
    browser.find_element_by_id('submit').click()
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'weatherChart'))
    )

    # Assert the chart is displayed
    assert browser.find_element_by_id('weatherChart').is_displayed()
