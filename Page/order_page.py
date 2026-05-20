import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        self.SEARCH_BOX = (By.NAME, "q")

        self.FIRST_PRODUCT = (
            By.XPATH,
            "(//a[contains(@href,'/products/') or contains(@href,'/product/')])[1]"
        )

        self.NAME = (By.NAME, "name")
        self.PHONE = (By.NAME, "phone")
        self.EMAIL = (By.NAME, "email")
        self.PROVINCE = (By.NAME, "address")
        self.ADDRESS = (By.NAME, "fulladdress")

        self.ADD_TO_CART = (
            By.CSS_SELECTOR,
            "#add-to-cart, button.add-to-cart"
        )

        self.CHECKOUT_BTN = (
            By.CSS_SELECTOR,
            ".linktocheckout.button.red, a[href*='checkout']"
        )

        self.SUBMIT_BTN = (By.ID, "place_order")

    def open(self, url):
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get(url)
            time.sleep(2)
        except Exception:
            self.driver.execute_script("window.stop();")
            time.sleep(2)

    def safe_click(self, locator):
        el = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            el
        )

        time.sleep(1)

        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();",
                el
            )

        time.sleep(1)

    def _type(self, locator, value):
        field = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        field.clear()

        if value:
            field.send_keys(value)

        time.sleep(0.3)

    def search_product(self, keyword):
        search_box = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_BOX)
        )

        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()

        WebDriverWait(self.driver, 20).until(
            lambda d: len(
                d.find_elements(
                    By.XPATH,
                    "//a[contains(@href,'/products/') or contains(@href,'/product/')]"
                )
            ) > 0
        )

        time.sleep(2)

    def click_first_product(self):
        try:
            product = self.wait.until(
                EC.presence_of_element_located(self.FIRST_PRODUCT)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                product
            )

            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].click();",
                product
            )

            time.sleep(2)

        except TimeoutException:
            raise TimeoutException(
                "Không tìm thấy sản phẩm đầu tiên sau khi search."
            )

    def add_to_cart(self):
        self.safe_click(self.ADD_TO_CART)
        time.sleep(2)

    def go_to_checkout_from_popup(self):
        try:
            checkout_btn = self.wait.until(
                EC.element_to_be_clickable(self.CHECKOUT_BTN)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                checkout_btn
            )

            self.driver.execute_script(
                "arguments[0].click();",
                checkout_btn
            )

        except TimeoutException:
            print("Popup checkout không hiện -> vào checkout trực tiếp")
            self.driver.get("https://swe.vn/checkout")

        time.sleep(2)

    def fill_checkout_form(self, name, phone, email, province, address):
        self._type(self.NAME, name)
        self._type(self.PHONE, phone)
        self._type(self.EMAIL, email)
        self._type(self.PROVINCE, province)
        self._type(self.ADDRESS, address)
        time.sleep(1)

    def submit_order(self):
        self.safe_click(self.SUBMIT_BTN)
        time.sleep(2)

    def _get_error_by_text(self, keyword):
        try:
            xpath = (
                "//div[@data-slot='error-message' and "
                f"contains(translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                f"'{keyword.lower()}')]"
            )

            el = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )

            return el.text.strip()

        except TimeoutException:
            return ""

    def _get_validation_message(self, locator):
        try:
            field = self.driver.find_element(*locator)
            validation = field.get_attribute("validationMessage")

            if validation:
                return validation.strip()

        except Exception:
            pass

        return ""

    def get_name_error(self):
        return (
            self._get_error_by_text("họ tên")
            or self._get_error_by_text("tên")
            or self._get_validation_message(self.NAME)
        )

    def get_phone_error(self):
        return (
            self._get_error_by_text("số điện thoại")
            or self._get_error_by_text("điện thoại")
            or self._get_error_by_text("phone")
            or self._get_validation_message(self.PHONE)
        )

    def get_email_error(self):
        return (
            self._get_error_by_text("email")
            or self._get_validation_message(self.EMAIL)
        )

    def get_address_error(self):
        return (
            self._get_error_by_text("địa chỉ")
            or self._get_validation_message(self.ADDRESS)
        )

    def get_province_error(self):
        return (
            self._get_error_by_text("tỉnh")
            or self._get_error_by_text("thành phố")
            or self._get_validation_message(self.PROVINCE)
        )