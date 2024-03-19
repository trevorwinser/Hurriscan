import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_admin_page(browser):
    browser.get('http://127.0.0.1:5000/admin')
    assert "Admin Dashboard" in browser.title

# Run the tests
if __name__ == "__main__":
    pytest.main()
