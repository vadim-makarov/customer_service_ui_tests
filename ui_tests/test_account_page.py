"""Contains account page test class"""

import allure

from models import NewService, NewUser
from ui_tests.pages.account_page import AccountPage
from ui_tests.pages.main_page import MainPage


class TestAccountPage:
    """Contains account page tests"""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User can add a service")
    def test_user_can_add_a_service(self, main_page: MainPage, user: NewUser, service: NewService):
        """User can add a service"""
        main_page.go_to_register_page() \
            .fill_user_data_and_continue(user) \
            .confirm_sms_code() \
            .go_to_account_page() \
            .select_service_and_continue(service) \
            .is_element_present(AccountPage.SERVICE_ALERT, "Запись не создана") \
            .change_service() \
            .is_element_present(AccountPage.SERVICE_ALERT, "Запись не изменена") \
            .delete_service()
        message = main_page.get_text(AccountPage.SERVICE_ALERT)
        assert 'Item deleted.' in message, "Сообщение об удалении записи не получено"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("User can change his data")
    def test_user_can_edit_profile(self, main_page: MainPage, user: NewUser, phone_number: str):
        """User can change his own profile"""
        main_page.go_to_register_page() \
            .fill_user_data_and_continue(user) \
            .confirm_sms_code() \
            .go_to_account_page() \
            .change_profile_data(phone_number) \
            .confirm_sms_code()
        message = main_page.get_text(AccountPage.SERVICE_ALERT)
        assert 'Values have been changed' in message, "Пользовательские данные не изменены"
