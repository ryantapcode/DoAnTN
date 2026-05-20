import os
import time
import pytest

from Page.addcart_page import AddCartPage
from Utils.data_reader import get_data
from Utils.test_result_writer_excel import log_result


BASE_URL = "https://swe.vn/"

DATA_TYPE = "xml"
DATA_FILES = {
    "csv": "Data/addcart/data_addcart.csv",
    "json": "Data/addcart/data_addcart.json",
    "sql": "Data/addcart/data_addcart.sql",
    "xlsx": "Data/addcart/data_addcart.xlsx",
    "xml": "Data/addcart/data_addcart.xml"
}

DATA_FILE = DATA_FILES[DATA_TYPE]


test_data = get_data(DATA_FILE, DATA_TYPE)


@pytest.mark.parametrize("row", test_data)
def test_add_to_cart(driver, row):

    page = AddCartPage(driver)

    keyword = row.get("keyword", "")
    quantity = int(row.get("quantity", 1))

    try:
        print(f"\nĐang test sản phẩm: '{keyword}' với số lượng {quantity}")
        print(f"Đang đọc data từ file: {DATA_FILE}")

        page.open(BASE_URL)

        page.search_product(keyword)

        page.open_first_product()

        page.increase_quantity(quantity)

        print(f"Đã click dấu '+' {quantity} lần.")

        page.add_to_cart()

        message = page.get_toast_message()

        assert any(
            w in message.lower()
            for w in ["giỏ hàng", "thành công", "added", "success"]
        ), f"Không thấy thông báo thêm vào giỏ hàng. Nhận được: {message}"

        page.view_cart()

        time.sleep(2)

        cart_qty = page.get_cart_quantity()

        assert cart_qty == quantity, \
            f"Số lượng trong giỏ hàng ({cart_qty}) không khớp với ({quantity})"

        log_result(
            keyword,
            quantity,
            "PASS",
            "Thêm sản phẩm vào giỏ hàng thành công"
        )

    except AssertionError as e:
        handle_exception(
            driver,
            keyword,
            quantity,
            "FAIL",
            str(e)
        )
        raise

    except Exception as e:
        handle_exception(
            driver,
            keyword,
            quantity,
            "ERROR",
            str(e)
        )
        raise


def handle_exception(driver, keyword, quantity, status, message):

    os.makedirs("Reports/screenshots", exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    safe_keyword = (
        str(keyword)
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    screenshot_path = (
        f"Reports/screenshots/"
        f"{safe_keyword}_{timestamp}.png"
    )

    driver.save_screenshot(screenshot_path)

    log_result(
        keyword,
        quantity,
        status,
        message,
        screenshot_path
    )