IndeedScraper
=============

Spider to make custom searches of Indeed

This code executes a custom search of Indeed.com based on user-specified 
"what" and "where" keywords.  It is recommended to run the code with

>>> sh searchwrapper.sh

which repeatedly runs the code for an input list of "where" keywords.
The default "what" keywords are "data science scientist" and can be 
changed within indeed/spiders/indeed_jobsearch.py on line 31. The
scraping process is visually displayed in an instance of Chromedriver.

From the search results page, four items are scraped and stored in an output
text file: company name, job location, job title, and the Indeed job link.

Dependencies:

Scrapy (http://scrapy.org/)
Selenium (http://docs.seleniumhq.org/)
Chromedriver (http://code.google.com/p/selenium/wiki/ChromeDriver)
