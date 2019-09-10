# -*- coding: utf-8 -*-
import os
import platform
import re
from codecs import open

from setuptools import setup

init_py_path = os.path.join('morris_counter', '__init__.py')
with open(init_py_path, 'r', encoding='utf8') as f:
    version = re.match(r".*__version__ = '(.*?)'", f.read(), re.S).group(1)

setup(
    name='morris_counter',
    packages=['morris_counter'],
    version=version,
    license='MIT License',
    platforms=['POSIX', 'Windows', 'Unix', 'MacOS'],
    description='Memory-efficient probabilistic counter namely Morris Counter',
    author='Yukino Ikegami',
    author_email='yknikgm@gmail.com',
    url='https://github.com/ikegami-yukino/morris_counter',
    keywords=['counter', 'probabilistic data structure', 'approximate counting'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    long_description='%s\n\n%s' % (open('README.rst', encoding='utf8').read(),
                                   open('CHANGES.rst', encoding='utf8').read()),
)
