import csv
import json
import re
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path


# =========================
# PATH HELPER
# =========================
def get_full_path(file_path):
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / file_path


# =========================
# MAIN ENTRY
# =========================
def get_data(file_path, data_type=None):
    full_path = get_full_path(file_path)

    if not full_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {full_path}")

    if data_type:
        ext = data_type.lower().replace(".", "")
    else:
        ext = full_path.suffix.lower().replace(".", "")

    if ext == "csv":
        data = read_csv(full_path)

    elif ext == "json":
        data = read_json(full_path)

    elif ext in ["xlsx", "xls", "excel"]:
        data = read_excel(full_path)

    elif ext == "sql":
        data = read_sql_as_data(full_path)

    elif ext == "xml":
        data = read_xml(full_path)

    elif ext == "txt":
        data = read_txt(full_path)

    else:
        raise ValueError(f"Không hỗ trợ loại file: {ext}")

    return normalize_data(data)


def load_data(file_path):
    return get_data(file_path)


# =========================
# READ CSV
# =========================
def read_csv(full_path):
    with open(full_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# =========================
# READ JSON
# =========================
def read_json(full_path):
    with open(full_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and "tests" in data:
        return data["tests"]

    if isinstance(data, list):
        return data

    raise ValueError("File JSON phải là list hoặc object có key 'tests'")


# =========================
# READ EXCEL
# =========================
def read_excel(full_path):
    df = pd.read_excel(full_path)
    df = df.fillna("")
    return df.to_dict(orient="records")


# =========================
# READ XML
# =========================
def read_xml(full_path):
    """
    Đọc XML dạng:

    <searchData>
        <testcase>
            <search>tee</search>
            <expected>Có sản phẩm</expected>
        </testcase>
    </searchData>

    hoặc:

    <checkoutData>
        <testcase>
            <keyword>...</keyword>
            <name>...</name>
        </testcase>
    </checkoutData>
    """

    tree = ET.parse(full_path)
    root = tree.getroot()

    data = []

    for testcase in root:
        row = {}

        for child in testcase:
            key = child.tag
            value = child.text if child.text is not None else ""
            row[key] = value

        if row:
            data.append(row)

    return data


# =========================
# READ TXT
# =========================
def read_txt(full_path):
    data = []

    with open(full_path, mode="r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                data.append({"value": line})

    return data


# =========================
# READ SQL
# =========================
def read_sql_as_data(full_path):
    with open(full_path, mode="r", encoding="utf-8") as file:
        sql_content = file.read()

    columns_match = re.search(
        r"insert\s+into\s+\w+\s*\((.*?)\)",
        sql_content,
        re.IGNORECASE | re.DOTALL
    )

    if columns_match:
        columns = [
            col.strip().strip("`").strip('"').lower()
            for col in columns_match.group(1).split(",")
        ]
    else:
        columns = []

    values_match = re.search(
        r"values\s*(.*?);",
        sql_content,
        re.IGNORECASE | re.DOTALL
    )

    if not values_match:
        return []

    values_part = values_match.group(1)
    rows = re.findall(r"\((.*?)\)", values_part, re.DOTALL)

    data = []

    for row in rows:
        values = parse_sql_row(row)

        if columns and len(columns) == len(values):
            data.append(dict(zip(columns, values)))
        else:
            temp = {}
            for index, value in enumerate(values):
                temp[f"col_{index}"] = value
            data.append(temp)

    return data


def parse_sql_row(row):
    values = []
    current = ""
    in_quote = False
    i = 0

    while i < len(row):
        char = row[i]

        if char == "'":
            # xử lý chuỗi rỗng ''
            if in_quote and i + 1 < len(row) and row[i + 1] == "'":
                current += "'"
                i += 1
            else:
                in_quote = not in_quote

        elif char == "," and not in_quote:
            values.append(current.strip())
            current = ""

        else:
            current += char

        i += 1

    values.append(current.strip())

    return values


# =========================
# NORMALIZE DATA
# =========================
def normalize_data(data):
    if not isinstance(data, list):
        raise ValueError("Data phải là list")

    normalized = []

    for index, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"Dòng {index + 1} không phải dạng dict")

        clean_row = {}

        for key, value in row.items():
            clean_key = str(key).strip().lower()

            if pd.isna(value):
                clean_value = ""
            else:
                clean_value = str(value).strip()

            clean_row[clean_key] = clean_value

        if all(value == "" for value in clean_row.values()):
            continue

        normalized.append(clean_row)

    return normalized