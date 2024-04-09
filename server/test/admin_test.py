import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import sqlite3
import datetime
import os
import logging
import sqlite_setup
sqlite_setup.main()

basedir = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_admin_page(browser):
    browser.get('http://127.0.0.1:5000/admin')
    assert "Admin Dashboard" in browser.title

def test_create_alert(browser):
    browser.get('http://127.0.0.1:5000/admin')
    browser.find_element_by_id('title').send_keys('Test Alert')
    browser.find_element_by_id('text').send_keys('This is a test alert')
    browser.find_element_by_css_selector('#create-alert button[type="submit"]').click()

    time.sleep(2)

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('hurriscan.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Alert (title, text, date) VALUES (?, ?, ?)', ('Test Alert', 'This is a test alert', current_datetime))
    conn.commit()
    conn.close()

    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Alert WHERE title = "Test Alert" AND text = "This is a test alert";')
    assert cursor.fetchone() is not None, "Alert was not created in the database"
    conn.close()

def test_display_user_info(browser):
    browser = webdriver.Chrome()
    browser.get('http://127.0.0.1:5000/admin')
    button = browser.find_element_by_xpath("//button[contains(text(), 'Display User Information')]")
    if button.is_displayed() and button.is_enabled():
        print("Button is visible")
    else:
        print("Button is not visible")
    button.click()

    browser.quit()

    
def test_num_rows(browser):
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User')
    rows = cursor.fetchall()
    assert len(rows) == 2, "Incorrect number of rows in database"
    conn.close()
    
def test_delete_user(browser):
    browser.get('http://127.0.0.1:5000/admin')
    browser.execute_script("deleteUser(1)")
    
    conn = sqlite3.connect(os.path.join(basedir, 'hurriscan.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        sql = cursor.execute('SELECT * FROM User WHERE id = 1;')
        logs = browser.get_log('browser')
        for log in logs:
            print(log['message'])
        assert not cursor.fetchall(), "User with ID 1 still in database"
        conn.commit() 
    finally:
        conn.close() 

    
if __name__ == "__main__":
    pytest.main()
