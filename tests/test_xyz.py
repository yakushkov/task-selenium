from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utils import fibonacci
import datetime
import pytest
import csv
import os
import allure

@pytest.fixture
def deposit_amount():
    # Вычисление числа Фибоначчи
    today = datetime.date.today()
    day = today.day + 1
    return fibonacci(day)

def test_deposit_and_withdraw(driver, deposit_amount):
    """Тест на успешный депозит и снятие средств с проверкой баланса и транзакций."""

    login_page = LoginPage(driver)
    account_page = AccountPage(driver)

    login_page.open()

    # Проверка, что страница загрузилась
    assert "XYZ Bank" in driver.page_source

    login_page.click_customer_login()

    user_name = "Harry Potter"
    login_page.select_user_by_name(user_name)
    login_page.click_login()

    assert login_page.is_welcome_message_displayed(user_name), "Приветственное сообщение не отображается."
    print("Логин как клиент завершен и приветственное сообщение отображено.")

    # Проверка начального баланса
    account_page.verify_balance(0)

    # Пополнение депозита
    print(f"Выполняем депозит на сумму: {deposit_amount}")
    account_page.deposit(deposit_amount)

    # Проверка баланса после депозита
    account_page.verify_balance(deposit_amount)
    print("Баланс после депозита проверен.")

    # Снятие средств
    account_page.withdraw(deposit_amount)

    # Проверка, что баланс снова равен нулю после снятия
    account_page.verify_balance(0)
    print("Баланс после снятия проверен и равен нулю.")

    # Переход к просмотру транзакций и их проверка
    transactions = account_page.view_transactions()
    assert len(transactions) >= 2, "Транзакции не найдены или их меньше двух."

    # Удаление файла перед записью, если он существует
    csv_file = "transactions.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print(f"Старый файл {csv_file} удален.")

    # Запись транзакций в новый CSV файл
    with open(csv_file, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Дата-время", "Сумма", "ТипТранзакции"])  # Заголовок
        for transaction in transactions:
            writer.writerow([transaction["date"], transaction["amount"], transaction["type"]])
    print(f"Транзакции успешно сохранены в файл {csv_file}")

    # Добавляем файл CSV в отчет Allure
    if os.path.exists(csv_file):
        with open(csv_file, "rb") as f:
            allure.attach(f.read(), name="transactions", attachment_type=allure.attachment_type.CSV)
