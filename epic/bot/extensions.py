# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twisted.internet import threads

from scrapy import log
from scrapy import signals
from scrapy.exceptions import NotConfigured

from epic.models import session, Dropped


class DroppedItemsCsv(object):

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.Session = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('PERSIST_DROPPED_ITEMS_ENABLED'):
            raise NotConfigured

        ext = cls(crawler)

        crawler.signals.connect(ext.spider_opened, signals.spider_opened)
        crawler.signals.connect(ext.item_dropped, signals.item_dropped)

        return ext

    def spider_opened(self, spider):
        self.Session = session()

    def item_dropped(self, item, spider, exception):

        def _persist_item(item):
            item['dropped_item_exception'] = str(exception)

            item_record = dict([(k, v) for k, v in item.items() if k in Dropped.__table__.columns])

            session = self.Session()
            try:
                session.add(Dropped(**item_record))
            except:
                session.rollback()
                raise
            else:
                session.commit()
                log.msg(format='Persisted: Dropped - %(track_url)s',
                        level=log.DEBUG, spider=spider,
                        track_url=item_record['track_url'])
            finally:
                session.close()
            return item

        return threads.deferToThread(_persist_item, item)