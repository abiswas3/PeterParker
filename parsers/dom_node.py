from . import utils

class Text_Node(object):
    
    def __init__(self, text_node, parent, path_func):
        """FIXME! briefly describe function

        :param text_node:
        :param parent:
        :param path_func:
        :returns:
        :rtype:

        """

        self.valid = False
        if not text_node.is_text:
            return

        self.xpath = path_func(parent)

        path = self.xpath
        if 'script' in path or 'style' in path:
            return

        # Get all text for this block
        self.text = self.clean_text_node(" ".join(text.strip() for text in parent.itertext()))

        # TODO: maybe look at a different tokenizer
        self.tokens = [token for token in self.text.split()]
        
        if ('{' in self.text and '}' in self.text) or ('<' in self.text and '>' in self.text):
            return
        
        if not len(self.clean_text_node(self.text)):
            return

        self.node = parent
        self.text_node = text_node.strip()
        if not len(self.text_node):
            return
        
        self.valid = True
        self.is_title = self.node.tag == 'title'

        # THIS IS TRICKY often: cos we have a lot of redundant tags
        # We will revisit this later
        self.tag = self.node.tag
        # self.tag = utils.get_right_tag(self.xpath)



    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.xpath == other.xpath
            )

    def __repr__(self):
        return self.text

    def __hash__(self):
        return utils.get_hash_num(self.xpath)

    def clean_text_node(self, _text):

        if not _text:
            return ""

        text = " ".join(tok.strip() for tok in _text.strip().split())

        return text.strip()
