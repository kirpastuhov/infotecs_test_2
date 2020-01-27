import os

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs

from routes.urls import routes

from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from geo.geo_methods import getbygeonameid, getcities, cities_list_info


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        url = self.path.split("/")[1]
        if url in routes:
            if url == "geonameid" and "id" in query_components:
                print(query_components)
                geo_id = query_components["id"][0]
                data = getbygeonameid(geo_id)
                handler = TemplateHandler()
                handler.func(data)
            elif url == "cmpcities" and "city1" and "city2" in query_components:
                city1 = query_components['city1'][0]
                city2 = query_components['city2'][0]
                data = getcities(city1, city2)
                handler = TemplateHandler()
                handler.func(data)
            elif url == "cities_list" and "cities_list" and "amount" in query_components:
                cities_list = query_components["cities_list"]
                data = cities_list_info([s.strip() for s in cities_list[0].split(",")])
                handler = TemplateHandler()
                handler.func(data)
            else:
                handler = TemplateHandler()
                handler.find(routes[url])
        else:
            handler = BadRequestHandler()

        self.respond({
            "handler": handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()
        content_type = handler.getContentType()

        self.send_response(status_code)

        if status_code == 200:
            if "html" in content_type:
                content = handler.getContents()
            elif "plain" in content_type:
                content = handler.read()
            self.send_header("Content-type", content_type)
        else:
            content = "404 Not Found"

        self.end_headers()
        return bytes(content, "utf-8")

    def respond(self, opts):
        response = self.handle_http(opts["handler"])
        self.wfile.write(response)
