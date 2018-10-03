from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nlp2',
    version='1.0.5',
    description='Tool for NLP - handle file and text',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/voidful/nlp2',
    author='Eric Lam',
    author_email='voidful.stack@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='nlp file io string text mining',
    packages=find_packages()
)
