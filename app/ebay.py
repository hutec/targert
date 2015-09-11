import os
import datetime
import json
from requests import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.parallel import Parallel
from ebaysdk.exception import ConnectionError
from pprint import pprint
from app import app, db
from app import models


class EbayHandler(object):
    """Communication with the ebay finding api"""

    def get_categorie_info(self):
        """ Get category info for specific item """

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
        # self.search_requests = self.parse_search_config()
        self.search_requests = self.get_searches()

        self.cached_results = {}
        for search in self.search_requests:
            self.add_search(search)

    def add_search(self, ebay_request):
        """ Add new search and cache it """
        self.cached_results[ebay_request.title] = \
            self.get_multi_page_result(ebay_request.get_request(), 1)


    def remove_search(self, title):
        """ Remove search from DB and cache """

        models.EbayRequest.query.filter(models.EbayRequest.title == title).\
            delete()
        db.session.commit()

        if title in self.cached_results:
            del self.cached_results[title]


    def get_multi_page_result(self, request, search_size=0):
        """Collect unique results on multiple pages for given request
        
        Note that just the request dict without the 'request' key is needed 
        """
        results = []
        result_ids = []
        for page_number in range(1, search_size + 1):
            site_request = request
            site_request['paginationInput'] = {'entriesPerPage': '100',
                                               'pageNumber': page_number}
            site_request['categoryId'] = [1059]

            response = self.finding_api.execute('findItemsAdvanced',
                                                site_request)
            

            if not hasattr(response.reply.searchResult, 'item'):
                return []
                
            for item in response.reply.searchResult.item:
                if item.itemId not in result_ids:
                    result_ids.append(item.itemId)
                    results.append(item)

        return results


    def get_searches(self):
        """ Get all searches from DB """
        searches = []
        for search in models.EbayRequest.query.all():
            searches.append(search)
        return searches


    def get_cached_results(self):
        return self.cached_results

    def get_all_titles(self):
        titles = []
        for req in models.EbayRequest.query.all():
            titles.append(str(req.title))
        return titles

    def get_search_results(self, title=None):
        print(self.cached_results.keys())
        if title is None:
            return None
        if title in self.cached_results:
            return self.cached_results[title]
        print("Key " + title + " is not in cached results")
        return None


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
    
