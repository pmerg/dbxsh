from setuptools import setup
import os
import sys

try:
    version = subprocess.check_output(["git", "describe"]).rstrip()
except:
    version = '0.0.dev'

setup(
    name='dbxsh',
    version="{ver}".format(ver=version),
    author='Panayotis Vryonis',
    author_email='vrypan@gmail.com',
    packages=['dbxsh'],
    scripts=['dbxsh.py'],
    include_package_data=True,
    url='http://www.vrypan.net/',
    license='MIT-LICENSE.txt',
    description='Dropbox commandline tools (unofficial).',
    long_description=open('README.rst').read(),
    install_requires=[
        "docopt",
        "dropbox",
    ],
    dependency_links = ['https://github.com/dropbox/dropbox-sdk-python/tarball/master'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
