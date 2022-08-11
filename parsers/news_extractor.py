import sys
sys.path.append('../')

from .document_extractor import DocumentExtractor
from .schemas.news import NewsArticle


# 3rd party libraries
from goose3 import Goose

class NewsExtractor(DocumentExtractor):

    def __init__(self, **kwargs):

        super(NewsExtractor, self).__init__(**kwargs)
        self.g = Goose()
        
    def process_page(self,
                     url,
                     page,
                     schema_org_check=True,
                     **kwargs):

        super().process_page(url,
                             page,
                             schema_org_check=schema_org_check,
                             **kwargs)

        goose_article = self.run_goose()
        
        self.article = NewsArticle(title=goose_article._title,
                                   full_text=goose_article._cleaned_text,
                                   url=goose_article._canonical_link,
                                   news_source=goose_article._domain,
                                   authors=goose_article._authors,
                                   publish_datetime_utc=str(goose_article._publish_datetime_utc),
                                   meta_description=goose_article._meta_description,
                                   meta_keywords=goose_article._meta_keywords,
                                   named_entities =None,
                                   top_image=goose_article._top_image,
                                   tweets=goose_article._tweets)

        
    def run_goose(self):
        """FIXME! briefly describe function

        :returns: 
        :rtype: 

        """

        # FIXME: Update schema for Article
        self.goose_article = self.g.extract(url=None, raw_html=self.curr_page)
        return self.goose_article

    def detect_events(self):
        pass

    def resolve_to_wikidata(self):
        pass

    def centrality(self):
        pass
