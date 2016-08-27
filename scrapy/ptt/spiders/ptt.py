import logging

from datetime import datetime

import html2text
import scrapy

from scrapy.http import FormRequest

from ptt.items import PostItem


class PTTSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    start_urls = ('https://www.ptt.cc/bbs/Gossiping/index.html', )

    _retries = 0
    MAX_RETRY = 1

    _pages = 0
    MAX_PAGES = 2

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            if self._retries < PTTSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.parse)
            else:
                logging.warning('you cannot pass')

        else:
            self._pages += 1
            for href in response.css('.r-ent > div.title > a::attr(href)'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_post)

            if self._pages < PTTSpider.MAX_PAGES:
                next_page = response.xpath(
                    '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('no next page')
            else:
                logging.warning('max pages reached')

    def parse_post(self, response):
        item = PostItem()
        item['title'] = response.xpath(
            '//meta[@property="og:title"]/@content')[0].extract()
        item['author'] = response.xpath(
            '//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()')[
                0].extract().split(' ')[0]
        datetime_str = response.xpath(
            '//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[
                0].extract()
        item['date'] = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        item['content'] = converter.handle(response.xpath('//div[@id="main-content"]')[ 0].extract())

        comments = []
        total_score = 0
        for comment in response.xpath('//div[@class="push"]'):
            push_tag = comment.css('span.push-tag::text')[0].extract()
            push_user = comment.css('span.push-userid::text')[0].extract()
            push_content = comment.css('span.push-content::text')[0].extract()

            if '推' in push_tag:
                score = 1
            elif '噓' in push_tag:
                score = -1
            else:
                score = 0

            total_score += score

            comments.append({'user': push_user,
                             'content': push_content,
                             'score': score})

        item['comments'] = comments
        item['score'] = total_score
        item['url'] = response.url

        yield item
