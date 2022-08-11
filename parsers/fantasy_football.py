import sys
sys.path.append('../')
import pandas as pd
from .document_extractor import DocumentExtractor

class FantasyPremierLeagueStats(DocumentExtractor):

    def __init__(self, **kwargs):

        super(FantasyPremierLeagueStats, self).__init__(**kwargs)

    def process_page(self,
                     url,
                     page,
                     schema_org_check=True,
                     **kwargs):

        super().process_page(url,
                             page,
                             schema_org_check=schema_org_check,
                             **kwargs)


        
        # print(self.tree.xpath('//*[@id="data-table"]'))
        nodes = self.tree.xpath('//table//tr')
        self.data = []
        for node in nodes:
            tmp = [i.text.strip() for i in node.xpath('.//child::td') if len(i.text.strip())]
            if not len(tmp):
                continue

            self.data.append(tmp)

        print(pd.DataFrame(self.data))
