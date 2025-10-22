from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.set_capability(
                        "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
                    )
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/events/?date_filter_option=TODAY&discover_tab=CUSTOM&end_date=2025-10-21T22%3A00%3A00.000Z&location_id=104005829635705&start_date=2025-10-20T22%3A00%3A00.000Z")

prev_h = 0
try:
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_h = driver.execute_script("return document.body.scrollHeight;");
        if prev_h != scroll_h:
            log_entries = driver.get_log("performance")

            for log in log_entries:
                body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
                print(log)

            divs = driver.find_elements(By.CSS_SELECTOR, ".x1vsv7so")
            print(len(divs), "events")
            for div in divs:
                a = div.find_elements(By.CSS_SELECTOR, "a")
                event_name = ""
                for anchor in a:
                    tabindex = anchor.get_attribute('tabindex')
                    if tabindex == "0":
                        event_name = anchor.get_attribute('innerText')

        prev_h = scroll_h
        time.sleep(3)
except Exception as e:
        print(e)
