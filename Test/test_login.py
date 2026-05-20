import os
from datetime import datetime
import pytest
from Page.login_page import LoginPage
from Utils.data_reader import get_data

DATA_TYPE = "sql"

DATA_FILES = {
    "csv": "Data/login/data_login.csv",
    "json": "Data/login/data_login.json",
    "sql": "Data/login/data_login.sql",
    "xlsx": "Data/login/data_login.xlsx",
    "xml": "Data/login/data_login.xml"
}
DATA_FILE = DATA_FILES[DATA_TYPE]
test_data = get_data(DATA_FILE, DATA_TYPE)
all_results = []


class TestLogin:

    @pytest.mark.parametrize("row", test_data)
    def test_login(self, driver, row):
        login_page = LoginPage(driver)
        email = row.get("email", "")
        password = row.get("password", "")
        expected_result = row.get("expected", "")
        test_name = f"test_login_{email if email else 'no_email'}"

        actual_result = ""
        status = "FAIL"

        # Mở trang login
        login_page.open("https://swe.vn/")
        login_page.login(email, password)

        try:
            # Lấy error message
            actual_result = login_page.get_error_message()
            if not actual_result:  # Nếu không có lỗi => login thành công
                actual_result = "Success"

            if actual_result.strip().lower() == expected_result.strip().lower():
                status = "PASS"
            else:
                raise AssertionError("Actual result doesn't match expected result.")

        except AssertionError as e:
            if not actual_result:
                actual_result = str(e)

        print(f"\n Email: {email}")
        print(f" Expected: {expected_result}")
        print(f" Actual: {actual_result}")

        all_results.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Username": email,
            "Password": password,
            "Expected": expected_result,
            "Actual": actual_result,
            "Status": status
        })

        assert status == "PASS", f"[{test_name}] Expected: {expected_result}, but got: {actual_result}"


def teardown_module(module):
    from Utils.test_result_writer_excel import write_test_results_excel
    write_test_results_excel(
        all_results,
        filename="test_results_login.xlsx",
        sheet_name="Test Results Login"
    )
