import os
# from lxml import etree
# from lxml.etree import Comment

# from crawler.browser_automation import make_driver
# import crawler.COLORS as C

import json
import time
# from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from .base import BaseHTMLRenderer

# os.environ['MOZ_HEADLESS'] = '1'
# TODO : Make this a spacific instance of Renderer: for Google scholar
class GoogleScholarHTMLRenderer(BaseHTMLRenderer):

    def __init__(self, **kwargs):
        super(GoogleScholarHTMLRenderer, self).__init__(**kwargs)        

    def get_main_page(self, url, fname, override=False):
        
        if os.path.exists(fname) and not override:
            return

        temp = fname.split('/')
        base_dir = "/".join(temp[:-1])        
        self.fname = fname
        
        try:
            self._url = url #: Url of page
            self._driver.get(self._url)
            page = self._driver.page_source
            self.html = page

            div_elements = self._driver.find_elements("xpath", "//span[@class='gs_lbl']")
            for div_element in div_elements:
                if div_element.text.strip() == 'SHOW MORE':
                    print('Clicking show more')
                    div_element.click()
            time.sleep(3)
            
            # print(C.RED, self._driver.title, C.RESET)
            self.page_title =  self._driver.title
            
            # print("page saved")
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
        
        with open(fname, 'w') as f:
            json.dump(save_file, f)

