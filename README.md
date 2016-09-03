# Simple producer-consumer example using a queue.
The program takes a list of URLs (from a file or stdin), extracts all hyperlinks from markup, and prints them as a list to stdout. Based on http://www.ibm.com/developerworks/aix/library/au-threadingpython/

# Requirements
* nose
* coverage
* bs4 >= 4.5.0
* requests >= 2.10.0

# Running tests
`nosetests -v --with-coverage --cover-package main tests.py`

# Read input from stdin
`cat ../data/urls.txt | python main.py`

# Read input from a file
`python main.py ../data/urls.txt`
