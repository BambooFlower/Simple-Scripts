# -*- coding: utf-8 -*-
"""
Script to catch new comments event from a live stream

What I want it to do...

1) Capture new comments... and store in a database
2) Get number of views every 5 seconds... and store in a database
"""

from seleniumwire import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import Processing as p

driver = webdriver.Firefox()

# Video URL
url = 'https://www.youtube.com/watch?v=ulBbBA5Ndu8'

driver.get(url)

# Switch to iframe
driver.switch_to.frame(driver.find_element_by_id('chatframe'))


stage = 0
while 1:
    try:
        if stage == 0:
            # Switch to live chat option
            driver.find_element_by_id('label-text').click()
            stage = 1
        if stage == 1:
            tmp = driver.find_element_by_tag_name('paper-listbox')
            stage = 2
        if stage == 2:
            tmp.find_elements_by_tag_name('a')[1].click()
            print("good")
            break
    except:
        print("bad")
        time.sleep(1)

def r():
    from importlib import reload  
    import traceback
    import Processing as p

    try:
        # Do some things.
        time.sleep(1)
        p = reload(p)
        p.test(driver)
    except Exception: 
        traceback.print_exc()


r()