import pytest
import os
from datetime import datetime

from Page.addcart2_page import CartPage
from Utils.data_reader import get_data
from Utils.test_result_writer_excel import ExcelReporter


DATA_TYPE = "sql"

DATA_FILES = {
    "csv": "Data/addcart/data_addcart.csv",
    "json": "Data/addcart/data_addcart.json",
    "sql": "Data/addcart/data_addcart.sql",
    "xlsx": "Data/addcart/data_addcart.xlsx",
    "xml": "Data/addcart/data_addcart.xml"
}

DATA_FILE = DATA_FILES[DATA_TYPE]

test_data = get_data(DATA_FILE, DATA_TYPE)


@pytest.mark.usefixtures("driver")
class TestCartSingle:

    @pytest.mark.parametrize("row", test_data)
    def test_add_reduce_remove_cart(self, driver, row):

        keyword = row.get("keyword", "")
        quantity = int(row.get("quantity", 1))

        # Web không cho số lượng giảm xuống 0
        expected_qty = max(quantity - 1, 1)

        page = CartPage(driver)
        reporter = ExcelReporter("Reports/test_results_cart.xlsx")

        status = "FAIL"
        error_msg = ""
        screenshot_path = ""

        try:
            page.open("https://swe.vn/")

            page.search_product(keyword)
            page.open_first_product()

            page.increase_quantity(quantity)

            page.add_to_cart()
            page.view_cart()

            page.decrease_quantity(1)

            qty = page.get_cart_quantity()

            assert qty == expected_qty, \
                f"Số lượng mong đợi = {expected_qty}, thực tế = {qty}"

            page.remove_product()

            assert page.is_cart_empty(), \
                "Giỏ hàng chưa trống sau khi xóa sản phẩm!"

            status = "PASS"

        except AssertionError as e:
            error_msg = str(e)
            screenshot_path = self.capture_screenshot(driver, "assert_fail")

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            screenshot_path = self.capture_screenshot(driver, "exception")

        finally:
            reporter.write_result({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test Name": "Thêm_Giảm_Xóa_Sản_Phẩm",
                "Keyword": keyword,
                "Expected": f"Số lượng sau khi giảm = {expected_qty}",
                "Actual": error_msg if error_msg else "Hoàn thành đúng",
                "Status": status,
                "Screenshot": screenshot_path
            })

            assert status == "PASS", f"Test không đạt: {error_msg}"

    def capture_screenshot(self, driver, prefix="screenshot"):
        os.makedirs("Reports/screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = f"Reports/screenshots/{prefix}_{timestamp}.png"

        driver.save_screenshot(path)

        return path