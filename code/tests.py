import logging
import Queue
#import time
from main import Consumer, Producer, extract_html, extract_links_from_html

#from nose.tools import assert_equal
#from nose.tools import assert_not_equal
#from nose.tools import assert_raises
#from nose.tools import raises

class TestExtractHtml(object):
    def test_extract_html(self):
        extract_html('http://www.math.sk/siran/')

class TestExtractLinksFromHtml(object):
    def test_extract_links(self):
        extract_links_from_html(extract_html('http://stackoverflow.com/'))

class TestProducer(object):
    def test_producer(self):
        N_THREADS_PRODUCER = 5

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        with open('../data/urls.txt') as f:
            urls = f.readlines()

        queue1 = Queue.Queue()
        queue2 = Queue.Queue()

        for i in range(N_THREADS_PRODUCER):
            t = Producer(queue1, queue2, logger)
            t.setDaemon(True)
            t.start()

        for url in urls:
            queue1.put(url.rstrip('\n'))

        #while True:
        #    time.sleep(1)

        queue1.join()

class TestConsumerProducer(object):
    pass

class TestConsumer(object):
    pass
