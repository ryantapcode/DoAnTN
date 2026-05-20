from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage:
    def __init__(self, driver, timeout=12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get(url)
            self.driver.maximize_window()
            time.sleep(2)

        except Exception:
            self.driver.execute_script("window.stop();")
            self.driver.maximize_window()
            time.sleep(2)

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    def input_text(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)
        return el


class AddCartPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "#inputSearchAuto")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-6.pro-loop")
    ADD_TO_CART = (By.CSS_SELECTOR, "#add-to-cart")
    TOAST_MESSAGE = (By.CSS_SELECTOR, "div.header_dropdown_content.site_cart p.titlebox")
    INCREASE_BTN = (By.CSS_SELECTOR, "input[value='+']")
    VIEW_CART_BTN = (By.CSS_SELECTOR, ".linktocart.button.dark")
    CART_QTY_INPUT = (By.CSS_SELECTOR, "input[name='updates[]'].line-item-qty")

    def search_product(self, keyword):
        el = self.input_text(self.SEARCH_INPUT, keyword)
        el.send_keys(Keys.ENTER)
        time.sleep(2)

    def open_first_product(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.SEARCH_RESULTS))
        if not items:
            raise AssertionError("Không tìm thấy sản phẩm nào sau khi tìm kiếm!")
        items[0].click()

    def increase_quantity(self, quantity):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.INCREASE_BTN))
            for i in range(int(quantity) - 1):  # click (quantity - 1) lần
                btn.click()
                time.sleep(0.6)  # delay nhỏ giữa mỗi click để web xử lý
        except Exception as e:
            raise AssertionError(f"Lỗi khi tăng số lượng: {e}")

    def add_to_cart(self):
        self.click(self.ADD_TO_CART)

    def get_toast_message(self, timeout=8):
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.TOAST_MESSAGE)
            )
            return el.text.strip()
        except:
            return ""

    def view_cart(self):
        self.click(self.VIEW_CART_BTN)

    def get_cart_quantity(self):
        try:
            qty_input = self.wait.until(
                EC.visibility_of_element_located(self.CART_QTY_INPUT)
            )
            return int(qty_input.get_attribute("value"))
        except:
            raise AssertionError("Không tìm thấy ô nhập số lượng trong giỏ hàng!")
