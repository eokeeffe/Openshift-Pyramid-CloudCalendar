import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
REQUIRES = open(os.path.join(here, 'REQUIRES.txt')).readlines()

requires = REQUIRES

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='pyramidapp',
      version='0.0',
      description='pyramidapp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = requires,
      test_suite="pyramidapp",
      entry_points = """\
      [paste.app_factory]
      main = pyramidapp:main
      [console_scripts]
      initialize_pyramidapp_db = pyramidapp.scripts.initializedb:main
      """,
      paster_plugins=['pyramid'],
      )