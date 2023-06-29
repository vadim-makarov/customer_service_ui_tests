"""Standard module for fixtures"""
from typing import Generator

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from config import URLs
from models import generate_phone_number, NewUser, NewService, NewReview
from ui_tests.pages.main_page import MainPage


@pytest.fixture
def driver(request) -> Generator:
    """
    the fixture downloads the latest driver and creates the browser instance with passed options
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    failed_before = request.session.testsfailed
    yield browser
    if request.session.testsfailed != failed_before:
        test_name = request.node.name
        screenshot(browser, test_name)
    browser.quit()


@pytest.fixture
def main_page(driver) -> MainPage:
    """Открывает главную страницу"""
    page = MainPage(driver)
    page.open(URLs.main_page_url)
    return page


def screenshot(browser: WebDriver, name: str) -> None:
    """
    Gets a screenshot and attaches it to the report
    """
    allure.attach(browser.get_screenshot_as_png(), name=f"Screenshot {name}", attachment_type=AttachmentType.PNG)


@pytest.fixture
def user() -> NewUser:
    """Returns a user instance for testing"""
    test_user = NewUser()
    return test_user


@pytest.fixture
def phone_number() -> str:
    """Generates a random phone number"""
    number = generate_phone_number()
    return number


@pytest.fixture
def service():
    """Returns a service instance for testing"""
    service = NewService()
    return service


@pytest.fixture
def review():
    """Returns a review instance for testing"""
    review = NewReview()
    return review
