#!/usr/bin/env python

"""
Simple producer-consumer example

Based on http://www.ibm.com/developerworks/aix/library/au-threadingpython/
"""

import sys
import Queue
import threading
from bs4 import BeautifulSoup
#import time
import json
import fileinput
import logging
import requests

def extract_html(url):
    """Return the HTML of a URL."""
    return requests.get(url, timeout=5).content

def extract_links_from_html(html):
    """Extract hyperlinks from HTML."""
    bs = BeautifulSoup(html, "html.parser")
    return [link.get('href') for link in bs.findAll('a')]

class Producer(threading.Thread):
    """Get URLs from the first queue, extract the markup
    and sends it to the second queue."""
    def __init__(self, in_queue, out_queue, logger):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.logger = logger

    def run(self):
        while True:
            #get url from the first queue
            host = self.in_queue.get()
            self.logger.debug('\n{} got {} from the first queue.\n'.format(self.getName(), host))

            #extract markup from url
            try:
                chunk = extract_html(host)
            except:
                chunk = None

            #send the url and markup to the second queue
            self.out_queue.put((host,chunk))

            #tell the queue that the task is done
            self.in_queue.task_done()
            self.logger.debug('\n{} sent results to the second queue {}.\n'.format(self.getName(), host))

class Consumer(threading.Thread):
    """Get markups from a queue, extract hyperlinks from each of them
     and prints it."""
    def __init__(self, in_queue, logger):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.logger = logger

    def run(self):
        while True:
            #get a url with its markup from the second queue
            chunk = self.in_queue.get()
            self.logger.debug('\n{} got {} from the second queue.\n'.format(self.getName(), chunk[0]))

            #extract hyperlinks from the markup
            if chunk[1]:
                try:
                    soup = extract_links_from_html(chunk[1])
                except:
                    soup = None
            else:
                soup = None

            #tell the queue that the task is done
            self.in_queue.task_done()
            self.logger.debug('\n{} finished processing {} from the second queue.\n'.format(self.getName(), chunk[0]))

            # jsonify the url and its hyperlinks and send it to stdout
            sys.stdout.write(json.dumps({'url': chunk[0], 'hyperlinks': soup}) + '\n')

if __name__ == '__main__':
    N_THREADS_PRODUCER = 5
    N_THREADS_CONSUMER = 5

    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    queue1 = Queue.Queue()
    queue2 = Queue.Queue()

    #start the first pool of threads, and initialize them with the queue instance
    for i in range(N_THREADS_PRODUCER):
        t = Producer(queue1, queue2, logger)
        t.setDaemon(True)
        t.start()

    logger.debug('First threads started')

    #insert data from stdin or a file into the queue
    for line in fileinput.input(sys.argv[1:]):
        queue1.put(line.rstrip('\n'))

    logger.debug('Populating queue finished')

    for i in range(N_THREADS_CONSUMER):
        dt = Consumer(queue2, logger)
        dt.setDaemon(True)
        dt.start()

    # Remove later
    #while True:
    #    time.sleep(1)

    logger.debug('Second threads started')

    #wait on the queue until everything has been processed
    queue1.join()
    logger.debug('First queue joined')
    queue2.join()
    logger.debug('Second queue joined')
