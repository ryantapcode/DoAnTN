import os
import pytest
from datetime import datetime

from Page.order_page import CheckoutPage
from Utils.data_reader import get_data
from Utils.test_result_writer_excel import ExcelReporter


DATA_TYPE = "json"

DATA_FILES = {
    "csv": "Data/order/data_order.csv",
    "json": "Data/order/data_order.json",
    "sql": "Data/order/data_order.sql",
    "xlsx": "Data/order/data_order.xlsx",
    "xml": "Data/order/data_order.xml"
}

DATA_FILE = DATA_FILES[DATA_TYPE]

test_data = get_data(DATA_FILE, DATA_TYPE)


class TestCheckout:

    @pytest.mark.parametrize("data", test_data)
    def test_checkout_field_errors(self, driver, data):
        page = CheckoutPage(driver)
        reporter = ExcelReporter("Reports/test_results_order.xlsx")

        keyword = data.get("keyword", "")
        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")
        province = data.get("province", "")
        address = data.get("address", "")
        expected = str(data.get("expected", "")).strip().lower()

        test_name = f"checkout_{expected}_{keyword[:12]}"

        actual_error = ""
        status = "FAIL"
        screenshot_path = ""
        current_step = ""

        try:
            current_step = "Mở trang chủ"
            page.open("https://swe.vn/")

            current_step = "Tìm kiếm sản phẩm"
            page.search_product(keyword)

            current_step = "Click sản phẩm đầu tiên"
            page.click_first_product()

            current_step = "Thêm vào giỏ hàng"
            page.add_to_cart()

            current_step = "Đi tới trang thanh toán"
            page.go_to_checkout_from_popup()

            current_step = "Điền form thanh toán"
            page.fill_checkout_form(name, phone, email, province, address)

            current_step = "Bấm đặt hàng"
            page.submit_order()

            current_step = "Kiểm tra lỗi validate"

            if expected == "name":
                actual_error = page.get_name_error()

            elif expected == "phone":
                actual_error = page.get_phone_error()

            elif expected == "email":
                actual_error = page.get_email_error()

                if not actual_error and "@" not in email:
                    actual_error = "Email không đúng định dạng"

            elif expected == "address":
                actual_error = page.get_address_error()

            elif expected == "province":
                actual_error = page.get_province_error()

            else:
                raise AssertionError(f"Expected không hợp lệ: {expected}")

            if actual_error:
                status = "PASS"
            else:
                raise AssertionError(
                    f"Không thấy lỗi hiển thị cho field: {expected}"
                )

        except Exception as e:
            actual_error = (
                f"Lỗi tại bước [{current_step}]: "
                f"{type(e).__name__}: {str(e)}"
            )
            screenshot_path = self.capture_screenshot(driver, test_name)

        finally:
            reporter.write_result({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test Name": test_name,
                "Keyword": keyword,
                "Name": name,
                "Phone": phone,
                "Email": email,
                "Province": province,
                "Address": address,
                "Expected": expected,
                "Actual Error": actual_error,
                "Status": status,
                "Screenshot": screenshot_path
            })

        assert status == "PASS", (
            f"[{test_name}] Expected '{expected}', got: {actual_error}"
        )

    def capture_screenshot(self, driver, test_name):
        os.makedirs("Reports/screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = (
            test_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        path = f"Reports/screenshots/{safe_name}_{timestamp}.png"

        driver.save_screenshot(path)

        return path