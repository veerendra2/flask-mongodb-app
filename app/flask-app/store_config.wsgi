#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/usr/local/apache2/htdocs/flask-app")

from http_api import app as application
