import os
import datetime
import json
from requests import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from pprint import pprint
from app import app, db
from app import models


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

    def get_categorie_info(self):
        shopping_api = Shopping()
        # UK = 3, Germany = 77
        response = shopping_api.execute('GetCategoryInfo',
                                        {'CategoryID': -1,
                                         'siteid': 77, 
                                         'IncludeSelector': 'ChildCategories'})
        pprint(response.reply)

    def __init__(self):
        self.filepath = os.path.dirname(os.path.realpath(__file__))
        self.finding_api = Finding(config_file= self.filepath + '/ebay.yaml')
        self.search_requests = self.parse_search_config()

        self.cached_results = []
        for req in self.search_requests:
            self.cached_results.extend(self.get_multi_page_result(req, 1))


    def get_multi_page_result(self, request, search_size=0):
        """Collect unique results on multiple pages for given request"""
        results = []
        result_ids = []
        self.search_requests = self.parse_search_config()
        for page_number in range(1, search_size + 1):
            site_request = request
            site_request['paginationInput'] = {'entriesPerPage': '100',
                                               'pageNumber': page_number}

            response = self.finding_api.execute('findItemsAdvanced',
                                                site_request)
            
            if not hasattr(response.reply.searchResult, 'item'):
                return []
                
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

    def get_cached_results(self):
        return self.cached_results

    def get_all_titles(self):
        titles = []
        for req in models.EbayRequest.query.all():
            titles.append(req.title)
        return titles


    def test(self):
        """method for testing some calls"""
        try:
            test_request = {
                'keywords': 'Red Wing',
                'itemFilter' : [
                    {'name': 'LocatedIn',
                     'value': 'DE'}
                ]
            }
            results = self.get_multi_page_result(test_request, 2)
            print(results[2])
            # for r in results:                     
            #     print r.title                     

        except ConnectionError as e:
            print(e)
            print(e.response.dict())




if __name__ == '__main__':
    e = EbayHandler()
    #e.get_categorie_info()
    e.test()
    
