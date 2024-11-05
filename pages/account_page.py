from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AccountPage:
    def __init__(self, driver):
        self.driver = driver

        # Локаторы
        self.deposit_button = (By.XPATH, "//button[normalize-space()='Deposit']")
        self.amount_input = (By.XPATH, "//input[@placeholder='amount']")
        self.confirm_deposit_button = (By.XPATH, "//button[@type='submit']")
        self.withdraw_button = (By.XPATH, "//button[normalize-space()='Withdrawl']")
        self.success_message_deposit = (By.XPATH, "//span[contains(@class, 'error') and contains(text(),'Deposit Successful')]")
        self.success_message_withdrawn = (By.XPATH, "//span[contains(text(),'Transaction successful')]")
        self.balance_field = (By.XPATH, "//div[@class='center']//strong[2]")
        self.withdraw_label = (By.XPATH, "//label[normalize-space()='Amount to be Withdrawn :']")
        self.transactions_button = (By.XPATH, "//button[normalize-space()='Transactions']")
        self.transaction_table = (By.XPATH, "//table[@class='table table-bordered table-striped']")
        self.transaction_rows = (By.XPATH, "//table[@class='table table-bordered table-striped']/tbody/tr")

    def take_screenshot(self, filename="screenshot.png"):
        """Сохранить скриншот страницы."""
        self.driver.save_screenshot(filename)
        print(f"Скриншот сохранен как {filename}")

    def deposit(self, amount):
        """Выполняет депозит на заданную сумму с отладочными выводами."""
        try:

            # Проверка на доступность кнопки Deposit
            deposit_btn = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.deposit_button)
            )

            deposit_btn.click()
            self.take_screenshot("after_deposit_click.png")

            # Вводим сумму депозита
            amount_field = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.amount_input)
            )
            amount_field.clear()
            amount_field.send_keys(str(amount))

            # Подтверждение депозита
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.confirm_deposit_button)
            ).click()

            # Проверка, что депозит успешно выполнен
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.success_message_deposit)
            )
            print("Депозит успешно выполнен.")
            self.take_screenshot('success_deposit.png')

        except TimeoutException as e:
            print("Ошибка: сообщение 'Deposit Successful' не найдено.")
            self.take_screenshot("error_deposit_click.png")
            raise e

    def withdraw(self, amount):
        """Выполняет снятие средств на заданную сумму с отладочными выводами."""
        try:

            # Проверка доступности кнопки Withdraw
            withdraw_btn = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.withdraw_button)
            )

            withdraw_btn.click()

            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.withdraw_label)
            )

            # Вводим сумму для снятия
            amount_field = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.amount_input)
            )
            amount_field.clear()
            amount_field.send_keys(str(amount))

            # Подтверждение снятия
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.confirm_deposit_button)
            ).click()

            # Проверка, что снятие успешно выполнено
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.success_message_withdrawn)
            )
            print("Снятие успешно выполнено.")
            self.take_screenshot('success_withdraw.png')

        except TimeoutException as e:
            print("Ошибка: текст 'Amount to be Withdrawn' не найден или не отображается.")
            self.take_screenshot("error_withdraw_label.png")
            raise e
        
    def verify_balance(self, expected_balance):
        """Проверяет, что текущий баланс соответствует ожидаемому значению."""
        try:
            balance_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.balance_field)
            )
            balance_text = balance_element.text.strip()
            print("Текущий баланс:", balance_text)
            
            assert balance_text == str(expected_balance), f"Ожидаемый баланс: {expected_balance}, но получено: {balance_text}"
            print("Баланс успешно проверен и соответствует ожидаемому.")

        except TimeoutException as e:
            print("Ошибка: баланс не найден или не отображен.")
            raise e

    def view_transactions(self):
        """Переходит на страницу транзакций, проверяет наличие таблицы и возвращает данные транзакций."""
        try:
            
            transactions_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.transactions_button)
            )
            transactions_btn.click()
            
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.transaction_table)
            )
            print("Таблица транзакций успешно найдена.")

            transactions = self._get_transactions_data()

            if not transactions:
                print("Транзакции не найдены, обновляем страницу и повторяем попытку.")
                self.driver.refresh()
                
                transactions_btn = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(self.transactions_button)
                )
                transactions_btn.click()
                
                WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located(self.transaction_table)
                )
                print("Таблица транзакций найдена после обновления страницы.")

                transactions = self._get_transactions_data()

            if not transactions:
                print("Транзакции отсутствуют после повторного обновления страницы.")
            else:
                print(f"Найдено {len(transactions)} транзакций.")

            return transactions

        except TimeoutException as e:
            print("Ошибка: таблица транзакций не найдена.")
            self.take_screenshot("error_transactions.png")
            raise e

    def _get_transactions_data(self):
        """Извлекает данные транзакций из таблицы, если она доступна."""
        transactions = []
        rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.transaction_rows)
        )
        for row in rows:
            date = row.find_element(By.XPATH, "./td[1]").text
            amount = row.find_element(By.XPATH, "./td[2]").text
            transaction_type = row.find_element(By.XPATH, "./td[3]").text
            transactions.append({
                "date": date,
                "amount": amount,
                "type": transaction_type
            })
        return transactions