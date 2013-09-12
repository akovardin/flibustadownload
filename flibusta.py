#!/usr/bin/env python

"""flibusta.net downloader.

Usage:
  flibusta.py --page=<page> [--saveto=<folder>]
  flibusta.py (-h | --help)
  flibusta.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --page=<page>      Download all books from this page
  --saveto=<folder>  Save all books in this folder [default: ./download]
"""
from __future__ import print_function
import urllib2
import os
from docopt import docopt
from bs4 import BeautifulSoup

SERVER = "http://flibusta.net/"


def get_html(page):
    response = urllib2.urlopen("".join([SERVER, page]))
    html = response.read()
    return BeautifulSoup(html)


def get_book(link, arguments):
    url = link.get('href')
    name = link.parent.find('a')
    name = name.get_text()+".fb2.zip"
    book = urllib2.urlopen("".join([SERVER, url]))
    download_book(book, name, arguments)


def download_book(book, name, arguments):
    saveto = arguments['--saveto']
    try:
        os.makedirs(saveto)
    except:
        pass

    try:
        localbook = open(os.path.join(saveto, name), 'wb')
    except:
        return
    meta = book.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = book.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        localbook.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status),

    localbook.close()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='flibusta.net downloader 0.1.0')
    soup = get_html(arguments['--page'])
    for link in soup.find_all('a', text="(fb2)"):
        get_book(link, arguments)
