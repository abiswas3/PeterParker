import os
from lxml import etree
from lxml.etree import Comment

from crawler.browser_automation import make_driver
import crawler.COLORS as C

import json
import time
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# os.environ['MOZ_HEADLESS'] = '1'
class BaseHTMLRenderer(object):


    def get_main_page(self, url, fname, override=False):

        
        if os.path.exists(fname) and not override:
            return

        self._driver = make_driver() #:Selenium webdriver
        self._driver.set_page_load_timeout(500)
        
        temp = fname.split('/')
        base_dir = "/".join(temp[:-1])        
        self.fname = fname
        
        try:
            self._url = url #: Url of page
            self._driver.get(self._url)
            page = self._driver.page_source
            self.html = page
            # print(C.RED, self._driver.title, C.RESET)
            self.page_title =  self._driver.title
            self._driver.quit()
            ret_code= 0

        except Exception as e:
            print('Could not load webpage in browser session')
            print(e)
            self._driver.quit()
            ret_code = -1


        if ret_code >= 0:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

            save_file = {"url": url,
                         "page_title": self.page_title,
                         "page": self.html
                         }
            print("Saving")
            with open(fname, 'w') as f:
                json.dump(save_file, f)

    def quit(self):
        self._driver.quit()
