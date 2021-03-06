import json
from response.requestHandler import RequestHandler

class TemplateHandler(RequestHandler):
    def __init__(self):
        super().__init__()

    def find(self, routeData):
        self.contentType ="text/html; charset=utf-8"
        try:
            template_file = open("templates/{}".format(routeData["template"]))
            self.contents = template_file
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False
    
    def create_json(self, data):
        self.contentType ="application/json; charset=utf-8"
        self.contents = data
        self.setStatus(200)
        return True
