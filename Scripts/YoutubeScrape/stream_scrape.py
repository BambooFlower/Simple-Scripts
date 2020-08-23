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

driver = webdriver.Firefox()

class LiveYouTube():
    def __init__(self,url,filename = 'test'):
        self.url = url
        self.filename = filename
    def start(self):
        # Video URL
        url = self.url
        
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
        
    def r(self):
        from importlib import reload  
        import traceback
        import Processing as p
    
        try:
            # Do some things.
            time.sleep(1)
            p = reload(p)
            p.test(driver,self.filename)
        except Exception: 
            traceback.print_exc()
        
        

#Capture = LiveYouTube('https://www.youtube.com/watch?v=fTTKboeQNTI','whatever.txt')
#Capture.r()
