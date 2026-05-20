import pandas as pd
from pathlib import Path


class ExcelReporter:
    def __init__(self, file_path):
        base_dir = Path(__file__).resolve().parent.parent
        self.file_path = base_dir / file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def write_result(self, result):
        new_df = pd.DataFrame([result])

        if self.file_path.exists():
            old_df = pd.read_excel(self.file_path)
            df = pd.concat([old_df, new_df], ignore_index=True)
        else:
            df = new_df

        df.to_excel(self.file_path, index=False)


def write_test_results_excel(results, filename="test_results.xlsx", sheet_name="Test Results"):
    base_dir = Path(__file__).resolve().parent.parent
    report_dir = base_dir / "Reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    file_path = report_dir / filename

    df = pd.DataFrame(results)
    df.to_excel(file_path, index=False, sheet_name=sheet_name)

    print(f"Đã ghi kết quả test vào file: {file_path}")

def log_result(keyword, quantity, status, message, screenshot_path=""):
    reporter = ExcelReporter("Reports/test_results_addcart.xlsx")

    reporter.write_result({
        "Keyword": keyword,
        "Quantity": quantity,
        "Status": status,
        "Message": message,
        "Screenshot": screenshot_path
    })