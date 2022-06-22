#!/usr/bin/env python

from distutils.command.install import INSTALL_SCHEMES
from os.path import abspath, dirname, join

from setuptools import setup
from setuptools.command.install import install

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup_args = {
    'cmdclass': {'install': install},
    'name': 'nerodia',
    'version': '0.14.1',
    'license': 'MIT',
    'description': 'Python port of WATIR https://github.com/watir/watir',
    'long_description': open(join(abspath(dirname(__file__)), 'README.rst')).read(),
    'url': 'https://github.com/watir/nerodia',
    'python_requires': '~=3.7',
    'classifiers': ['Intended Audience :: Developers',
                    'Operating System :: POSIX',
                    'Operating System :: Microsoft :: Windows',
                    'Operating System :: MacOS :: MacOS X',
                    'Topic :: Software Development :: Testing',
                    'Topic :: Software Development :: Libraries',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7'],
    'install_requires': ['selenium~=4.0',
                         'six',
                         'python-dateutil'],
    'package_dir': {'nerodia': 'nerodia'},
    'packages': ['nerodia',
                 'nerodia.elements',
                 'nerodia.locators',
                 'nerodia.locators.button',
                 'nerodia.locators.cell',
                 'nerodia.locators.element',
                 'nerodia.locators.row',
                 'nerodia.locators.text_area',
                 'nerodia.locators.text_field',
                 'nerodia.wait'],
    'package_data': {
        'nerodia': ['js_snippets/*.js']
    },
    'zip_safe': False
}

setup(**setup_args)
