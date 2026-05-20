import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():

    chrome_options = Options()

    # =========================
    # CI / HEADLESS MODE
    # =========================
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")

    # =========================
    # ANTI DETECT
    # =========================
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # =========================
    # PERFORMANCE / STABILITY
    # =========================
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-background-timer-throttling")

    # =========================
    # PAGE LOAD STRATEGY
    # =========================
    chrome_options.page_load_strategy = "eager"

    # =========================
    # USER AGENT
    # =========================
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )

    # =========================
    # CREATE DRIVER
    # =========================
    drv = webdriver.Chrome(options=chrome_options)

    # =========================
    # TIMEOUT
    # =========================
    drv.set_page_load_timeout(60)
    drv.implicitly_wait(10)

    yield drv

    drv.quit()