import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    
    # Подключение к Selenium Grid
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',  # Укажи свой URL для Grid
        options=chrome_options
    )
    yield driver
    driver.quit()