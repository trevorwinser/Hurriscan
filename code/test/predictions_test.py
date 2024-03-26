import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    driver_path = 'C:\\Users\\ksing\\Downloads\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get('http://127.0.0.1:5000/temperature-predictions')
    yield driver
    driver.quit()

def test_default_page_load(browser):
    assert "Weather Predictions" in browser.title

def test_chart_data(browser):
    # Interact with the year and month dropdowns
    Select(browser.find_element(By.ID, 'month')).select_by_visible_text('August')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'PredictionsChart'))
    )
    # Assert the chart is displayed
    assert browser.find_element(By.ID, 'PredictionsChart').is_displayed()