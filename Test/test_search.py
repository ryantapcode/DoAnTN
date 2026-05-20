import os
import pytest
from datetime import datetime

from Page.search_page import SearchPage
from Utils.data_reader import read_json

BASE_URL = "https://swe.vn/"
test_data = read_json("Data/data_search.json")


class TestSearch:
    @pytest.mark.parametrize("data", test_data)
    def test_search_product(self, driver, data):
        page = SearchPage(driver)

        keyword = data.get("search") or data.get("keyword") or ""
        expected = data.get("expected", "")
        test_name = f"search_{keyword if keyword else 'empty'}"

        try:
            page.open(BASE_URL)
            page.search_product(keyword)

            actual = page.get_search_message()
            print(f"Từ khóa: '{keyword}' | Kết quả: {actual}")

            assert expected.lower() in actual.lower(), (
                f"[{test_name}] Expected '{expected}', got '{actual}'"
            )

        except Exception as e:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_kw = keyword.replace(" ", "_") if keyword else "empty"
            screenshot_path = f"report/screenshots/{safe_kw}_{timestamp}.png"

            os.makedirs("report/screenshots", exist_ok=True)
            driver.save_screenshot(screenshot_path)

            print(f"FAIL: {test_name}")
            print(f"Screenshot: {screenshot_path}")
            raise