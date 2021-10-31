import os
import sys
import math

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import config as app_config

bind = [f'0.0.0.0:{app_config.srv_port}']
worker_class = 'gevent'
workers = math.ceil(math.log2(os.cpu_count() + 1))
