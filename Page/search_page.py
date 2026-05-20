from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)
        self.search_input = (By.ID, "inputSearchAuto")
        self.result_count = (By.XPATH, "//p[contains(@class,'subtxt')]")
        self.result_empty = (
            By.XPATH,
            "//h2[contains(text(),'Không tìm thấy nội dung bạn yêu cầu')]"
        )
        self.popup_close = (
            By.CSS_SELECTOR,
            "button.popup-close, .popup__close, .klaviyo-close-form"
        )

    def _close_popups(self):
        try:
            elements = self.driver.find_elements(*self.popup_close)
            for el in elements:
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

    def _get_visible_search_input(self):
        inp = self.wait.until(EC.visibility_of_element_located(self.search_input))
        self.wait.until(EC.element_to_be_clickable(self.search_input))
        return inp

    def open(self, url):
        self.driver.get(url)
        self._close_popups()

    def search_product(self, keyword: str):
        self._close_popups()

        inp = self._get_visible_search_input()
        inp.click()
        inp.send_keys(Keys.CONTROL + "a")
        inp.send_keys(Keys.DELETE)

        if keyword:
            inp.send_keys(keyword)

        inp.send_keys(Keys.ENTER)

        try:
            self.wait.until(
                lambda d: "/search" in d.current_url
                or any(el.is_displayed() for el in d.find_elements(*self.result_count))
                or any(el.is_displayed() for el in d.find_elements(*self.result_empty))
            )
        except TimeoutException:
            pass

    def get_search_message(self) -> str:
        nodes = self.driver.find_elements(*self.result_count)
        for n in nodes:
            if n.is_displayed() and n.text.strip():
                return n.text.strip()

        nodes = self.driver.find_elements(*self.result_empty)
        for n in nodes:
            if n.is_displayed() and n.text.strip():
                return n.text.strip()

        try:
            inp = self._get_visible_search_input()
            vmsg = inp.get_attribute("validationMessage")
            if vmsg:
                return vmsg.strip()
        except Exception:
            pass

        return ""