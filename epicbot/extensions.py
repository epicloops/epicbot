# -*- coding: utf-8 -*-
'''
Scrapy extensions.
'''
from __future__ import unicode_literals

from twisted.python.log import PythonLoggingObserver

import scrapy
from scrapy import log
from scrapy.settings import overridden_settings
from scrapy import signals

from epiclib.db import session


class PersistDroppedItems(object):
    '''Writes dropped items to db.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.session = session(self.settings['SQLALCHEMY_DATABASE_URI'])

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.item_dropped, signals.item_dropped)
        return ext

    def item_dropped(self, item, spider, exception):

        item['dropped_item_exception'] = str(exception)

        self.session.add(item.instance(dropped=True))
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        else:
            log.msg(format='Persisted: Dropped - %(track_page_url)s',
                    level=log.DEBUG, spider=spider,
                    track_page_url=item['track_page_url'])

        return item


class ExtStats(object):
    '''Add extended stats to crawler object.'''

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        return ext

    def spider_opened(self, spider):
        self.stats.set_value('spider_start_{}'.format(spider.name),
                             self.stats.get_value('start_time'))
        self.stats.set_value('crawl_id', spider.opts.crawl_id)


class PythonLogging(object):
    '''Direct scrapy/twisted logging to standard Python logging.'''

    def __init__(self, crawler):
        settings = crawler.settings
        observer = PythonLoggingObserver(loggerName='epicbot')
        observer.start()
        log.msg('Scrapy {} starting (bot: {})'.format(scrapy.__version__,
                                                      settings['BOT_NAME']))

        log.msg('Optional features available: {}'.format(
                                        ', '.join(scrapy.optional_features)))

        d = dict(overridden_settings(settings))
        log.msg(format='Overridden settings: %(settings)r', settings=d)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
