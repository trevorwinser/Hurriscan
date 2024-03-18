from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, os

driver = webdriver.Chrome(ChromeDriverManager().install())
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
alerts_html_path = os.path.join(parent_dir, 'templates', 'alerts.html')
driver.get("file:///" + alerts_html_path)
wait = WebDriverWait(driver, 10)
try:
    east_coast_checkbox = wait.until(EC.presence_of_element_located((By.ID, "east-coast")))
except TimeoutException:
    print("Timed out waiting for the element to appear.")

east_coast_checkbox = driver.find_element(By.ID, "east-coast")
west_coast_checkbox = driver.find_element(By.ID, "west-coast")
east_coast_checkbox.click()  
west_coast_checkbox.click()  

phone_input = driver.find_element(By.ID, "phone")
phone_input.send_keys("7894563333")

email_input = driver.find_element(By.ID, "email")
email_input.send_keys("mock@gmail.com")

submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
submit_button.click()

time.sleep(3)

driver.quit() 