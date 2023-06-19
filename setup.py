import site
import sys
from setuptools import setup

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

setup()
