import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

from main import app as application
if __name__ == "__main__":
    application.run()
