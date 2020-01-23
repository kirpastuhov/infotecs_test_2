import os

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

from routes.main import routes

from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from geo import getbygeonameid, getcities


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        # print (split_path)
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        # print(request_extension)
        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            elif 'id' in query_components:
                # print(query_components)
                geo_id = query_components["id"][0]
                data = getbygeonameid(geo_id)
                handler = TemplateHandler()
                handler.func(data)
            elif 'city1' and 'city2' in query_components:
                city1 = query_components['city1'][0]
                city2 = query_components['city2'][0]
                data = getcities(city1, city2)
                handler = TemplateHandler()
                handler.func(data)
            else:
                handler = BadRequestHandler()

        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        content_type = handler.getContentType()

        self.send_response(status_code)

        if status_code == 200:
            if 'html' in content_type:
                content = handler.getContents()
            elif 'plain' in content_type:
                content = handler.read()
            self.send_header('Content-type', content_type)
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'utf-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
