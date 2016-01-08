#!/usr/bin/env python
from setuptools import setup, find_packages

from splitwise import VERSION


setup(
    name='splitwise-openexchangerates-python-client',
    version=VERSION,
    url='https://github.com/nlindblad/splitwise-openexchangerates-python-client',
    description=(
        "Splitwise client that seamlessly converts currencies using Open Exchange Rates"),
    long_description=open('README.rst').read(),
    keywords="Splitwise",
    license=open('LICENSE').read(),
    platforms=['linux'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=['oauth2'],
    extras_require={},
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
        'Topic :: Office/Business :: Financial'],
)
