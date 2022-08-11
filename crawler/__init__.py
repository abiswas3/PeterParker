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
# TODO : Make this a spacific instance of Renderer: for Google scholar
class HomePageHTMLRenderer(object):

    def __init__(self, url, fname, override=False):
        """Accepts the main url of a newsPage and crawls subsequent pages.

        :param str url: The homepageURL of what we wish to parse
        """
        if os.path.exists(fname) and not override:
            return

        self.fname = fname
        temp = fname.split('/')
        base_dir = "/".join(temp[:-1])

        self._url = url #: Url of page
        self._driver = make_driver() #:Selenium webdriver
        # # Allow driver 50ms for page to load or else timeout
        self._driver.set_page_load_timeout(500)

        ret_code = self.get_main_page()

        if ret_code >= 0:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

            save_file = {"url": url,
                         "page_title": self.page_title,
                         "page": self.html
            }

            with open(fname, 'w') as f:
                json.dump(save_file, f)

    def get_main_page(self):

        try:
            self._driver.get(self._url)


            
            div_elements = self._driver.find_elements_by_xpath("//span[@class='gs_lbl']")
            for div_element in div_elements:
                if div_element.text.strip() == 'SHOW MORE':
                    print('Clicking show more')
                    div_element.click()
            time.sleep(3)

            # SCROLL_PAUSE_TIME = 0.5
            # # Get scroll height
            # last_height = self._driver.execute_script("return document.body.scrollHeight")
            # while True:
            #     # Scroll down to bottom
            #     self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #     # Wait to load page
            #     time.sleep(SCROLL_PAUSE_TIME)

            #     # Calculate new scroll height and compare with last scroll height
            #     new_height = self._driver.execute_script("return document.body.scrollHeight")
            #     if new_height == last_height:
            #         break

            #     last_height = new_height


            page = self._driver.page_source
            self.html = page
            # print(C.RED, self._driver.title, C.RESET)
            self.page_title =  self._driver.title
            self._driver.quit()
            # print("page saved")
            return 0

        except Exception as e:
            print('Could not load webpage in browser session')
            print(e)
            self._driver.quit()
            return -1
