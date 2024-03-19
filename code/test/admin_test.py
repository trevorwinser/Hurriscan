import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    # Initialize WebDriver needed for Selenium web automation tests
    driver = webdriver.Chrome()  # You can change this to your preferred browser driver
    yield driver
    driver.quit()

def test_admin_page(browser):
    # Open the admin page
    browser.get('http://127.0.0.1:5000/admin')

    # Check if the page title contains "Admin Dashboard"
    assert "Admin Dashboard" in browser.title

    # You can add more assertions to verify elements or functionalities on the admin page

def test_users_page(browser):
    # Open the users page
    browser.get('http://127.0.0.1:5000/users')

    # Check if the page title contains "Users"
    assert "Users" in browser.title

    # You can add more assertions to verify elements or functionalities on the users page

# Run the tests
if __name__ == "__main__":
    pytest.main()
