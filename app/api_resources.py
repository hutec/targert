from flask_restful import Resource

class IgnoreItem(Resource):
    """Rest Endpoint for adding items to ignore list"""

    ignored_list = []
    def get(self,item_id):
        print(self.ignored_list)
        return self.ignored_list

    def post(self, item_id):
        self.ignored_list.append(item_id)
        print("Added " + item_id + " to ignore list")
        print(len(self.ignored_list))
