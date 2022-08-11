from . import utils

def get_all_paths_for_a_node(xpath):
    '''
    Note this is not combninatorial like Percy:
    In between Percy and level order


    _...._._...

    Make sure each and everyone of them is turned on and off
    |...._._...
    _....|._...
    _...._.|...

    Then make sure they're turned off in a <left -> right manner> (Percy does 2^n) ways
    |....|._...
    |....|.|...
    '''

    # Get each part of the XPATH
    path = [part for part in xpath.split('/')]


    # the orignal path is always a candidate
    potential_groups = [xpath]


    # GIVES US:
    # LEVEL ORDER SEARCH for all nodes; not just openers
    for i, node in enumerate(path):

        tag = node
        if len(utils.get_tag_and_index(node)[1]):            
            tag = utils.get_tag_and_index(node)[0]
            temp = path[:]
            temp[i] = tag
            new_path = "/".join(temp[:i+1])
            if len(new_path.strip()):
                potential_groups.append(new_path)

        # I don't want to kill that tag
        # If that was possible I've already done it and added it to the block
        temp = path[:]
        potential_groups.append("/".join(temp[:i+1]))


    # Get all the spots which can be turned on and off
    indices = {idx: utils.get_tag_and_index(part)[0]
               for idx, part in enumerate(path) if len(utils.get_tag_and_index(part)[1])}
        
    if not len(indices):
        return potential_groups

    # go through each on an off guy
    # This is the first part

    # _...._._...

    # GIVES US:

    # |...._._...
    # _....|._...
    # _...._.|...

    for i, tag in indices.items():
        temp = path[:]
        temp[i] = tag # turn on
        new_path = "/".join(temp)
        if len(new_path.strip()):
            potential_groups.append(new_path)
            
    return potential_groups

def level_order_paths_for_a_node(node):

    path = [part for part in node.xpath.split('/')][1:]

    # get all indices which have a branch
    indices = {idx: utils.get_tag_and_index(part)[0]
               for idx, part in enumerate(path) if len(utils.get_tag_and_index(part)[1])}

    # Always include the full path.
    potential_groups = [node.xpath]

    # construct a new path:
    condensed_path = [utils.get_tag_and_index(path[idx])[0] for idx,tag in indices.items()]

    for i in range(len(condensed_path)):
        temp = condensed_path[:i+1]
        potential_groups.append("/".join(temp))

    return potential_groups


def unshortened_level_order(node):

    path = node.xpath.split('/')[1:]
    tags = [utils.get_tag_and_index(part)[0] for part in path]

    potential_groups = [node.xpath]

    for i in range(1, len(tags)+1):
        potential_groups.append("/".join(tags[:i]))

    return potential_groups
