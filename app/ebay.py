import os
import datetime
import json
from requests import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from pprint import pprint

# def get_categorie_info():
#     shopping_api = Shopping()
#     response = shopping_api.execute('GetCategoryInfo', {'CategoryID': '-1'})
#     print response

def byteify(input):
    """Encode unicode in dicts to utf8"""
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in
                input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class EbayHandler(object):
    """Communication with the ebay finding api"""

    def __init__(self):
        self.filepath = os.path.dirname(os.path.realpath(__file__))
        self.finding_api = Finding(config_file= self.filepath + '/ebay.yaml')
        self.search_requests = self.parse_search_config()


    def get_multi_page_result(self, request, search_size=0):
        """Collect unique results on multiple pages for given request"""
        results = []
        result_ids = []
        self.search_requests = self.parse_search_config()
        for page_number in range(1, search_size + 1):
            site_request = request
            site_request['paginationInput'] = {'entriesPerPage': '100',
                                               'pageNumber': page_number}

            print(site_request)
            response = self.finding_api.execute('findItemsAdvanced', site_request)
            for item in response.reply.searchResult.item:
                if item.itemId not in result_ids:
                    result_ids.append(item.itemId)
                    results.append(item)

        return results


    def parse_search_config(self, path=None):
        """Construct search requests from search config file"""
        if path is None:
            path = self.filepath + '/search.json' 

        results = []
        with open(path) as json_file:
            data = json.load(json_file)
            data = byteify(data)
            for key, value in data.iteritems():
                if 'request' in value.keys():
                    results.append(value['request'])

        return results


    def test(self):
        """method for testing some calls"""
        try:
            test_request = {
                'keywords': 'Viberg',
                'itemFilter' : [
                    {'name': 'LocatedIn',
                     'value': 'DE'}
                ]
            }
            results = self.get_multi_page_result(test_request, 2)
            for r in results:                     
                print r.title                     

        except ConnectionError as e:
            print(e)
            print(e.response.dict())




if __name__ == '__main__':
    e = EbayHandler()
    e.test()
    
