import pytest
from selenium import webdriver
import sqlite3
import time

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_admin_page(browser):
    browser.get('http://127.0.0.1:5000/admin')
    assert "Admin Dashboard" in browser.title

def test_delete_user(browser):
    browser.get('http://127.0.0.1:5000/admin')
    browser.execute_script("deleteUser(1)")
    conn = sqlite3.connect('hurriscan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE id = 1;')
    assert cursor.fetchall() is None, "User with ID 1 still in database" 

def test_create_alert(browser):
    browser.get('http://127.0.0.1:5000/admin')
    browser.find_element_by_id('title').send_keys('Test Alert')
    browser.find_element_by_id('text').send_keys('This is a test alert')
    browser.find_element_by_css_selector('#create-alert button[type="submit"]').click()
    conn = sqlite3.connect('hurriscan.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Alert WHERE title = "Test Alert" AND text = "This is a test alert";')
    assert cursor.fetchone() is not None, "Alert was not created in the database"
    conn.close()

def test_display_user_info(browser):
    browser.get('http://127.0.0.1:5000/admin')
    button = browser.find_element_by_xpath("//button[contains(text(), 'Display User Information')]")
    button.click()
    time.sleep(2) 
    table = browser.find_element_by_id('user-table')
    assert table.is_displayed(), "User table is not displayed"

if __name__ == "__main__":
    pytest.main()
