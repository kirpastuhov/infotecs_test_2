import json
from response.requestHandler import RequestHandler

class TemplateHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        # self.contentType = 'text/plain'

    def find(self, routeData):
        self.contentType ="text/html; charset=utf-8"
        try:
            template_file = open('templates/{}'.format(routeData['template']))
            self.contents = template_file
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False
    
    def func(self, data):
        self.contentType ="text/plain; charset=utf-8"
        self.contents = data
        self.setStatus(200)
        return True
