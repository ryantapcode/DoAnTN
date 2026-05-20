import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Page.addcart_page import AddCartPage


class CartPage(AddCartPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

        self.DECREASE_BTN = (By.CSS_SELECTOR, "button.qtyminus.qty-btn")
        self.REMOVE_PRODUCT_BTN = (By.CSS_SELECTOR, "tbody tr:first-child td:nth-child(3) a img")
        self.EMPTY_CART_MSG = (By.CSS_SELECTOR, ".expanded_message")

        # ô số lượng trong giỏ hàng
        self.CART_QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name='updates[]']")

    def decrease_quantity(self, times=1):
        try:
            for _ in range(times):
                btn = self.wait.until(EC.element_to_be_clickable(self.DECREASE_BTN))
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
        except Exception as e:
            raise AssertionError(f"Lỗi khi giảm số lượng sản phẩm: {e}")

    def get_cart_quantity(self):
        try:
            qty_input = self.wait.until(
                EC.presence_of_element_located(self.CART_QUANTITY_INPUT)
            )

            value = qty_input.get_attribute("value")

            return int(value)

        except Exception as e:
            raise AssertionError(f"Lỗi khi lấy số lượng trong giỏ hàng: {e}")

    def remove_product(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.REMOVE_PRODUCT_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)
        except Exception as e:
            raise AssertionError(f"Lỗi khi xóa sản phẩm: {e}")

    def is_cart_empty(self):
        try:
            msg = self.wait.until(
                EC.visibility_of_element_located(self.EMPTY_CART_MSG)
            )
            return msg.is_displayed()
        except:
            return False