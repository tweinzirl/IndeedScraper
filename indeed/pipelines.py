# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import json

import unicodedata
import sys

#handles crazy unicode characters by translating them back into ACII
def unicodeHandle(stuff):
	return unicodedata.normalize('NFKD', stuff).encode('ascii','ignore')

#remove the data from the arrays and store them nicely in formatted strings
def cleanUpBrackets(stuff):
	if isinstance(stuff,str):
		return stuff
	if not stuff:
		return ''
	else:
		string = unicodeHandle(stuff.pop(0))
		for x in stuff:
			if not x == '':
				string = string + ', ' + unicodeHandle(x)
		return string

class indeedPipeline(object):
    
    def __init__(self):
    	self.file = open('items.txt','wb')
    
    def process_item(self, item, spider):
        thing = dict(item)
        
        title	= thing['title']
        url   = thing['url'] 
        location = thing['location']
        company = thing['company']
        
        delimiter = " # "
        
        line = title + delimiter + company + delimiter + location + delimiter + url
        
        print line
        sys.stdout.flush()
        
        return item
