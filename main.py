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
    same_count = 0
    while same_count < 20:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_h = driver.execute_script("return document.body.scrollHeight;");
        
        if prev_h == scroll_h:
            same_count = same_count + 1

            # for event in events:
            #     driver.get(event["link"])
            #     top = driver.find_element(By.CSS_SELECTOR, ".x1ni5s2d")
            #     content = top.find_element(By.CSS_SELECTOR, ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x41vudc.x6prxxf.xvq8zen.xo1l8bm.xzsf02u")
            #     print(content.get_attribute("innerText"))
            #     time.sleep(1000)
        prev_h = scroll_h
        time.sleep(0.5)
    
    divs = driver.find_elements(By.CSS_SELECTOR, ".x1xmf6yo.x2fvf9.x1e56ztr.xdwrcjd.x1j9u4d2.xqyf9gi.xbx0bkf.xgkj6nh.xokokum.x1m0d6it.x12zdd2p.xxhiflr.x3th3hn")
    events = []
    print("Found", len(divs), "events")
    for div in divs:
        a = div.find_elements(By.CSS_SELECTOR, "a")
        event_name = ""

        try:
            parent = div.find_element(By.CSS_SELECTOR, ".x1i10hfl.xjbqb8w.x1ejq31n.x18oe1m7.x1sy0etr.xstzfhl.x972fbf.x10w94by.x1qhh985.x14e42zd.x9f619.x1ypdohk.xt0psk2.x3ct3a4.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xkrqix3.x1sur9pj.x1pd3egz")
            date = div.find_element(By.CSS_SELECTOR, ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1nxh6w3.x1sibtaa.x1s688f.xzsf02u")
            events.append({"title": parent.get_attribute("innerText"), "link": parent.get_attribute("href"), "date": date.get_attribute("innerText")})
        except:
            print("na")

        #child1 = parent.find_elements(By.TAG_NAME, "div")[1] 
        #ok = child1.find_element(By.CSS_SELECTOR, "div > div > span > span > span")
        #print(child1.get_attribute("innerText"))

        for anchor in a:
            tabindex = anchor.get_attribute('tabindex')
            if tabindex == "0":
                event_name = anchor.get_attribute('innerText')
except Exception as e:
        print(e)