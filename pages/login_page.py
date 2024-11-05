from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"

    def open(self):
        """Открыть страницу логина."""
        self.driver.get(self.url)

    def click_customer_login(self):
        """Нажать на кнопку 'Customer Login'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Customer Login')]"))
        ).click()

    def select_user_by_name(self, user_name):
        """Выбрать пользователя из выпадающего списка по имени."""
        user_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "userSelect"))
        )
        user_dropdown.click()
        user_dropdown.find_element(By.XPATH, f"//option[contains(text(), '{user_name}')]").click()

    def click_login(self):
        """Нажать на кнопку 'Login' для завершения логина."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        ).click()

    def is_welcome_message_displayed(self, user_name):
        """Проверить, что отображается приветственное сообщение с именем пользователя."""
        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//strong[contains(text(), 'Welcome')]/span[contains(text(), '{user_name}')]"))
        )
        return user_name in welcome_message.text