#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/outline.braiiin.com/client")
sys.path.insert(0,"/var/www/outline.braiiin.com")

from outline_client import create_outline_app

application = create_outline_app(root='outline_client', config='ProductionConfig')

if __name__ == "__main__":
    application.run(**application.config['INIT'])
