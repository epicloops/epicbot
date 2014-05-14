# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from epiclib.config import read_config


BOT_NAME = 'epicbot',
SPIDER_MODULES = ['epicbot.spiders']

# disable logging
# don't use scrapy.log.ScrapyFileLogObserver instead we use
# twisted.python.log.PythonLoggingObserver in epicbot.extensions.PythonLogging
# to redirect log events toPython's standard logging module
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

# optimized
# http://support.scrapinghub.com/topic/187082-optimizing-scrapy-settings-for-crawlera/
# This seemed to be crashing the xmlinfo soundclick page
# 'CONCURRENT_REQUESTS = 100,
# 'CONCURRENT_REQUESTS_PER_DOMAIN = 100,
# 'AUTOTHROTTLE_ENABLED = False,
# 'DOWNLOAD_TIMEOUT = 600,

# delayed
DOWNLOAD_DELAY = 5   # echonest api limit is 20/min.
                     # 3 secs even doesn't fix the issue, most likely
                     # because our api calls are deffered to twisted
                     # threads so their frequency isn't directly
                     # correlated to this delay. TODO: find better fix
AUTOTHROTTLE_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapylib.crawlera.CrawleraMiddleware': 600,
}

ITEM_PIPELINES = {
    # Add any additional post crawl data to every item returned from spiders
    'epicbot.pipelines.post_crawl.PostCrawlPipeline': 200,
    # Drop dups based on track_id.
    'epicbot.pipelines.filters.DuplicatesPipeline': 300,
    # Check for CC license and download flag
    'epicbot.pipelines.filters.CCFilterPipeline': 400,
    # Download track data and store it in S3
    'epicbot.pipelines.track.TrackPipeline': 500,
    # Run the track against the echonest api and gather data.
    'epicbot.pipelines.echonest.EchonestPipeline': 600,
    # Persist item to db
    'epicbot.pipelines.db.DbPipeline': 700,
    # Write item to queue to be picked up by samplers
    'epicbot.pipelines.queue.QueuePipeline': 800,
}

EXTENSIONS = {
    # 'epicbot.extensions.PythonLogging': 200,
    'epicbot.extensions.ExtStats': 300,
    'epicbot.extensions.PersistDroppedItems': 400,
}

# CLOSESPIDER_TIMEOUT:
CLOSESPIDER_ITEMCOUNT = 1000
CLOSESPIDER_PAGECOUNT = 20000   # ~1000 tracks at $30 conservative
                                # ~ $25 crawlera + ~ $2 scrapinghub
CLOSESPIDER_ERRORCOUNT = 20



epiclib_config = read_config()

for k, v in epiclib_config.items():
    if k == 'log_level':
        v = v.upper()
    setattr(sys.modules[__name__], k.upper(), v)
