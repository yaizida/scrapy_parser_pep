import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains, start_urls = (['peps.python.org'],
                                   ['https://peps.python.org/'])

    def parse(self, response):
        """собирает ссылки на документы PEP."""
        all_peps = response.xpath(
            '//a[@class="pep reference internal"]/@href'
        ).getall()
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """парсит страницы с документами и формирует Items."""
        number, _, *name = response.css(
            'h1.page-title::text'
        ).get().split()
        data = {
            'number': number,
            'name': ' '.join(name).strip(),
            'status': response.css(
                'dt:contains("Status")+dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
