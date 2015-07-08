#!/usr/bin/env python

# Scraper is setup to search for all Instagram photos with the hashtag #vancouver
# and then to filter through those to find those that *also* have another hashtag
# (in the case below, "snow"). Can be altered by simply changing "snow" below to another
# hashtag. Takes awhile to run because has to go through a lot of #vancouver photos
# that don't match the other hashtag. Set to 60,000 max so wouldn't hit limits of Excel download

import scraperwiki
import instagram
from datetime import datetime
import time
import mechanize
import urllib2
from instagram.client import InstagramAPI
import re

br = mechanize.Browser()

api = InstagramAPI(client_id='895d2b07f8914cf6a50285796b59fd09', client_secret='f0983351e19645a28fd1aef32b87d739')

paginationid = 1

count = 0

while paginationid > 0:

    results = api.tag_recent_media(tag_name='vancouver', max_tag_id=paginationid) # uses #vancouver as basic hashtag
    
    print results
    
    resultsloop = results[0]
    
    for m in resultsloop:
        try:
            caption = m.caption.text
            print caption
        except:
            print 'no caption'
            caption = ""
        if "christmas" in caption or "xmas" in caption: # filters to #vancouver photos also tagged #snow; change "snow" to whatever you want
            count = count + 1
            print count
            print m
            username = m.user.username
            fullname = m.user.full_name
            link = m.link
            image = m.images['standard_resolution'].url
            imagelowres = m.images['low_resolution'].url
            thumbnail = m.images['thumbnail'].url
            created_time = m.created_time
            photoid = m.id
            caption = m.caption.text
            try:
                lat = m.location.point.latitude
                lng = m.location.point.longitude
            except:
                lat = "No Lat"
                lng = "No Long"
            record={}
            record["uniqueid"] = ""    
            record["username"] = ""
            record["fullname"] = ""
            record["link"] = ""
            record["image"] = ""
            record["created_time"] = ""
            record["lat"] = ""
            record["lng"] = ""
            record["photoid"] = ""
            record["caption"] = ""
            record["username"] = username
            record["fullname"] = fullname
            record["link"] = link
            record["image"] = image
            record["imagelowres"] = imagelowres
            record["thumbnail"] = thumbnail
            record["created_time"] = created_time
            record["lat"] = lat
            record["lng"] = lng
            record["caption"] = caption        
            record["photoid"] = str(photoid)    
            uniqueid = str(datetime.now())
            record["uniqueid"] = uniqueid
            try:
                scraperwiki.sqlite.save(['uniqueid'], record)
            except:
                print 'Could not add record'
            print record
        
        time.sleep(1) # made longer so as not to hit 5000/hr rate limit (not sure if that's per media item or per page of data)
        
    url = results[1]
    
    print url
    
    try:
        
        response = br.open(url).read()
    
    except:
        
        print 'Error loading page in Mechanize'
        
    print response
    
    try:
        pagination = re.search('next_max_id\":\"(.+?)\",', response)
        paginationid = pagination.group(1)
        print paginationid
    except:
        paginationid = 0
        print 'End of series'
        
    if count > 60000:
        paginationid = 0

