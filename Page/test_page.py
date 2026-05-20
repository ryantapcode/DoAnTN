import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AddToCartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # ===== LOCATORS =====
        self.search_icon = (By.CSS_SELECTOR, ".search.font-oswald.lang")
        self.search_input = (By.CSS_SELECTOR, "#inputSearchAuto")
        self.product_link = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-6.pro-loop")
        self.add_button = (By.CSS_SELECTOR, "#add-to-cart")
        self.view_cart_btn = (By.CSS_SELECTOR, ".lang.linktocart.button.dark")
        self.cart_page_heading = (By.CSS_SELECTOR, ".heading-cart")

    def open_homepage(self, url="https://hades.vn"):
        self.driver.get(url)
        self.driver.maximize_window()

    def search_product(self, keyword):
        # Nhấn vào biểu tượng tìm kiếm (đảm bảo hiển thị)
        icon = self.wait.until(EC.element_to_be_clickable(self.search_icon))
        self.driver.execute_script("arguments[0].click();", icon)
        time.sleep(1)

        # Chờ ô tìm kiếm xuất hiện và có thể nhập
        box = self.wait.until(EC.presence_of_element_located(self.search_input))

        # Đảm bảo phần tử hiển thị và focus
        self.driver.execute_script("arguments[0].scrollIntoView(true);", box)
        self.driver.execute_script("arguments[0].focus();", box)

        # Xóa & nhập từ khóa
        try:
            box.clear()
        except:
            # nếu chưa clear được thì gửi phím BACKSPACE để xóa
            box.send_keys("\b" * 20)

        box.send_keys(keyword if isinstance(keyword, str) else keyword[0])
        box.submit()
        time.sleep(2)

    def open_first_product(self):
        # Nhấn vào sản phẩm đầu tiên trong danh sách
        self.wait.until(EC.element_to_be_clickable(self.product_link)).click()

    def add_to_cart(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.add_button))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

    def view_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.view_cart_btn)).click()

    def is_cart_page_displayed(self):
        try:
            heading = self.wait.until(EC.presence_of_element_located(self.cart_page_heading))
            return "giỏ hàng" in heading.text.lower() or "cart" in heading.text.lower()
        except:
            return False
