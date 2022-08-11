import sys
sys.path.append('../')
import pandas as pd
from .document_extractor import DocumentExtractor

class GoogleScholar(DocumentExtractor):

    def __init__(self, **kwargs):

        super(GoogleScholar, self).__init__(**kwargs)

    def process_page(self,
                     url,
                     page,
                     schema_org_check=True,
                     **kwargs):

        super().process_page(url,
                             page,
                             schema_org_check=schema_org_check,
                             **kwargs)


        data = []
        papers = self.tree.xpath("//*[@class='gsc_a_t']/a")
        years = self.tree.xpath("//*[@class='gsc_a_h gsc_a_hc gs_ibl']")
        for idx, url in enumerate(papers):
            if url.text:                
                data.append({'title': url.text, 'year':years[idx].text})
    
        self.papers = pd.DataFrame(data)
        
