import os
import re
import hashlib
from collections import defaultdict, Counter
from fuzzywuzzy import fuzz
import json
import logging
import boto3
from botocore.exceptions import ClientError

import random
import string

    
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# def create_bucket(bucket_name, region=None):
#     """Create an S3 bucket in a specified region

#     If a region is not specified, the bucket is created in the S3 default
#     region (us-east-1).

#     :param bucket_name: Bucket to create
#     :param region: String region to create bucket in, e.g., 'us-west-2'
#     :return: True if bucket created, else False
#     """
#     os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'

#     # Create bucket
#     try:
#         if region is None:
#             s3_client = boto3.client('s3')
#             s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
#                 'LocationConstraint': AWS_DEFAULT_REGION})
#         else:
#             s3_client = boto3.client('s3')
#             location = {'LocationConstraint': region}
#             s3_client.create_bucket(Bucket=bucket_name,
#                                     CreateBucketConfiguration=location)
#     except ClientError as e:
#         print(e)
#         return False

#     return True

# def upload_json(bucket_name, filename, data):


#     return True

# def upload_file(bucket_name, filename):

#     s3 = boto3.client('s3')
#     s3.upload_file(filename, bucket_name, filename)

#     return True

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'
    
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': AWS_DEFAULT_REGION})
        else:
            s3_client = boto3.client('s3')
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False

    return True

def upload_json(bucket_name, filename, data):

    s3 = boto3.resource('s3')
    s3object = s3.Bucket(bucket_name).Object(filename)
    s3object.put(Body=bytes(json.dumps(data).encode('UTF-8')))

    return True
    
def upload_file(bucket_name, filename):

    s3 = boto3.client('s3')
    s3.upload_file(filename, bucket_name, filename)

    return True

def lca(_what, _where):

    what = _what.split('/')
    where = _where.split('/')

    temp = min(len(what), len(where))

    for idx in range(temp):
        what_tag = what[idx]
        where_tag = where[idx]

        if what_tag != where_tag:
            return idx

    return temp

def get_right_tag(xpath):
    path = xpath.split('/')[1:]

    answer = ""
    for tag in path[::-1]:
        tag, index = get_tag_and_index(tag)
        if not len(index):
            answer = tag
            break

    if answer not in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
        return get_tag_and_index(path[-1])[0]

    return answer

def fuzz_match(stringA, stringB):


    # partial_score = fuzz.partial_ratio(stringA, stringB)
    sort_score = fuzz.token_sort_ratio(stringA, stringB)
    set_score = fuzz.token_set_ratio(stringA, stringB)

    token_diff = abs(len(stringA.split()) - len(stringB.split()))

    # random number that's small
    # if token_diff >= 3:
    #     return 0


    return max([partial_score,
                sort_score,
                set_score
    ])

def fuzz_match_token(stringA, stringB):

    # B IS THE PRED
    # A is the true

    # pred is a unigram, never the answer
    if len(stringB.split()) <= 1:
        return 0

    token_diff = abs(len(stringA.split()) - len(stringB.split()))
    
    sort_score = fuzz.token_sort_ratio(stringA, stringB)
    # set_score = fuzz.token_set_ratio(stringA, stringB)
    
    return max([sort_score, 0, 0])

def get_hash(text_string):
    """Given a string compute a unique hash using MD5

    :param str text_string: String
    :returns: string object of double length
    :rtype: str

    """
    hash_object = hashlib.md5(text_string.encode())
    return hash_object.hexdigest()

def get_hash_num(text_string):
    """Given a string compute a unique hash using MD5

    :param str text_string: String
    :returns: string object of double length
    :rtype: str

    """
    hash_object = hashlib.md5(text_string.encode())
    return int(hash_object.hexdigest(), 16)

def get_tag_and_index(xpath_tag):

    """Given an xpath tag filter out tag and index

    >>> get_tag_and_index('div[0]')
    div, 0

    :param str xpath_tag: the xpath piece
    :returns: tuple of tag and index
    :rtype: tuple (str, str)
    """

    if not len(xpath_tag):
        return '', ''

    tag = re.findall(r'\w+', xpath_tag)[0]
    index = re.findall(r"\[(\d+)\]", xpath_tag)

    if index:
        index = index[0]
    else:
        index = ''

    return tag, index


def label_creator(row, what, where):

    # -1 if unknown
    if not len(what):
        return -1

    what_max = 0
    where_max = 0
    for _, text in row['texts']:

        what_true = fuzz_match(text, what)
        where_true = fuzz_match(text, where)

        if what_max < what_true:
            what_max = what_true

        if where_max < where_true:
            where_max = where_true

    if what_max > 85 and where_max > 85:
        return 1

    return 0

def title_features(row):

    headers = {'h1': 1, 'h2': 0.5, 'h3': 0.3, 'h4': 0.1}

    header_dist = []

    for i, (tag, text) in enumerate(row['texts']):
        if tag in headers:
            header_dist.append(tag)

    header_score = 0
    if len(header_dist):
        header_score = sum([headers[key] for key in header_dist])/(len(header_dist))
    return {
        'score': header_score,
        'header_dist': Counter(header_dist)
    }

def when_features(row, nlp):
    """Given a group it tells me if that row has a score of being an
    address

    :param row:
    :param nlp:
    :returns:
    :rtype:

    """


    annotations = [valid(text, nlp) for _, text in row['texts']]
    scores = [x['score'] for x in annotations]
    score = sum(scores)

    return score, [text for idx, (_,text) in enumerate(row['texts']) if scores[idx] > 0]





def valid(text, nlp):
    '''
    This a text sentence from the webpage.
    '''
    # tokenize
    doc = nlp(text)

    def is_state(state):
        # easily gazetted using state names and state codes.
        american_cities = {'wa', 'wi', 'ca', 'ny', 'new york', 'washington', 'california'}
        if state.lower() in american_cities:
            return 1
        return 0

    def is_zip_code(zip_code):
        '''
        Is it an US zip code
        '''
        if len(zip_code) == 5 and zip_code.isdigit():
            return 1
        return 0

    def st_heuristics(_token):

        token = _token.lower()

        if 'st' == token or 'ave' == token or 'av' == token or 'avenue' == token:
            return 1

        return 0

    full_address = False

    punct = {","}

    zip_score = sum([is_zip_code(x.text.strip()) for x in doc if x.text not in punct])

    # there is a state in this sentence
    state_score = sum([is_state(x.text.strip()) for x in doc if x.text not in punct])

    # it exists
    temp = [st_heuristics(x.text.strip()) for x in doc if x.text not in punct]
    street_score = max(temp) if len(temp) else 0

    # this is the full sentence
    if state_score > 0 and zip_score >0 and len(doc) > 5:
        full_address = True

    return {"zip_score": zip_score,
            "state_score": state_score,
            "score": zip_score + state_score + street_score,
           "full_address": full_address}


