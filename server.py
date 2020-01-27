#!/usr/bin/env python3
import time
import pandas as pd
from http.server import HTTPServer

from main_server import Server

HOST_NAME = "localhost"
PORT_NUMBER = 8000


if __name__ == "__main__":
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), "Server Up - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Down - %s:%s" % (HOST_NAME, PORT_NUMBER))
   