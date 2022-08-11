from .document_extractor import DocumentExtractor
from .dom_node import Text_Node

def item_generator(json_input, lookup_key, value):
    """Iterate through nested json looking for key= look_up key and value
    == value

    :param json_input: 
    :param lookup_key: 
    :param value: 
    :returns: 
    :rtype:

    """
    
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key and v == value:
                yield json_input
            else:
                yield from item_generator(v, lookup_key, value)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key, value)
            
class FoodNetworkParser(DocumentExtractor):

    def __init__(self, url, page, meta_data, nlp):        
        super().__init__(url, page, meta_data, nlp)


    def get_query_from_page(self):

        if not self.title_node:
            return

        return self.title_node.text.split(':')[0]

    def get_answers(self):

        temp = {'query': self.get_query_from_page(), 'answers': []}

        for gallery in item_generator(self.schema_org['json-ld'],'@type','ImageGallery'):
            temp['answers'] += gallery['Image']
            
        # temp['answers'] = [x['name'] for x in item_generator(self.schema_org['json-ld'],
        #                                                      '@type',
        #                                                      'ImageObject')]

        return temp
